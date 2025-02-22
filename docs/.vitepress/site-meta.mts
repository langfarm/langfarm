const nav = [
    { text: '首页', link: '/' },
    { text: '文档', link: '/intro' }
]

const sidebar = [
    {
        text: '介绍',
        link: '/intro',
    },
    {
        text: '贡献',
        items: [
            { text: '贡献指南', link: '/CONTRIBUTING' },
            { text: '贡献公约', link: '/CODE_OF_CONDUCT' },
        ]
    },

]

const en_nav = [
    { text: 'Home', link: '/en' },
    { text: 'Docs', link: '/en/intro' }
]

const en_sidebar = [
    {
        text: 'Introduction',
        link: '/en/intro',
    },
    {
        text: 'Contribute',
        items: [
            { text: 'Contributing', link: '/en/CONTRIBUTING' },
            { text: 'Code of Conduct', link: '/en/CODE_OF_CONDUCT' },
        ]
    },
]


export {nav, sidebar, en_nav, en_sidebar}