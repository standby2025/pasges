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
