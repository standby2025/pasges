import { SITE_TITLE, SITE_DESCRIPTION } from '../consts';
export const languages = ['zh', 'en', 'fr', 'es', 'ru', 'ar'] as const;
export type Language = (typeof languages)[number];
export const languageNames: Record<Language, string> = {
 zh: '中文', en: 'English', fr: 'Français', es: 'Español', ru: 'Русский', ar: 'العربية',
};
export const localeNames: Record<Language, string> = {
 zh: 'zh-CN', en: 'en-US', fr: 'fr-FR', es: 'es-ES', ru: 'ru-RU', ar: 'ar',
};
export const articleUI = {
 zh: { home: '首页', posts: '文章', about: '关于', languages: '文章语言', updated: '更新于', machine: '此版本为机器翻译，尚未经人工校对。数据和待核实标记沿用原文。', original: '中文原文', legacy: '页面已迁移，前往中文版本。' },
 en: { home: 'Home', posts: 'Articles', about: 'About', languages: 'Article language', updated: 'Updated', machine: 'This version is machine translated and has not been human reviewed. Data and pending verification notes follow the original.', original: 'Chinese original', legacy: 'This article has moved.' },
 fr: { home: 'Accueil', posts: 'Articles', about: 'À propos', languages: 'Langue de l’article', updated: 'Mis à jour', machine: 'Cette version est une traduction automatique non relue par une personne. Les données et les mentions à vérifier sont celles du texte original.', original: 'Original chinois', legacy: 'Cet article a été déplacé.' },
 es: { home: 'Inicio', posts: 'Artículos', about: 'Acerca de', languages: 'Idioma del artículo', updated: 'Actualizado', machine: 'Esta versión es una traducción automática sin revisión humana. Los datos y las notas pendientes de verificación proceden del original.', original: 'Original en chino', legacy: 'Este artículo se ha trasladado.' },
 ru: { home: 'Главная', posts: 'Статьи', about: 'О блоге', languages: 'Язык статьи', updated: 'Обновлено', machine: 'Это машинный перевод без проверки человеком. Данные и пометки о необходимости проверки сохранены из оригинала.', original: 'Китайский оригинал', legacy: 'Статья перемещена.' },
 ar: { home: 'الرئيسية', posts: 'المقالات', about: 'حول', languages: 'لغة المقال', updated: 'آخر تحديث', machine: 'هذه ترجمة آلية لم يراجعها إنسان. البيانات وملاحظات التحقق المعلقة مأخوذة من النص الأصلي.', original: 'الأصل الصيني', legacy: 'تم نقل هذه المقالة.' },
} satisfies Record<Language, Record<string, string>>;

export const themeUI = {
 zh: { label: '配色', random: '每次随机', paper: '暖纸 · 米白', mist: '晴雾 · 蓝灰', forest: '松林 · 浅绿', rose: '蔷薇 · 淡粉', night: '深海 · 夜色' },
 en: { label: 'Colors', random: 'Random on each visit', paper: 'Warm paper', mist: 'Blue mist', forest: 'Forest', rose: 'Rose', night: 'Deep sea' },
 fr: { label: 'Couleurs', random: 'Aléatoire à chaque visite', paper: 'Papier chaud', mist: 'Brume bleue', forest: 'Forêt', rose: 'Rose', night: 'Océan profond' },
 es: { label: 'Colores', random: 'Aleatorio en cada visita', paper: 'Papel cálido', mist: 'Niebla azul', forest: 'Bosque', rose: 'Rosa', night: 'Mar profundo' },
 ru: { label: 'Цвета', random: 'Случайно при входе', paper: 'Тёплая бумага', mist: 'Голубой туман', forest: 'Лес', rose: 'Роза', night: 'Глубокое море' },
 ar: { label: 'الألوان', random: 'عشوائي عند كل زيارة', paper: 'ورق دافئ', mist: 'ضباب أزرق', forest: 'غابة', rose: 'وردي', night: 'بحر عميق' },
} satisfies Record<Language, Record<string, string>>;

export const siteUI = {
 zh: { title: SITE_TITLE, description: SITE_DESCRIPTION, recent: '最近更新', all: '查看全部文章', empty: '还没有文章。', archive: '全部文章，按时间倒序。', aboutDescription: '关于这个博客和它的作者。', aboutText: '在这里介绍你自己：你是谁，做什么，这个博客写什么、写给谁。', contactText: '也可以放上联系方式、其他平台的账号链接。', author: '你的名字', language: '语言', navigation: '主导航', rss: '订阅 RSS' },
 en: { title: SITE_TITLE, description: 'Explain what I learn clearly. Write slowly, write thoughtfully.', recent: 'Latest articles', all: 'View all articles', empty: 'No articles yet.', archive: 'All articles, newest first.', aboutDescription: 'About this blog and its author.', aboutText: 'Introduce yourself here: who you are, what you do, and what this blog covers and for whom.', contactText: 'You can also add contact details and links to your other profiles.', author: 'Your name', language: 'Language', navigation: 'Main navigation', rss: 'Subscribe via RSS' },
 fr: { title: SITE_TITLE, description: 'Expliquer clairement ce que j’apprends. Écrire avec soin, à mon rythme.', recent: 'Derniers articles', all: 'Voir tous les articles', empty: 'Aucun article pour le moment.', archive: 'Tous les articles, du plus récent au plus ancien.', aboutDescription: 'À propos de ce blog et de son auteur.', aboutText: 'Présentez-vous ici : qui vous êtes, ce que vous faites, les sujets et le public de ce blog.', contactText: 'Vous pouvez aussi ajouter vos coordonnées et des liens vers vos autres profils.', author: 'Votre nom', language: 'Langue', navigation: 'Navigation principale', rss: 'S’abonner par RSS' },
 es: { title: SITE_TITLE, description: 'Explicar con claridad lo que aprendo. Escribir sin prisas y con cuidado.', recent: 'Artículos recientes', all: 'Ver todos los artículos', empty: 'Todavía no hay artículos.', archive: 'Todos los artículos, del más reciente al más antiguo.', aboutDescription: 'Sobre este blog y su autor.', aboutText: 'Preséntate aquí: quién eres, a qué te dedicas y qué temas trata este blog y para quién.', contactText: 'También puedes añadir datos de contacto y enlaces a tus otros perfiles.', author: 'Tu nombre', language: 'Idioma', navigation: 'Navegación principal', rss: 'Suscribirse por RSS' },
 ru: { title: SITE_TITLE, description: 'Понятно объяснять то, что узнаю. Писать вдумчиво и не спеша.', recent: 'Последние статьи', all: 'Все статьи', empty: 'Статей пока нет.', archive: 'Все статьи, начиная с новых.', aboutDescription: 'Об этом блоге и его авторе.', aboutText: 'Расскажите здесь о себе: кто вы, чем занимаетесь, о чём и для кого этот блог.', contactText: 'Также можно добавить контакты и ссылки на другие профили.', author: 'Ваше имя', language: 'Язык', navigation: 'Основная навигация', rss: 'Подписаться на RSS' },
 ar: { title: SITE_TITLE, description: 'أشرح ما أتعلمه بوضوح، وأكتب بتأنٍ وعناية.', recent: 'أحدث المقالات', all: 'عرض جميع المقالات', empty: 'لا توجد مقالات بعد.', archive: 'جميع المقالات، من الأحدث إلى الأقدم.', aboutDescription: 'حول هذه المدونة وكاتبها.', aboutText: 'عرّف بنفسك هنا: من أنت، وماذا تعمل، وما موضوع هذه المدونة ولمن تكتب.', contactText: 'يمكنك أيضاً إضافة معلومات الاتصال وروابط حساباتك الأخرى.', author: 'اسمك', language: 'اللغة', navigation: 'التنقل الرئيسي', rss: 'الاشتراك عبر RSS' },
} satisfies Record<Language, Record<string, string>>;
