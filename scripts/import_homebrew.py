"""Rebuild the first import from archived HTML and cached translations.

Run: python3 scripts/import_homebrew.py
Only --translate allows network translation; normal rebuilds are offline.
Archived original files are never modified. Generated Markdown and SVG are rebuilt.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, re, sys, time, unicodedata

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / 'archives/articles/homebrew-ai-toolbox'
ASSETS = ROOT / 'src/assets/blog/homebrew-ai-toolbox'
CONTENT = ROOT / 'src/content/blog'
LANGS = ['zh', 'en', 'fr', 'es', 'ru', 'ar']
SLUG = 'homebrew-ai-toolbox'
TITLE = '别再挨个追新了：用 Homebrew 管好你 Mac 上的 AI 工具'
DESCRIPTION = '用 Homebrew 统一安装、升级和管理 Mac 上的 AI 工具，附热门工具覆盖情况、更新时差统计与图形界面选择指南。'
CACHE_PATH = ARCHIVE / 'translations.json'
cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}

class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self):
        return ''.join(x if isinstance(x, str) else x.text() for x in self.children)
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root'); self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        n=Node(tag, attrs); self.stack[-1].children.append(n)
        if tag not in ['br','img','meta','link','hr','input']: self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag==tag: self.stack.pop()
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:
                self.stack=self.stack[:i]; break
    def handle_data(self, text): self.stack[-1].children.append(text)

def descendants(n, tag):
    result=[]
    for c in n.children:
        if isinstance(c, Node):
            if c.tag==tag: result.append(c)
            result.extend(descendants(c,tag))
    return result

figures=[]
def md(n):
    if isinstance(n,str): return n
    inner=lambda: ''.join(md(c) for c in n.children)
    if n.tag=='figure':
        figures.append(n)
        return '\n\nFIGURETOKEN%02d\n\n' % len(figures)
    if n.tag=='pre': return '\n\n```sh\n'+n.text().strip()+'\n```\n\n'
    if n.tag=='code': return '`'+n.text()+'`'
    if n.tag in ['strong','b']: return '**'+inner()+'**'
    if n.tag=='a': return '['+inner()+']('+n.attrs['href']+')'
    if n.tag=='mark': return '【'+n.text()+'】'
    if n.tag=='br': return ' / '
    if n.tag in ['h1','h2','h3']: return '\n\n'+'#'*int(n.tag[1])+' '+inner().strip()+'\n\n'
    if n.tag=='p': return '\n\n'+inner().strip()+'\n\n'
    if n.tag=='li': return '- '+inner().strip()+'\n'
    if n.tag=='ul': return '\n\n'+inner().strip()+'\n\n'
    if n.tag=='table':
        rows=descendants(n,'tr'); out=[]
        for i,row in enumerate(rows):
            cells=[x for x in row.children if isinstance(x,Node) and x.tag in ['td','th']]
            out.append('| '+' | '.join(md(c).strip().replace('|','\\|') for c in cells)+' |')
            if i==0: out.append('| '+' | '.join(['---']*len(cells))+' |')
        return '\n\n'+'\n'.join(out)+'\n\n'
    return inner()

parser=Parser(); parser.feed((ARCHIVE/'source.html').read_text())
article=descendants(parser.root,'article')[0]
source=''.join(md(n) for n in article.children if not (isinstance(n,Node) and n.tag=='h1'))
source=re.sub(r'\n{3,}','\n\n',source).strip()

# Image labels, descriptions and reconstruction prompts are translated with prose.
labels={
 'before':'以前：各装各的', 'after':'现在：统一交给 Homebrew',
 'methods':'三种装法、三套升级方式', 'unified':'一个入口、一条升级命令',
 'curl':'curl 脚本', 'dmg':'官网 dmg', 'npm':'npm',
 'delay':'官方发布到 Homebrew 的中位时差', 'hours':'小时',
 'delay-note':'2026-08-11 至 2026-11-09；GitHub 发布时间（Claude Code 使用 npm）至 Homebrew 合并时间。',
 'coverage':'热门 AI 软件：23 个中 17 个可用 Homebrew 安装',
 'core':'官方仓库', 'tap':'项目自有 tap', 'none':'暂未收录',
 'agents':'AI Agent 和编程助手', 'models':'本地模型', 'other':'其他 AI 工具和桌面 App',
 'desktop':'ComfyUI 桌面版',
 'coverage-note':'截至 2026-11-09；15 个官方仓库、2 个项目 tap。每个方块代表一个项目。',
 'stars':'AI 相关包的 GitHub 星数分布', 'packages':'包数量',
 'star-low':'少于 1000 星', 'star-mid':'1000 至 1 万星', 'star-high':'1 万至 10 万星', 'star-top':'10 万星以上',
 'stars-note':'297 个可查到星数的包；按 AI 关键词粗略筛选，可能存在误判。',
 'installs':'过去 30 天的 Homebrew 安装次数',
 'installs-note':'截至 2026-11-09；仅统计开启分析的用户；Ollama App 版另有 8,975 次。',
 'screens':'Homebrew.app 截图待补', 'main':'主界面', 'updates':'升级列表', 'command':'对应命令提示',
 'screens-note':'这是明确标注的占位图，不是真实产品截图；原稿记载 macOS 26+，版本 0.6.0。',
 'choice':'图形界面怎么选',
 'new-system':'macOS 26 或更新：官方 Homebrew.app',
 'apps-only':'系统较旧，只管理普通 App：Applite',
 'advanced':'需要更细的管理：Cork', 'terminal':'喜欢终端：Bold Brew',
 'choice-note':'按原稿建议重绘；功能与兼容性仍应参考项目官方说明。',
}

chart_specs=[
 ('01-unified-management','before','对比流程图。左栏依次连接 curl 脚本到 Claude Code、官网 dmg 到 Ollama、npm 到 Gemini CLI；右栏由 Homebrew 和 brew upgrade 统一连接这三个工具。上方说明三套升级方式与一个入口的差别。'),
 ('02-update-delay','delay','水平条形图，单位小时。OpenCode 0.5、uv 1.6、llama.cpp 1.6、Codex 1.8、Claude Code 3.5、Hermes Agent 6.7、OpenClaw 8.0、Ollama 25.0、Gemini CLI 26.8。统计区间 2026-08-11 至 2026-11-09；仅统计能匹配的版本，中位时差不是完整覆盖率。'),
 ('03-tool-coverage','coverage','项目覆盖矩阵。Agent 8/8：OpenClaw、DeepSeek Harness、Hermes Agent、OpenCode、Claude Code、Codex、Gemini CLI、Pi，均为官方仓库。本地模型 3/3：Ollama、llama.cpp、Whisper，均为官方仓库。其他工具 6/12：cc-switch、spec-kit、ComfyUI 桌面版、Open Design 为官方仓库；Orca、VoiceStudio 为项目 tap；claw-code、Stable Diffusion WebUI、Graphify、MoneyPrinterTurbo、Paperclip、RuView 未收录。总计 17/23，其中官方 15、tap 2。'),
 ('04-star-distribution','stars','水平条形图，297 个 AI 相关包按 GitHub 星数分组：少于 1000 星 88 个，1000 至 1 万星 126 个，1 万至 10 万星 72 个，10 万星以上 11 个。按关键词粗略筛选，可能存在误判。'),
 ('05-install-counts','installs','水平条形图，过去 30 天安装次数：Codex 351138、uv 206718、Ollama 62453、Claude Code 58378、OpenCode 45393、llama.cpp 35373。Ollama 只含命令行版，App 版另有 8975 次。数据截至 2026-11-09，只统计开启分析的用户。'),
 ('06-screenshot-placeholders','screens','三张虚线边框占位卡片，分别标明 Homebrew.app 主界面、升级列表和对应命令提示截图待补。明确标为占位示意，不模仿或伪造真实界面。原稿版本 0.6.0，要求 macOS 26 及以上。'),
 ('07-gui-selection','choice','选择指南，四行建议：macOS 26 或更新选择官方 Homebrew.app；较旧系统且只管理图形 App 选择 Applite；需要更细管理选择 Cork；喜欢终端选择 Bold Brew。保留原稿建议并注明以官方兼容性说明为准。'),
]
base_prompt='重建 prompt：制作独立原生 SVG 信息图，不含 HTML、脚本或远程依赖。白色背景，深蓝正文 #203047，蓝色图形 #275fa4，紫色区分项目 tap，灰色区分未收录。宽 1000 像素，高度随内容调整；标签清晰换行，不裁切；阿拉伯文使用从右向左文字排版。文字语言为 LANG。'
lang_names={'zh':'中文','en':'English','fr':'français','es':'español','ru':'русский','ar':'العربية'}
texts=[TITLE,DESCRIPTION,'AI 工具','文中数据截至 2026 年 11 月 9 日']
# Every prose line is translated as a whole, retaining Markdown emphasis and inline code.
lines=source.splitlines()
translate_lines=[x for x in lines if x.strip() and not x.startswith('FIGURETOKEN') and not x.startswith('```') and not x.startswith('brew ') and not re.fullmatch(r'[| :\-]+',x)]
texts+=translate_lines+list(labels.values())
for _,key,details in chart_specs:
    for lang in LANGS:
        texts.append(details+' '+base_prompt.replace('LANG',lang_names[lang]))
texts=list(dict.fromkeys(texts))

def needed_texts(lang):
    return [t for t in texts if not t.startswith('|') and ('文字语言为 ' not in t or t.endswith('文字语言为 '+lang_names[lang]+'。'))]

def cache_key(lang,text): return lang+':'+hashlib.sha256(('v2:'+text).encode()).hexdigest()
TABLE_WORDS = {
 'en': ['Tool','Median delay','Within 6 hours','Within 24 hours','Longest delay','Total','hours','stable release'],
 'fr': ['Outil','Délai médian','En 6 heures','En 24 heures','Délai maximal','Total','heures','version stable'],
 'es': ['Herramienta','Retraso mediano','En 6 horas','En 24 horas','Retraso máximo','Total','horas','versión estable'],
 'ru': ['Инструмент','Медианная задержка','За 6 часов','За 24 часа','Максимальная задержка','Итого','ч','стабильная версия'],
 'ar': ['الأداة','وسيط التأخر','خلال 6 ساعات','خلال 24 ساعة','أطول تأخر','الإجمالي','ساعة','الإصدار المستقر'],
}
def table_row(lang,text):
    words=TABLE_WORDS[lang]
    mapping=dict(zip(['工具','中位时差','6 小时内上架','24 小时内上架','最慢一次','合计'],words))
    cells=[c.strip() for c in text.strip('|').split('|')]
    return '| '+' | '.join(mapping.get(c,c).replace('小时',words[6]).replace('（正式版）',' ('+words[7]+')').replace('（@latest）',' (@latest)').replace('（',' (').replace('）',')') for c in cells)+' |'

def trans(lang,text):
    if lang=='zh' or not re.search(r'[\u3400-\u9fff]',text): return text
    if text.startswith('|'): return table_row(lang,text)
    key=cache_key(lang,text)
    if key not in cache: raise RuntimeError('Missing cached translation: '+lang+' '+text[:60]+'; use --translate explicitly')
    return cache[key]

def translate_batch(item):
    lang,batch=item
    protected={}
    def protect(m):
        key='ZXQKEEP%04dQXZ'%len(protected); protected[key]=m.group(0); return key
    prepared=[]
    for i,text in enumerate(batch):
        # Protect code, URLs and numeric cells; their exact spelling is part of the source.
        value=re.sub(r'`[^`]+`|https?://[^\s)]+|[A-Za-z][A-Za-z0-9_.@+\-]*(?: [A-Z][A-Za-z0-9_.@+\-]*)*|[0-9]+(?:[.,][0-9]+)*',protect,text)
        prepared.append('ZXQITEM%04dQXZ '%i+value)
    q=prepared[0].split(' ',1)[1] if len(batch)==1 else '\n\n'.join(prepared)
    url='https://translate.googleapis.com/translate_a/single?'+urlencode({'client':'gtx','sl':'zh-CN','tl':lang,'dt':'t','q':q})
    last=None
    for attempt in range(4):
        try:
            data=json.load(urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40))
            output=''.join(x[0] or '' for x in data[0])
            if len(batch)==1:
                segments=[(0, output)]
            else:
                matches=list(re.finditer(r'ZXQITEM\s*(\d{4})\s*QXZ\s*',output,re.I))
                if len(matches)!=len(batch): raise ValueError('Translation lost item markers')
                segments=[(int(m.group(1)), output[m.end():matches[j+1].start() if j+1<len(matches) else len(output)].strip()) for j,m in enumerate(matches)]
            results={}
            for item_index,value in segments:
                for token,original in protected.items(): value=re.sub(token,lambda _:original,value,flags=re.I)
                if re.search(r'ZXQKEEP',value,re.I): raise ValueError('Translation damaged protected token')
                # Code and URL literals must survive translation exactly.
                original=batch[item_index]
                for literal in re.findall(r'`[^`]+`|https?://[^\s)]+',original):
                    if literal not in value: raise ValueError('Translation lost literal: '+literal)
                # Remove invisible zero-width artifacts, not Arabic shaping characters.
                value=re.sub(r'\s+', ' ', value.replace('\u200b','').replace('\ufeff','')).strip()
                results[cache_key(lang,original)]=value
            return results
        except Exception as e:
            last=e; time.sleep((attempt+1)*10 if getattr(e, 'code', None)==429 else attempt+1)
    raise RuntimeError(str(last))

if '--translate' in sys.argv:
    work=[]
    for lang in LANGS[1:]:
        missing=[t for t in needed_texts(lang) if re.search(r'[\u3400-\u9fff]',t) and cache_key(lang,t) not in cache]
        batch=[]; size=0
        for t in missing:
            if batch: work.append((lang,batch)); batch=[]; size=0
            batch.append(t); size+=len(t)+30
        if batch: work.append((lang,batch))
    print('Translation batches:',len(work),flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,result in enumerate(pool.map(translate_batch,work)):
            cache.update(result); CACHE_PATH.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
            
            if (i+1)%50 == 0 or i+1 == len(work): print('Cached batch',i+1,'/',len(work),flush=True)

def width_units(text): return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in text)
def wrap(text,max_units):
    # Word-aware wrapping, with a character fallback for CJK and long labels.
    words=text.split(' ') if ' ' in text else list(text)
    lines=[]; current=''; sep=' ' if ' ' in text else ''
    for word in words:
        if current and width_units(current+sep+word)>max_units: lines.append(current); current=word
        else: current=current+sep+word if current else word
    if current: lines.append(current)
    return lines or ['']

def make_svg(lang,index):
    name,key,details=chart_specs[index]
    L=lambda k:trans(lang,labels[k])
    prompt=trans(lang,details+' '+base_prompt.replace('LANG',lang_names[lang]))
    title=(L('methods')+' / '+L('unified')) if index==0 else L(key); rtl=lang=='ar'; items=[]; y=42
    def text(value,x=32,size=22,color='#203047',max_units=78,bold=False):
        nonlocal y
        chunks=wrap(value,max_units)
        if rtl: x=1000-x
        for line in chunks:
            items.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="start" direction="{"rtl" if rtl else "ltr"}" unicode-bidi="embed"'+(' font-weight="600"' if bold else '')+'>'+escape(line)+'</text>')
            y+=size*1.5
    text(title,size=29,max_units=58,bold=True);y+=12
    def bar(label,value,max_value,display):
        nonlocal y
        text(label,size=22,max_units=76)
        length=round(720*value/max_value,1)
        items.append(f'<rect x="32" y="{y-12}" width="720" height="24" rx="5" fill="#e7edf5"/>')
        items.append(f'<rect x="32" y="{y-12}" width="{max(length,3)}" height="24" rx="5" fill="#275fa4"/>')
        items.append(f'<text x="778" y="{y+8}" font-size="22" fill="#203047" direction="ltr">{escape(display)}</text>')
        y+=45
    if index==0:
        start=y
        for x in [28,516]:
            items.append(f'<rect x="{x}" y="{start-18}" width="456" height="390" rx="12" fill="#f4f7fb" stroke="#d9e2ee"/>')
        text(L('before'),x=48,size=23,max_units=29,bold=True)
        for k,tool in [('curl','Claude Code'),('dmg','Ollama'),('npm','Gemini CLI')]:
            text(L(k),x=48,size=21,max_units=29);text('→ '+tool,x=48,size=22,max_units=29,bold=True);y+=10
        left_end=y
        y=start
        text(L('after'),x=536,size=23,max_units=29,bold=True)
        text('Homebrew',x=536,size=26,max_units=29,bold=True)
        text('brew upgrade',x=536,size=22,max_units=29,bold=True)
        text('↓',x=536,size=26)
        for tool in ['Claude Code','Ollama','Gemini CLI']:text(tool,x=536,size=22,max_units=29)
        y=max(left_end,y,start+390)+28
    elif index==1:
        for label,value in [('OpenCode',.5),('uv',1.6),('llama.cpp',1.6),('Codex',1.8),('Claude Code',3.5),('Hermes Agent',6.7),('OpenClaw',8),('Ollama',25),('Gemini CLI',26.8)]:
            bar(label,value,30,f'{value:.1f} '+L('hours'))
        text(L('delay-note'),size=18,max_units=90)
    elif index==2:
        text('■ '+L('core')+' · ■ '+L('tap')+' · □ '+L('none'),size=19,max_units=85)
        groups=[('agents','8 / 8',[(x,'core') for x in ['OpenClaw','DeepSeek Harness','Hermes Agent','OpenCode','Claude Code','Codex','Gemini CLI','Pi']]),('models','3 / 3',[(x,'core') for x in ['Ollama','llama.cpp','Whisper']]),('other','6 / 12',[('cc-switch','core'),('spec-kit','core'),(L('desktop'),'core'),('Open Design','core'),('Orca','tap'),('VoiceStudio','tap')]+[(x,'none') for x in ['claw-code','Stable Diffusion WebUI','Graphify','MoneyPrinterTurbo','Paperclip','RuView']])]
        for group,count,projects in groups:
            y+=20;text(L(group)+' · '+count,bold=True)
            for project,status in projects:
                text(('□ ' if status=='none' else '■ ')+project+' · '+L(status),size=20,color={'core':'#275fa4','tap':'#6250d6','none':'#637388'}[status],max_units=85)
        text(L('coverage-note'),size=18,max_units=90)
    elif index==3:
        for k,v in [('star-low',88),('star-mid',126),('star-high',72),('star-top',11)]:bar(L(k),v,140,str(v))
        text(L('packages'),size=18);text(L('stars-note'),size=18,max_units=90)
    elif index==4:
        for label,v in [('Codex',351138),('uv',206718),('Ollama',62453),('Claude Code',58378),('OpenCode',45393),('llama.cpp',35373)]:bar(label,v,360000,f'{v:,}')
        text(L('installs-note'),size=18,max_units=90)
    elif index==5:
        for k in ['main','updates','command']:
            chunks=wrap(L(k),65);height=max(100,len(chunks)*34+32)
            items.append(f'<rect x="28" y="{y-20}" width="944" height="{height}" rx="12" fill="#f4f7fb" stroke="#91a3ba" stroke-dasharray="8 5"/>')
            y+=15;text(L(k),x=48,size=24,max_units=65);y+=height-(len(chunks)*36+15)+18
        text(L('screens-note'),size=18,max_units=90)
    elif index==6:
        for k in ['new-system','apps-only','advanced','terminal']:
            y+=12;text(L(k),size=24,max_units=65,bold=True)
        y+=15;text(L('choice-note'),size=18,max_units=90)
    height=int(y+22)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" lang="{lang}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(prompt)}</desc><rect width="1000" height="{height}" rx="14" fill="#ffffff"/><g font-family="Arial, Noto Sans, Noto Sans Arabic, PingFang SC, Microsoft YaHei, sans-serif">'+''.join(items)+'</g></svg>\n'
    filename=name+'.'+lang+'.svg';(ASSETS/filename).write_text(svg)
    return filename,prompt

ASSETS.mkdir(parents=True,exist_ok=True)
assets=[]
for lang in LANGS:
    title=trans(lang,TITLE); description=trans(lang,DESCRIPTION)
    output=[]; in_code=False
    for line in lines:
        if line.startswith('```'): in_code=not in_code; output.append(line);continue
        if in_code:
            output.append(line.replace('名字','NAME') if lang!='zh' else line);continue
        if line.startswith('FIGURETOKEN'):
            index=int(line[-2:])-1;filename,prompt=make_svg(lang,index)
            alt=prompt.replace('\\','\\\\').replace('[','\\[').replace(']','\\]').replace('\n',' ')
            output.append(f'![{alt}](../../assets/blog/{SLUG}/{filename})')
            assets.append({'file':filename,'lang':lang,'figure':index+1,'prompt':prompt})
        else:
            translated=trans(lang,line) if line in translate_lines else line
            translated=re.sub(r'\]\s+\(', '](', translated)
            # Keep original Markdown syntax even if the translation service changes spacing.
            if line.startswith('## '): translated='## '+re.sub(r'^#+\s*','',translated)
            if line.startswith('- '): translated='- '+re.sub(r'^[-•]\s*','',translated)
            if line.startswith('|'):
                translated='| '+translated.strip().strip('|').strip()+' |'
                if translated.count('|')!=line.count('|'): raise ValueError('Damaged table row: '+lang+' '+translated)
            output.append(translated)
    front={'title':title,'description':description,'pubDate':'2026-11-11','tags':['Homebrew',trans(lang,'AI 工具'),'macOS'],'lang':lang,'translationKey':SLUG,'translationStatus':'original' if lang=='zh' else 'machine','draft':False}
    metadata='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in front.items())+'\n---\n\n'
    (CONTENT/(SLUG+'.'+lang+'.md')).write_text(metadata+'\n'.join(output).strip()+'\n')
old=CONTENT/(SLUG+'.md')
if old.exists():old.unlink()
(ASSETS/'manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
manifest={
 'slug':SLUG,'importedAt':'2026-11-11','sourceLanguage':'zh','languages':LANGS,
 'originalFiles':[{'file':f,'sha256':hashlib.sha256((ARCHIVE/f).read_bytes()).hexdigest()} for f in ['source.html','source.zh.md']],
 'sourcePaths':['../a1/Homebrew-AI工具箱-成品.html','../a1/Homebrew-AI工具箱-成品-haiku.md'],
 'displaySource':'src/content/blog/homebrew-ai-toolbox.<lang>.md',
 'translation':{'method':'Google Translate via public translation endpoint, cached; agent corrections to metadata, chart labels and table structure; not human reviewed','cache':'translations.json','preservation':'Every source paragraph, list, table, link and code block retained; code/URLs protected during translation.'},
 'figures':{'countPerLanguage':7,'format':'native SVG','localizedAssets':42,'method':'Redrawn from archived chart data. No HTML foreignObject or screenshots fabricated. Screenshot placeholders remain visibly labeled.','prompts':'src/assets/blog/homebrew-ai-toolbox/manifest.json'},
 'editorialPending':['Original fact-check markers retained and translated.','Original three missing product screenshots retained as one localized placeholder figure.'],
 'rebuild':'python3 scripts/import_homebrew.py (offline); --translate explicitly enables missing network translations'
}
(ARCHIVE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Drop superseded cache schema entries; keep only current reproducible translations.
valid_keys={cache_key(lang,t) for lang in LANGS[1:] for t in needed_texts(lang)}
cache={k:v for k,v in cache.items() if k in valid_keys}
CACHE_PATH.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
print('Generated six Markdown articles and 42 localized SVG assets.',flush=True)
