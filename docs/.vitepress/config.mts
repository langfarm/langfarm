import { defineConfig } from 'vitepress'
import markdownItTextualUml from 'markdown-it-textual-uml'
import { zh_theme_config, en_theme_config } from './theme-config.mts'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Langfarm",
  description: "Langfarm 是 LLM 的应用 DevOps 平台",
  sitemap: {
    hostname: 'https://langfarm.github.io'
  },
  markdown: {
    lineNumbers: true
    , config: (md) => {
      // 使用更多的 Markdown-it 插件！
      md.use(markdownItTextualUml);
    }
  },
  ignoreDeadLinks: [
    // ignore all localhost links
    /^https?:\/\/localhost/,
  ],
    locales: {
    root: {
      label: '简体中文',
      lang: 'zh',
      themeConfig: zh_theme_config,
    },
    en: {
      label: 'English',
      lang: 'en', // 可选，将作为 `lang` 属性添加到 `html` 标签中
      themeConfig: en_theme_config,
      // 其余 locale 特定属性...
    }
  },
  themeConfig: {
    lastUpdated: {
      formatOptions: {
        dateStyle: 'medium',
        timeStyle: 'medium',
      },
    },
    outline: {
      level: [2, 4]
    },

    search: {
      provider: 'local',
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/langfarm' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024-present Langfarm'
    }
  }
})
