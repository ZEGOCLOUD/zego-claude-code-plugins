# ZEGO Assistant（已弃用）

> **⚠️ 本插件已被 [zego-integration Agent Skill](https://github.com/ZEGOCLOUD/zego-integration) 取代，本仓库已停止演进。**

自 v2.0.0 起，本插件只包含一个迁移引导 skill，不再提供原有的 5 个 skill 与 ZEGO 文档 MCP 服务。

## 迁移方法

安装新的 zego-integration Skill（一次安装，Claude Code / Codex / Cursor 等工具通用）：

```bash
npx skills add ZEGOCLOUD/zego-integration
```

国内网络一键安装：

```bash
curl -fsSL https://gh-proxy.com/https://raw.githubusercontent.com/ZEGOCLOUD/zego-integration/main/install.sh | bash
```

装好后建议卸载本插件：

```text
/plugin uninstall zego-assistant@zego-claude-code-plugins
/plugin marketplace remove zego-claude-code-plugins
```

## 插件结构

```
zego-assistant/
├── .claude-plugin/
│   └── plugin.json          # 插件清单
└── skills/
    └── zego-integration-migration/  # 迁移引导（唯一 skill）
```

## 技术支持

- 官方文档：https://doc-zh.zego.im
- 使用指引：https://doc-zh.zego.im/ai-coding/using-ai-coding
- 问题反馈：https://github.com/ZEGOCLOUD/zego-claude-code-plugins/issues

## 许可证

MIT License
