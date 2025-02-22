import { nav, sidebar, en_nav, en_sidebar } from './site-meta.mjs'

const zh_theme_config = {
    // https://vitepress.dev/reference/default-theme-config
    nav: nav,
    sidebar: sidebar,
    darkModeSwitchLabel: '主题',
    darkModeSwitchTitle: '切换到深色模式',
    docFooter: {
      next: '下一页',
      prev: '上一页',
    },
    lastUpdated: {
      text: '最后更新于',
    },
    lightModeSwitchTitle: '切换到浅色模式',
    outline: {
      label: '页面导航',
    },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',

    search: {
      options: {
        translations: {
          button: {
            buttonText: '搜索文档',
            buttonAriaLabel: '搜索文档'
          },
          modal: {
            noResultsText: '无法找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: {
              selectText: '选择',
              navigateText: '切换',
              closeText: '关闭'
            }
          }
        }
      }
    }
  }

const en_theme_config = {
    nav: en_nav,
    sidebar: en_sidebar,
    darkModeSwitchLabel: 'theme',
    darkModeSwitchTitle: 'Switch to dark mode',
    docFooter: {
      next: 'Next page',
      prev: 'Previous page',
    },
    lastUpdated: {
      text: 'Last updated on',
    },
    lightModeSwitchTitle: 'Switch to light mode',
    outline: {
      label: 'Page navigation',
    },
    returnToTopLabel: 'Back to the top',
    sidebarMenuLabel: 'menu',

    search: {
      options: {
        translations: {
          button: {
            buttonText: 'Search document',
            buttonAriaLabel: 'Search document'
          },
          modal: {
            noResultsText: 'No results could be found',
            resetButtonTitle: 'Clear query criteria',
            footer: {
              selectText: 'Select',
              navigateText: 'Toggle',
              closeText: 'Close'
            }
          }
        }
      }
    }
  }

export {zh_theme_config, en_theme_config}
