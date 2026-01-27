# 发布日志示例

本文描述新产品发布日志的建议示例。老产品建议保持原有格式，除非用户主动要求更新。

```mdx
## V2
### 2025-12-25

<Accordion title="服务端 v2.9.0" defaultOpen="true">

**新增功能**

| 功能项| 功能描述| 相关文档|
| ---- | ---- | ---- |
| 支持多模态大模型 |支持符合 OpenAI 标准的文字输入语音输出的多模态大模型，例如 gpt-4o-audio、qwen3-omni-flash 等模型。详情请参考[配置 LLM](/aiagent-server/guides/configuring-llm)。|[配置 LLM](/aiagent-server/guides/configuring-llm)|
| 支持 OpenAI [Responses API](https://platform.openai.com/docs/api-reference/responses) 标准|支持调用符合 OpenAI Responses API 标准的大语言模型或智能体，例如可调用豆包 seed 系列模型、百炼智能体等。详情请参考[配置 LLM](/aiagent-server/guides/configuring-llm)。|[配置 LLM](/aiagent-server/guides/configuring-llm)|
|支持火山单向流式TTS的情绪标签|支持火山单向流式 TTS 的情绪标签，从而实现 AI 语音更好的情绪展现，例如愤怒、悲伤、恐惧等。实现效果可参考[豆包语音合成大模型](https://www.volcengine.com/product/tts)中的多情感音色。<br/><Note title="说明">若希望使用本能力，请联系 ZEGO 技术支持。</Note>||
|支持服务端 API 实现插入若干条上下文消息|-|[AI短期记忆（智能体上下文）管理](/aiagent-server/advanced/ai-short-term-memory)|


**改进优化**
- 优化语音实例、数字人实例的互动延迟，降低约 100ms 。

**问题修复**
- 修复 [UserAudioData](/aiagent-server/callbacks/receiving-callback) 回调不可用问题。
</Accordion>
```
