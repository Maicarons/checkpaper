---
layout: home

hero:
  name: CheckPaper
  text: AI 论文验证智能体
  tagline: 利用 AI 技术自动检测学术论文中的格式问题、引用错误、数据真实性等问题，帮助研究者提升论文质量。
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/guide/introduction
    - theme: alt
      text: GitHub 仓库
      link: https://github.com/Maicarons/checkpaper

features:
  - icon: 📄
    title: 多格式支持
    details: 支持 PDF、Word (.docx)、LaTeX 格式的论文解析和验证，自动识别文件格式并提取结构化数据。
  - icon: 🔍
    title: 格式检查
    details: 检查标题层级、编号规范、字体字号一致性、页面布局以及目录与正文的对应关系。
  - icon: 📊
    title: 图表引用检查
    details: 交叉验证所有图表定义与正文引用，检测"孤儿引用"和"未引用"的图表。
  - icon: 📚
    title: 参考文献引用检查
    details: 验证正文引用与参考文献列表的一致性，检测重复引用、缺失引用和格式不规范问题。
  - icon: ✅
    title: 参考文献验证
    details: 通过 Crossref 和 Semantic Scholar API 验证参考文献的真实性，检查 DOI 有效性、元数据准确性，检测可疑引用。
  - icon: 📈
    title: 数据真实性验证
    details: 验证数据来源、执行 GRIM/SPRITE 统计一致性测试、检查图表数据与正文报告的一致性。
  - icon: 🤖
    title: Agent 智能编排
    details: 基于 OpenAI Agents SDK 和 MCP 协议，专项 Agent 分别处理格式、引用、参考文献和数据验证任务。
  - icon: 📋
    title: 结构化报告
    details: 生成详细的 Markdown 验证报告，问题按严重程度分级（严重、警告、信息），并提供改进建议。
---
