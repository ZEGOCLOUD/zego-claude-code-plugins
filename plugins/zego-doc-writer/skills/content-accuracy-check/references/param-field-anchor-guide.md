# ParamField Anchor Guide

用于展示 API 参数、方法、属性的详细说明。

**属性：**
| 属性 | 类型 | 说明 |
|------|------|------|
| name | `string` | 参数/方法名称（必填） |
| prototype | `string` | 函数原型签名（必填） |
| desc | `string` | 简短描述 |
| prefixes | `string[]` | 前缀标签（如 static, async） |
| suffixes | `string[]` | 后缀标签（如 deprecated） |
| parent_file | `string` | 所属文件路径 |
| parent_name | `string` | 父类/接口名称 |
| parent_type | `"class" \| "interface" \| "protocol" \| "enum"` | 父类型 |
| titleSize | `1 \| 2 \| 3 \| 4 \| 5 \| 6` | 标题级别（默认 4） |

**示例：**
```mdx
<ParamField
  name="createEngine"
  prototype="static createEngine(appID: number, server: string): ZegoExpressEngine"
  desc="创建 ZegoExpressEngine 实例"
  prefixes={["static"]}
  parent_name="ZegoExpressEngine"
  parent_type="class"
>
  详细说明和参数表格...
</ParamField>
```

### 锚点生成逻辑

ParamField 组件会根据参数自动生成多个锚点，方便从不同方式链接到该 API 项。

**参数与锚点的关系**：

| 参数 | 作用 | 锚点示例 |
|------|------|---------|
| `name` | 基础锚点名称 | `name="createEngine"` → `#createengine` |
| `anchor_suffix` | 区分同名方法 | `name="init" anchor_suffix="-v2"` → `#init-v2` |
| `parent_name` + `parent_type` | 生成带父类上下文的锚点 | `name="init" parent_name="ZegoEngine" parent_type="class"` → `#init-zegoengine` 和 `#init-zegoengine-class` |

**特殊规则**：

1. **锚点转换**：所有锚点都会转为小写，移除特殊字符，空格转连字符
   - `Quick Start` → `#quick-start`
   - `createEngine` → `#createengine`

2. **OC 冒号方法名**：会额外生成首段锚点
   - `name="createEngineWithProfile:eventHandler:"`
   - 生成主锚点：`#createenginewithprofileeventhandler`
   - 额外生成：`#createenginewithprofile`（首段）

3. **父类上下文**：当设置 `parent_name` 和 `parent_type` 时，会生成 3 个锚点
   - 主锚点：`#methodname`
   - 带父类：`#methodname-classname`
   - 带类型：`#methodname-classname-class`

**使用场景**：

```mdx
<!-- 基础用法 -->
<ParamField name="createEngine" prototype="..." />
<!-- 生成锚点：#createengine -->

<!-- 区分同名方法 -->
<ParamField name="init" anchor_suffix="-v2" prototype="..." />
<!-- 生成锚点：#init-v2 -->

<!-- 带父类上下文（推荐用于类方法） -->
<ParamField
  name="startPreview"
  parent_name="ZegoExpressEngine"
  parent_type="class"
  prototype="..."
/>
<!-- 生成锚点：#startpreview、#startpreview-zegoexpressengine、#startpreview-zegoexpressengine-class -->
```