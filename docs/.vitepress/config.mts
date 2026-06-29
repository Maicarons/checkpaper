import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'CheckPaper',
  description: 'AI-Powered Academic Paper Verification Agent',
  lastUpdated: true,

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' }],
  ],

  locales: {
    root: {
      label: 'English',
      lang: 'en-US',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/guide/introduction', activeMatch: '/guide/' },
          { text: 'API Reference', link: '/api/', activeMatch: '/api/' },
          { text: 'Developer', link: '/developer/contributing', activeMatch: '/developer/' },
          {
            text: 'v0.1.0',
            items: [
              { text: 'Changelog', link: '/changelog' },
              { text: 'Roadmap', link: 'https://github.com/Maicarons/checkpaper/blob/main/plan.md' },
            ]
          },
        ],
        sidebar: {
          '/guide/': [
            {
              text: 'Getting Started',
              items: [
                { text: 'Introduction', link: '/guide/introduction' },
                { text: 'Quick Start', link: '/guide/getting-started' },
                { text: 'Features', link: '/guide/features' },
                { text: 'Deployment', link: '/guide/deployment' },
              ]
            }
          ],
          '/api/': [
            {
              text: 'API Reference',
              items: [
                { text: 'Overview', link: '/api/' },
                { text: 'Documents', link: '/api/documents' },
                { text: 'Validation', link: '/api/validation' },
                { text: 'Reports', link: '/api/reports' },
                { text: 'Health', link: '/api/health' },
                { text: 'MCP Tools', link: '/api/mcp-tools' },
              ]
            }
          ],
          '/developer/': [
            {
              text: 'Developer Guide',
              items: [
                { text: 'Contributing', link: '/developer/contributing' },
                { text: 'Architecture', link: '/developer/architecture' },
                { text: 'Configuration', link: '/developer/configuration' },
                { text: 'Testing', link: '/developer/testing' },
              ]
            }
          ],
        },
        editLink: {
          pattern: 'https://github.com/Maicarons/checkpaper/edit/main/docs/:path',
          text: 'Edit this page on GitHub'
        },
        footer: {
          message: 'Released under the GNU Affero General Public License v3.0.',
          copyright: 'Copyright © 2024-2026 CheckPaper Team'
        },
        outline: {
          label: 'Page Navigation',
          level: [2, 3]
        },
        lastUpdated: {
          text: 'Last updated',
        },
        docFooter: {
          prev: 'Previous',
          next: 'Next'
        },
      }
    },

    zh: {
      label: '中文',
      lang: 'zh-CN',
      title: 'CheckPaper',
      description: 'AI 驱动的学术论文验证智能体系统',
      themeConfig: {
        nav: [
          { text: '指南', link: '/zh/guide/introduction', activeMatch: '/zh/guide/' },
          { text: 'API 参考', link: '/zh/api/', activeMatch: '/zh/api/' },
          { text: '开发者', link: '/zh/developer/contributing', activeMatch: '/zh/developer/' },
          {
            text: 'v0.1.0',
            items: [
              { text: '更新日志', link: '/zh/changelog' },
              { text: '路线图', link: 'https://github.com/Maicarons/checkpaper/blob/main/plan.md' },
            ]
          },
        ],
        sidebar: {
          '/zh/guide/': [
            {
              text: '入门指南',
              items: [
                { text: '项目简介', link: '/zh/guide/introduction' },
                { text: '快速开始', link: '/zh/guide/getting-started' },
                { text: '功能特性', link: '/zh/guide/features' },
                { text: '部署', link: '/zh/guide/deployment' },
              ]
            }
          ],
          '/zh/api/': [
            {
              text: 'API 参考',
              items: [
                { text: '概览', link: '/zh/api/' },
                { text: '文档管理', link: '/zh/api/documents' },
                { text: '验证任务', link: '/zh/api/validation' },
                { text: '报告管理', link: '/zh/api/reports' },
                { text: '健康检查', link: '/zh/api/health' },
                { text: 'MCP 工具', link: '/zh/api/mcp-tools' },
              ]
            }
          ],
          '/zh/developer/': [
            {
              text: '开发者指南',
              items: [
                { text: '贡献指南', link: '/zh/developer/contributing' },
                { text: '系统架构', link: '/zh/developer/architecture' },
                { text: '配置说明', link: '/zh/developer/configuration' },
                { text: '测试', link: '/zh/developer/testing' },
              ]
            }
          ],
        },
        editLink: {
          pattern: 'https://github.com/Maicarons/checkpaper/edit/main/docs/:path',
          text: '在 GitHub 上编辑此页面'
        },
        footer: {
          message: '基于 GNU Affero 通用公共许可证 v3.0 发布。',
          copyright: 'Copyright © 2024-2026 CheckPaper Team'
        },
        outline: {
          label: '页面导航',
          level: [2, 3]
        },
        lastUpdated: {
          text: '最后更新',
        },
        docFooter: {
          prev: '上一篇',
          next: '下一篇'
        },
      }
    },
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'CheckPaper Docs',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Maicarons/checkpaper' }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: 'Search',
            buttonAriaLabel: 'Search'
          },
          modal: {
            noResultsText: 'No results found',
            resetButtonTitle: 'Clear search',
            footer: {
              selectText: 'to select',
              navigateText: 'to navigate',
              closeText: 'to close'
            }
          }
        }
      }
    },
  }
})
