# 文档路径查找指引

本文件提供在 ZEGO 文档仓库中查找相关文档的策略和命令。

## 前置步骤：获取文档路径

在搜索文档之前，首先需要从 `references/products-platforms.md` 中获取对应产品和平台的文档路径。

### 获取路径流程

1. 用户选择产品（如"实时音视频"）
2. 用户选择平台（如"Android Java"）
3. 从 `products-platforms.md` 的表格中查找对应行，获取 `文档路径` 值
4. 如果有 `客户端 API 路径` 列，一并记录

### 示例

假设用户选择：
- 产品：实时音视频 (Video Call)
- 平台：Android Java

从 `products-platforms.md` 查得：
- 文档路径：`core_products/real-time-voice-video/zh/android-java`
- 客户端 API 路径：`client-sdk/api-reference`

后续搜索将基于这些路径进行。

---

## 文档查找策略

### 1. 使用 Glob 工具查找目录结构

首先使用 Glob 查找文档的目录结构：

```bash
# 查找所有 MDX 文件
Glob "**/*.mdx"

# 查找特定目录下的文档
Glob "**/integration/**/*.mdx"

# 查找快速开始文档
Glob "**/quick-start/**/*.mdx"
Glob "**/quick-start**.mdx"

# 查找客户端 API 文档
Glob "**/client-sdk/api-reference/**/*.mdx"

# 查找服务端 API 文档
Glob "**/server/api-reference/**/*.yaml"
```

### 2. 使用 Grep 工具搜索关键词

使用 Grep 在文档中搜索特定关键词：

```bash
# 搜索产品名称
Grep "实时音视频" --glob "*.mdx"
Grep "ZEGO Express" --glob "*.mdx"

# 搜索功能相关
Grep "Token 鉴权" --glob "*.mdx"
Grep "登录房间" --glob "*.mdx"

# 搜索 API 名称
Grep "createEngine" --glob "*.mdx"
Grep "loginRoom" --glob "*.mdx"
```

### 3. 搜索配置文件

查找侧边栏配置文件，了解文档结构：

```bash
# 搜索 sidebars.json
Glob "**/sidebars.json"

# 搜索 Docuo 配置
Glob "**/.docuo/**/*"
Glob "**/docu.json"
```

## 文档内容读取策略

### 按优先级读取

读取文档时按以下优先级：

1. **集成指南** - 了解如何引入 SDK
2. **快速开始** - 了解最小可用示例
3. **API 文档** - 了解具体接口
4. **Token 说明** - 了解鉴权机制（如需要）
5. **功能文档** - 了解特定功能实现

### 读取策略

**使用 Read 工具读取找到的文档**：

```bash
# 读取单个文档
Read /path/to/document.mdx

# 读取多个文档（并行）
Read /path/to/doc1.mdx
Read /path/to/doc2.mdx
Read /path/to/doc3.mdx
```

**只读取需要的文档**：
- 如果只需要 Android 文档，不要读取 iOS 文档
- 如果只需要快速开始，不要读取完整 API 文档
- 根据用户选择精准读取
- 客户端 API 文档通常非常大，读取时可以先搜索到关键行，然后只读取前后20行内容
- 服务端 API 如果有 yaml 格式的文件则优先读取，如果整个目录都没有yaml文件才读取mdx文件

## 关键信息提取

从文档中提取以下关键信息示例：

### SDK 引入

**Android (Gradle)**:
```gradle
implementation 'im.zego:express-video:x.y.z'
```

**iOS (CocoaPods)**:
```ruby
pod 'ZegoExpressEngine', '~> x.y.z'
```

**Web (npm)**:
```bash
npm install zego-express-engine-webrtc
```

### 初始化代码

查找引擎创建方法：
- `[ZegoExpressEngine createEngineWithProfile:profile eventHandler:self]`
- `ZegoExpressEngine.createEngine(profile, null)`
- `new ZegoExpressEngine(appID, server)`

提取参数：
- AppID
- AppSign // 已不推荐
- 场景 (scenario)
- 回调 (eventHandler)

### 方法调用

查找房间相关方法：
- `loginRoom()` - 加入房间
- `logoutRoom()` - 离开房间

提取参数：
- String roomID
- ZegoUser user
- ZegoRoomConfig config
- IZegoRoomLoginCallback callback


### Token 相关

查找 Token 相关内容：
- Token 生成算法版本 (04)
- Token 生成服务端接口
- Token 使用客户端接口