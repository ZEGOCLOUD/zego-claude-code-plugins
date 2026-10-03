# ZEGO Claude Code Plugins

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README_EN.md) [![中文](https://img.shields.io/badge/lang-中文-red.svg)](README.md)

> **⚠️ 本仓库已停止演进。** `zego-assistant` 插件已被独立的 **[zego-integration Agent Skill](https://github.com/ZEGOCLOUD/zego-integration)** 取代，请直接安装新 Skill（一次安装，Claude Code / Codex / Cursor 等工具通用）：
>
> ```bash
> npx skills add ZEGOCLOUD/zego-integration
> ```
>
> 国内网络一键安装：
>
> ```bash
> curl -fsSL https://gh-proxy.com/https://raw.githubusercontent.com/ZEGOCLOUD/zego-integration/main/install.sh | bash
> ```

## 现状说明

自 v2.0.0 起，本仓库的 `zego-assistant` 插件不再提供原有的 5 个 skill 与 ZEGO 文档 MCP 服务，仅保留一个**迁移引导 skill**：已安装旧插件的用户在提出 ZEGO 相关任务时，agent 会引导安装新的 zego-integration Skill。原有的 MCP 工作流（`search_zego_docs`、`get_doc_links` 等）已移除。

已安装旧插件的用户建议在新 Skill 装好后卸载旧插件：

```text
/plugin uninstall zego-assistant@zego-claude-code-plugins
/plugin marketplace remove zego-claude-code-plugins
```

## 仍想安装本插件（仅获得迁移引导）

```bash
/plugin marketplace add https://github.com/ZEGOCLOUD/zego-claude-code-plugins
/plugin install zego-assistant@zego-claude-code-plugins
```

## 为什么迁移

新的 zego-integration Skill 把官方文档仓库缓存到本地、由 agent 直接检索源文件，替代了原来的 RAG + MCP 方案；不再依赖 MCP 服务，覆盖错误码、API 参数、Token/签名、SDK 下载与场景最佳实践，且与具体编程工具解耦。详见 [使用 AI Coding](https://doc-zh.zego.im/ai-coding/using-ai-coding)。

## 许可证

MIT License

## 联系方式

- 问题反馈: [GitHub Issues](https://github.com/ZEGOCLOUD/zego-claude-code-plugins/issues)
- 邮件: docuo@zego.im
