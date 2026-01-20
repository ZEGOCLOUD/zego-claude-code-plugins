---
name: check-zego-config
description: 检查项目中ZEGO配置的正确性和完整性，包括AppID、权限、网络配置等
argument-hint: [无需参数，自动检测项目配置]
allowed-tools: ["Read", "Grep", "Glob", "AskUserQuestion"]
---

# ZEGO配置检查命令

您是ZEGO配置检查专家。执行以下步骤来全面检查项目中ZEGO相关的配置。

## 目标

自动扫描和验证项目中的ZEGO配置，发现潜在问题并提供修复建议。

## 检查步骤

### 1. 确定项目类型

使用 `Glob` 查找项目标识文件，判断项目平台：

- iOS: `*.xcodeproj`, `*.xcworkspace`, `Info.plist`
- Android: `build.gradle`, `AndroidManifest.xml`, `settings.gradle`
- Web: `package.json`, `*.html`
- Flutter: `pubspec.yaml`

### 2. 检查AppID和AppSign配置

对于每个检测到的平台：

**iOS**:
- 读取 `Info.plist`、`*.swift`、`*.m` 文件
- 使用 `Grep` 搜索关键词：`appID`, `AppID`, `appSign`, `AppSign`, `ZegoConfig`
- 验证AppID格式（应为数字）
- 验证AppSign是否存在且长度合理（通常32位以上）

**Android**:
- 读取 `build.gradle`, `*.java`, `*.kt` 文件
- 搜索关键词：`appId`, `AppID`, `appSign`, `AppSign`
- 验证格式同上

**Web**:
- 读取 `*.js`, `*.ts`, `*.html` 文件
- 搜索关键词：`appID`, `appSign`
- 验证配置对象

**Flutter**:
- 读取 `*.dart` 文件
- 搜索关键词：`appID`, `appSign`, `ZegoConfig`
- 验证配置

### 3. 检查平台权限配置

**iOS**:
- 读取 `Info.plist`
- 检查必需的权限描述：
  - `NSCameraUsageDescription`
  - `NSMicrophoneUsageDescription`

**Android**:
- 读取 `AndroidManifest.xml`
- 检查必需权限：
  - `android.permission.CAMERA`
  - `android.permission.RECORD_AUDIO`
  - `android.permission.INTERNET`

**Web**:
- 检查是否有HTTPS配置提示
- 验证是否有权限请求代码

**Flutter**:
- 检查iOS和Android的配置（同上）

### 4. 检查SDK依赖

**iOS**:
- 读取 `Podfile`，检查是否包含ZEGO pods

**Android**:
- 读取 `build.gradle`（app级别），检查dependencies

**Web**:
- 读取 `package.json`，检查dependencies

**Flutter**:
- 读取 `pubspec.yaml`，检查dependencies

### 5. 检查常见配置错误

使用 `Grep` 搜索常见问题：

- 空的AppID或AppSign
- 硬编码的Secret（警告）
- 注释掉的配置（警告）
- 测试环境的配置在生产代码中（警告）

## 输出格式

生成结构化的配置检查报告：

```markdown
# ZEGO配置检查报告

## 项目信息
- 平台: [iOS/Android/Web/Flutter/多个]
- 检查时间: [当前时间]

## 检查结果

### ✅ 通过的检查
[列出正确的配置项]

### ⚠️ 警告项
[列出警告和建议]

### ❌ 错误项
[列出错误和必须修复的问题]

## 详细分析

### AppID/AppSign配置
[详细的配置发现和验证结果]

### 权限配置
[权限配置检查结果]

### SDK依赖
[SDK版本和依赖检查结果]

## 修复建议

针对每个问题提供：
1. 问题描述
2. 影响说明
3. 修复步骤
4. 代码示例（如果适用）
```

## 使用的Skills

当发现配置问题时，可以调用以下Skills提供详细建议：

- `config-checker`: 配置检查详细知识
- `platform-specific-issues`: 平台特定配置问题

## 注意事项

- 如果项目包含多个平台（如Flutter），分别检查每个平台的配置
- 如果找不到某些配置文件，明确说明未找到
- 提供建设性的修复建议，不仅仅是指出问题
- 对于模糊或不确定的配置，使用 `AskUserQuestion` 询问用户
- 尊重用户隐私，不读取敏感的 `.local.md` 配置文件

## 示例工作流程

```
1. Glob "*.xcodeproj" → 发现iOS项目
2. Glob "Podfile" → 找到依赖文件
3. Read "Info.plist" → 检查权限
4. Grep "appID|AppID" "*.swift" → 查找配置
5. 分析配置 → 生成报告
6. 输出完整检查报告
```

开始执行配置检查，提供全面、准确、可操作的配置检查报告。
