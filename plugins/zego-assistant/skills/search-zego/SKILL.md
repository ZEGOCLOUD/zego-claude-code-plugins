---
name: search-zego
description: 使用此技能搜索 ZEGO 相关问题和文档。当用户需要搜索 ZEGO（ZEGOCLOUD、即构科技）相关问题和文档时触发。
version: 1.0.0
---

## ZEGO 文档搜索指南

ZEGO 提供了非常多的产品，每个产品对应提供非常多平台的文档。当用户需要搜索 ZEGO 相关问题和文档时，请遵循一定的搜索原则：


## 集成 ZEGO 产品
如果用户要求集成 ZEGO 的一个或者多个产品，请优先通过阅读相关产品快速开始文档了解整体集成流程后开始集成工作。步骤大致如下：
- 根据当前项目性质或者用户要求确定用户要集成哪些产品或者平台
- 调用 get_platforms_by_product 工具了解相关产品都支持哪些平台
- 调用 get_doc_links 或者指定产品和平台的文档链接，从中过滤 implementing xxx/integrating sdk/quick start 相关的链接
- 调用 get_token_generate_doc 获取客户端如何使用 Token 鉴权以及如何在服务端生成 Token 的说明及示例代码
- 调用 get_server_signature_doc 获取调用 ZEGO 服务端 API 的签名机制说明及示例代码
- 通过浏览快速开始或者集成链接了解实现步骤后开始制定实现任务并开始实现集成

如果集成过程中有相关的接口需要明确详细用法或者在集成测试时发现某些接口有错。可通过过滤出 get_doc_links 工具返回链接中带client-sdk/api-reference 字样的文档查看详细的接口说明。
优先通过相关链接阅读文档内容，如果通过链接还不能完全了解到完整的集成流程需要更多的信息辅助集成，可调用 search_zego_docs 搜索相关产品的文档说明。该方法使用 RAG 技术搜索向量数据库并返回知识库片段。


## 修复 ZEGO 产品相关错误

先了解项目中集成了哪些 ZEGO 产品，集成了哪些平台的 SDK 或者接口。并按以下大致步骤处理：
- 如果有错误码，调用 search_zego_docs 搜索相关产品文档尝试找到错误码说明
- 如果是客户端接口使用报错，可通过过滤出 get_doc_links 工具返回链接中带client-sdk/api-reference 字样的文档查看详细的接口说明。
- 根据问题错误提示或者结合上下文整合问题或关键字直接调用 search_zego_docs 搜索文档。

在通过搜索错误码、错误描述、阅读接口文档后，仔细分析问题原因后，制定修复计划并开始实施修复。

## 文档获取方式选择（重要）

**禁止使用 search_zego_docs 的场景（必须用 WebFetch 打开链接阅读完整文档）：**
- 快速开始/Quick Start 类文档
- 集成指南/Integrating SDK 类文档

**适合使用 search_zego_docs 的场景：**
- 查询特定错误码含义
- 搜索某个具体 API 的用法片段
- 根据关键字查找相关信息

原因：search_zego_docs 基于 RAG 返回文档片段，无法保证完整性。对于需要完整流程的场景，必须通过 WebFetch 工具打开文档链接阅读完整内容。

## 最佳实践要求
- get_doc_links 工具返回的链接都是.md结尾的，可以用 WebFetch 直接读取文档页面对应的 md 内容
- 调用 search_zego_docs 工具时，如果涉及 FAQ 知识库和其他知识库片段冲突时，应优先以其他知识库的片段为准。因为 FAQ 知识库更新没那么及时。
- search_zego_docs 参数 传datasetid时，这些id必须是一串只包含字母和数字的字符串，不包含其他特殊字符。
- 可以通过 get_doc_links 找到相关产品和平台 release-note 确定最新的 SDK 版本号

## 避免做什么
- 避免在不查阅 ZEGO 文档的情况下就直接尝试集成 ZEGO 产品或者修复 ZEGO 相关问题。
- 避免通过搜索引擎搜索 ZEGO 相关问题，而应该优先通过调用 ZEGO 提供的工具搜索 ZEGO 文档说明或者文档链接后再查看文档链接内容。

## 重要说明

当准备使用关键词搜索时:

1. **Get available datasets** - Call `mcp__plugin_zego-assistant_ZEGO__get_zego_product_datasets` to list all products and their knowledge base IDs
2. **Search for API docs** - Call `mcp__plugin_zego-assistant_ZEGO__search_zego_docs` with relevant dataset IDs
3. **Validate dataset IDs** - Ensure IDs contain only numbers and lowercase letters (no `-` or `_`)
4. **Confirm with user** - Present the found API and confirm before integrating
5. **Implement integration** - Add the API call with proper signature to the project
