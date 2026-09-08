# ZEGO Assistant

ZEGO 产品集成和问题排查智能助手，帮助开发者快速接入 ZEGO 产品（RTC / ZIM / AI Agent）并提供全方位的技术支持。

## 功能特性

### 📚 知识库（Skills）
提供 5 大通用知识模块，覆盖跨产品的集成和问题排查：

1. **integrate-zego-product**：客户端 SDK 集成（Express / ZIM / AI Agent / 数字人 / 超级白板），覆盖快速开始、SDK 初始化、事件处理等完整流程
2. **implement-zego-token-on-server**：服务端 Token 生成（多语言示例：Go / Java / Python / Node / PHP / C#）
3. **integrate-zego-server-api**：服务端 API 调用与签名机制
4. **resource-downloader**：下载 ZEGO SDK、示例项目和 Demo
5. **search-zego-doc-fragments**：RAG 检索 ZEGO 文档片段（错误码、API 参数、平台兼容性）

### 📖 文档服务（MCP）
连接 ZEGO 文档服务（`https://doc-ai.zego.im/mcp/`），提供实时文档查询能力，包括产品知识库索引、平台支持列表、文档链接、Token 鉴权说明、服务端签名说明及 RAG 文档搜索。

## 安装

```bash
/plugin marketplace add https://github.com/ZEGOCLOUD/zego-claude-code-plugins
/plugin install zego-assistant@zego-claude-code-plugins
```

安装后即可在当前会话中直接使用（无需重启）。

## 快速开始

直接用自然语言提问即可，例如：

```
如何集成 ZEGO 的 RTC SDK 到我的 iOS 项目？
```

```
帮我在 Go 服务端实现 ZEGO Token 生成
```

```
错误码 1000001 是什么意思？
```

## 插件结构

```
zego-assistant/
├── .claude-plugin/
│   └── plugin.json          # 插件清单
├── skills/                   # 知识库
│   ├── integrate-zego-product/
│   ├── implement-zego-token-on-server/
│   ├── integrate-zego-server-api/
│   ├── resource-downloader/
│   └── search-zego-doc-fragments/
└── .mcp.json                 # ZEGO 文档服务 MCP 配置
```

## 技术支持

- 官方文档：https://doc-zego.im
- 技术支持：support@zego.im
- 问题反馈：https://github.com/ZEGOCLOUD/zego-claude-code-plugins/issues

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
