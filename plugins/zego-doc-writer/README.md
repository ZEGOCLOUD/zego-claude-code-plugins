# write-zego-docs 插件

ZEGO 技术文档写作助手，提升文档写作效率。

## 目录结构

```
write-zego-docs/
├── plugin.json       # 插件配置文件
├── commands/         # Slash 命令
├── skills/           # 技能（可被多个 agent 调用的可复用能力）
├── agents/           # 子代理（负责特定类型的完整任务）
└── mcp/              # MCP 服务器配置
```

## 架构设计

### Skills vs Agents 职责划分

本插件采用 **Skills（技能）+ Agents（子代理）** 的分层架构：

#### Skills - 可复用的原子能力

**定义**：单一、具体的检查或操作能力，可被多个 agent 或主 agent 调用。

**特点**：
- 专注于单一职责
- 高度可复用
- 无状态或轻状态
- 接收明确输入，返回明确输出

**示例 Skills**：
| Skill 名称 | 功能描述 | 可被调用者 |
|-----------|---------|-----------|
| `link-check` | 检查文档中的链接是否有效 | 所有 reviewer agents |
| `content-accuracy-check` | 检查内容准确性和完整性 | 所有 reviewer agents |
| `code-syntax-check` | 代码语法和格式检查 | 包含代码的文档 reviewers |
| `image-check` | 图片存在性和格式检查 | 所有 reviewer agents |
| `terminology-consistency-check` | 术语一致性检查 | 所有 reviewer agents |
| `dependency-check` | 依赖包版本和可用性检查 | run-demo reviewers |
| `code-runnable-check` | 示例代码可运行性验证 | run-demo reviewers |

#### Agents - 特定类型的任务处理器

**定义**：负责特定类型文档的完整审核或处理任务，可组合调用多个 skills。

**特点**：
- 面向特定文档类型
- 有明确的工作流程
- 可组合多个 skills
- 具备决策逻辑

**示例 Agents**：
| Agent 名称 | 负责文档类型 | 调用的 Skills |
|-----------|-------------|--------------|
| `quick-start-reviewer` | 快速开始文档 | link-check, content-accuracy-check, code-syntax-check |
| `run-demo-reviewer` | 跑通示例代码文档 | code-runnable-check, dependency-check, content-accuracy-check |
| `feature-doc-reviewer` | 功能说明文档 | link-check, content-accuracy-check, image-check |
| `release-note-reviewer` | Release Notes | link-check, terminology-consistency-check |
| `server-api-reviewer` | 服务端 API 文档 | link-check, param-completeness-check, content-accuracy-check |
| `client-api-reviewer` | 客户端 API 文档 | link-check, param-completeness-check, code-syntax-check |

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      文档审核主任务                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   遍历产品文档    │
                    │   分类文档类型    │
                    └─────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 快速开始文档     │ │ 示例代码文档     │ │ API 文档        │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│quick-start      │ │run-demo         │ │api-doc          │
│reviewer agent   │ │reviewer agent   │ │reviewer agent   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│link-check skill  │ │code-runnable    │ │link-check skill  │
│content-accuracy  │ │dependency-check │ │param-completeness│
│code-syntax       │ │content-accuracy │ │content-accuracy  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 架构优势

1. **复用性** - 如 `link-check` 等通用技能可被所有 reviewer 复用，避免重复实现
2. **职责清晰** - 每个 agent 专注一种文档类型，每个 skill 专注一种检查
3. **易于维护** - 修改某个检查逻辑只需改对应 skill，影响范围可控
4. **可扩展性** - 新增文档类型只需创建新 agent，组合现有 skills 即可
5. **并行处理** - 不同类型文档可分发给多个 agents 并行处理，提升效率

## 本地调试

```bash
claude --plugin-dir ./claude/plugins/write-zego-docs
```

## 功能规划

### Commands (Slash 命令)
- `/z-review-docs` - 检查文档质量
- `/new-doc` - 创建新文档
- `/format-doc` - 格式化文档
- `/check-links` - 检查文档链接
- `/translate-doc` - 翻译文档
- `/insert-snippet` - 插入代码片段
- 更多...

### Skills (技能)
- 文档结构分析
- 内容质量检查
- 自动生成目录
- 术语一致性检查
- 更多...

### Agents (子代理)
- 文档翻译助手
- 文档重构助手
- 迁移文档助手
-

### MCP Servers
- ZEGO API 文档查询
- 代码片段管理
- 更多...

## 开发说明

逐步添加功能，每个功能独立开发和测试。
