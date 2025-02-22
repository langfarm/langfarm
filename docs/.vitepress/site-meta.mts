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
        text: '快速开始',
        link: '/quick-start',
    },
    {
        text: '数据入湖',
        items: [
            { text: '快速开始', link: '/streaming/quick-start' },
        ]
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
        text: 'Quick Start',
        link: '/en/quick-start',
    },
    {
        text: 'Lakehouse',
        items: [
            { text: 'Quick Start', link: '/en/streaming/quick-start' },
        ]
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