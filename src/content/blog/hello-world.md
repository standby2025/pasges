---
title: 你好,世界:这个博客怎么用
description: 一篇示例文章,演示 frontmatter、代码块、引用和表格,写自己的文章时可以直接删掉。
pubDate: 2026-11-10
tags: [说明]
---

这是模板自带的示例文章。新文章放在 `src/content/blog/` 下,一篇一个 `.md` 或 `.mdx` 文件,文件名即 URL。

## 文章头信息

```yaml
---
title: 标题
description: 一句话摘要,会显示在列表页
pubDate: 2026-11-10
updatedDate: 2026-11-20   # 可选
tags: [标签一, 标签二]      # 可选
draft: true               # 可选,true 时不会发布
---
```

## 代码与引用

```python
def greet(name: str) -> str:
    return f"你好,{name}"
```

> 引用块会用左侧竖线标出,适合放原文摘录。

| 能力 | 说明 |
| --- | --- |
| 明暗主题 | 跟随系统 |
| RSS | `/rss.xml` |
