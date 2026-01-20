# ZEGO Assistant

ZEGO产品集成和问题排查智能助手，帮助开发者快速接入ZEGO产品（RTC/IM/AIAgent）并提供全方位的技术支持。

## 功能特性

### 🤖 智能集成向导（Agents）
- **RTC集成向导**：实时音视频产品交互式集成助手
- **IM集成向导**：即时通讯产品交互式集成助手
- **AIAgent集成向导**：AI Agent产品交互式集成助手

### 📚 知识库（Skills）
提供6大通用知识模块，覆盖跨产品的集成和问题排查：

1. **服务端集成**：Token生成、服务端API调用、认证流程
2. **客户端集成**：SDK初始化、登录流程、事件处理
3. **配置检查**：AppID、权限、网络配置验证
4. **性能诊断**：卡顿、延迟、音视频质量问题诊断
5. **平台特定问题**：iOS/Android/Web/Flutter平台特定解决方案
6. **问题排查**：错误码、日志分析、调试技巧

### 🎯 快速命令（Commands）
- `/check-zego-config`：检查项目中ZEGO配置的正确性和完整性
- `/diagnose-zego-issue`：交互式诊断ZEGO相关问题

### 📖 文档服务（MCP）
连接ZEGO文档服务，提供实时文档查询能力（即将推出）

## 安装

### 从Marketplace安装（即将推出）
```bash
/plugin marketplace add https://github.com/ZEGOCLOUD/zego-claude-code-plugins
/plugin install zego-assistant
```

### 本地安装
```bash
# 将插件复制到Claude Code插件目录
cp -r plugins/zego-assistant ~/.claude/plugins/
```

## 快速开始

### 1. 集成ZEGO RTC产品
直接提问：
```
如何集成ZEGO的RTC SDK到我的iOS项目？
```

或使用命令：
```
/integrate-rtc
```

### 2. 检查配置
```bash
/check-zego-config
```

### 3. 诊断问题
```bash
/diagnose-zego-issue
```

## 配置

创建用户配置文件 `.claude/zego-assistant.local.md`：

```yaml
---
default_app_id: "your_app_id_here"
server_environment: "production"  # production | staging | test
primary_platform: "ios"           # ios | android | web | flutter
log_level: "info"                 # debug | info | warn | error
---
```

## 插件结构

```
zego-assistant/
├── .claude-plugin/
│   └── plugin.json          # 插件清单
├── commands/                 # 快速命令
│   ├── check-zego-config.md
│   └── diagnose-zego-issue.md
├── agents/                   # 集成向导
│   ├── rtc-integration-agent.md
│   ├── im-integration-agent.md
│   └── aiagent-integration-agent.md
├── skills/                   # 知识库
│   ├── server-integration/
│   ├── client-integration/
│   ├── config-checker/
│   ├── performance-diagnosis/
│   ├── platform-specific-issues/
│   └── troubleshooting/
└── .mcp.json                # 文档服务配置
```

## 使用示例

### 示例1：RTC集成
**用户**：帮我集成ZEGO RTC到我的Android项目

**Agent**：
1. 询问项目信息（技术栈、业务场景）
2. 引导添加SDK依赖
3. 引导配置权限
4. 引导初始化代码
5. 提供测试验证建议

### 示例2：性能问题诊断
**用户**：我的RTC通话很卡，画质也不清晰

**Claude**：（调用performance-diagnosis Skill）
1. 检查网络环境
2. 分析性能指标（码率、帧率、丢包率）
3. 提供优化建议
4. 针对平台调优建议

### 示例3：配置检查
**用户**：/check-zego-config

**Claude**：
1. 扫描配置文件
2. 验证AppID、AppSign
3. 检查权限配置
4. 生成检查报告

## 技术支持

- 官方文档：https://doc-zego.im
- 技术支持：support@zego.im
- 问题反馈：https://github.com/ZEGOCLOUD/zego-claude-code-plugins/issues

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
