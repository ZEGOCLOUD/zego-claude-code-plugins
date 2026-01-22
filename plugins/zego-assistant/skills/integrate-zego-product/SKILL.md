---
name: integrate-zego-product
description: This skill should be used when the user asks to "integrate ZEGO SDK", "add ZEGO product", "implement ZEGO RTC/AIAgent/etc.", "implement screen sharing", "integrate ZEGO feature", "集成ZEGO产品", "集成屏幕共享", "集成ZEGO某个功能", or requests guidance on integrating ZEGO services or features like Real-Time Audio/Video, ZIM, AI Agent, Low-Latency Live Streaming, screen sharing, in-app audio/video effects, or other ZEGO product features. Provides step-by-step integration workflows for ZEGO products and features.
version: 1.0.0
---

## ZEGO Product Integration Guide

This skill provides structured workflows for integrating ZEGO products and features into applications. Follow the established integration process to ensure proper implementation of SDKs, authentication, and server-side APIs.

**This skill handles:**
- Full product integration (RTC, ZIM, AI Agent, etc.)
- Specific feature integration (screen sharing, audio effects, cloud recording, etc.)
- Server-side API integration with signature and token generation

## Integration Workflow

When a user requests integration of ZEGO products, follow these steps in order:

### Step 1: Determine Integration Scope

Identify which products, features, and platforms the user needs to integrate:

**Product-Level Integration:**
- Clarify the target platform (iOS, Android, Web, Windows, macOS, Linux, Flutter, etc.)
- Confirm which ZEGO products are required:
  - Real-Time Audio/Video (RTC)
  - In-app Chat (ZIM)
  - AI Agent
  - Low-Latency Live Streaming
  - AI Effects/AI Effects SDK
  - Digital Human/Digital Human SDK
  - SuperBoard/SuperBoard SDK
  - Cloud Recording
  - Cloud Player
  - Cloud ASR
  - Other ZEGO products

**Feature-Level Integration (examples):**
- Screen sharing (屏幕共享)
- Live streaming with mixing (混流直播)
- Virtual background (虚拟背景)
- Other ZEGO Product/SDK features

**Project Type:**
- Verify the user's project type (native app, web app, server-side integration)

### Step 2: Gather Product Information

Before writing any integration code, gather necessary documentation:

**Call required MCP tools:**

1. **`get_platforms_by_product`** - Retrieve all supported platforms for the target product
2. **`get_doc_links`** - Get documentation links for the specific product and platform
3. **`get_token_generate_doc`** - Obtain Token generation documentation and example code for authentication
4. **`get_server_signature_doc`** - Get server API signature documentation for server-side calls

### Step 3: Review Integration Documentation

From the documentation links returned by `get_doc_links`, filter for:
- Quick Start / 快速开始
- Integrating SDK / 集成SDK
- Implementation Guide / 实现指南

Use `mcp__web_reader__webReader` to read the complete documentation from `.md` links. Complete documentation is essential for integration workflows - do not rely on fragmented search results.

### Step 4: Implement Client-Side Integration

Based on the Quick Start or Integration guide:

1. **SDK Installation**
   - Add SDK dependencies to the project
   - Configure build settings as required

2. **Initialization**
   - Create engine instance with AppID
   - Set up event handlers

3. **Authentication**
   - Implement Token-based authentication
   - Use the token generation examples from `get_token_generate_doc`
   - Generate tokens on the server, acquire on client

4. **Core Features**
   - Implement the primary product features (room joining, publishing, etc.)
   - Follow the specific integration guide for the product

### Step 5: Implement Server-Side Components

For server-side API calls:

1. **API Signature**
   - Use the signature mechanism from `get_server_signature_doc`
   - Implement signature generation based on the programming language
   - Include signature in API request headers

2. **Token Generation Endpoint**
   - Create an endpoint to generate tokens for clients
   - Use the examples from `get_token_generate_doc`
   - Implement proper error handling

### Step 6: API Reference and Troubleshooting

When specific API usage needs clarification during implementation:

From `get_doc_links` results, filter for links containing:
- `client-sdk` - Client SDK API reference
- `api-reference` - Detailed API documentation

Read the specific API documentation to understand parameters, callbacks, and usage patterns.

## Documentation Access Patterns

**For complete integration workflows:**
- Use `get_doc_links` to retrieve documentation URLs
- Use `mcp__web_reader__webReader` to read complete `.md` documentation
- Never rely on RAG fragments for Quick Start or Integration guides

**For specific API queries:**
- Use `get_doc_links` and filter for `api-reference` or `client-sdk`
- Read the complete API documentation

**For general information searches:**
- Use `search_zego_docs` with relevant dataset IDs
- Suitable for: error codes, specific API usage snippets, keyword-based searches
- Not suitable for: complete integration workflows

### Critical: Dataset ID Parameter Format for search_zego_docs

When calling `search_zego_docs`, the `dataset_ids` parameter requires the **`id`** field from `get_zego_product_datasets` output, NOT the **`name`** field.

**Example from get_zego_product_datasets:**
```json
{
  "name": "云端播放器",
  "description": "【英文名Cloud Player】云端播放器...",
  "datasets": [
    {
      "id": "a6ce5daa960911f085fd76185b8a64f0",
      "name": "cloud_player_zh"
    },
    {
      "id": "a7803c00960911f0962376185b8a64f0",
      "name": "cloud_player_server_zh"
    }
  ]
}
```

**Correct usage:**
```python
dataset_ids = ["a6ce5daa960911f085fd76185b8a64f0", "a7803c00960911f0962376185b8a64f0"]
```

**WRONG usage (will fail):**
```python
dataset_ids = ["cloud_player_zh", "cloud_player_server_zh"]  # ❌ These are names, not IDs!
```

**Rules for dataset_ids parameter:**
1. Use the **`id`** field value (e.g., "a6ce5daa960911f085fd76185b8a64f0")
2. Never use the **`name`** field value (e.g., "cloud_player_zh")
3. Always call `get_zego_product_datasets` first to get valid IDs
4. Copy the `id` value exactly as returned (32-character hexadecimal string)

## Available MCP Tools

**Product Information:**
- `mcp__plugin_zego-assistant_ZEGO__get_zego_product_datasets` - List all products and knowledge bases
- `mcp__plugin_zego-assistant_ZEGO__get_platforms_by_product` - Get supported platforms for a product
- `mcp__plugin_zego-assistant_ZEGO__get_doc_links` - Get documentation links for product/platform

**Code Examples:**
- `mcp__plugin_zego-assistant_ZEGO__get_token_generate_doc` - Token generation code (GO, CPP, JAVA, PYTHON, NODEJS, PHP, CSHARP)
- `mcp__plugin_zego-assistant_ZEGO__get_server_signature_doc` - API signature code (GO, CPP, JAVA, PYTHON, NODEJS, PHP, CSHARP)

**Documentation Search:**
- `mcp__plugin_zego-assistant_ZEGO__search_zego_docs` - RAG-based documentation search

## Best Practices

1. **Read Before Coding**
   - Always read the complete Quick Start or Integration guide before implementation
   - Never attempt integration without consulting ZEGO documentation first

2. **Token Management**
   - Generate tokens on the server-side
   - Acquire fresh tokens from the server when needed
   - Never hardcode secrets or long-lived tokens in client applications

3. **API Signature**
   - All server API calls require proper signature
   - Use the unified signature mechanism for all ZEGO products
   - Each product has different server endpoints - verify the correct base URL

4. **Dataset ID Format**
   - Dataset IDs must contain only numbers and lowercase letters
   - No hyphens, underscores, or special characters

5. **FAQ Handling**
   - FAQ knowledge bases may not be as current as other documentation
   - Prioritize official guides and API references over FAQ content

## Common Integration Scenarios

**Real-Time Audio/Video/Live Streaming (RTC):**
- Requires client SDK integration
- Token authentication for room entry
- Optional server API for room management

**AI Agent:**
- Client SDK for agent interaction
- Server API for agent configuration and management
- Token authentication for both client and server calls

**In-app Chat (ZIM):**
- Client SDK for messaging
- Server API for user and conversation management
- Token-based user authentication

## Integration Checklist

Before declaring integration complete, verify:
- [ ] Correct SDK dependencies added for target platform
- [ ] AppID properly configured
- [ ] Token generation endpoint implemented on server
- [ ] Client acquires and uses tokens for authentication
- [ ] Server API calls include proper signatures
- [ ] Event handlers properly configured
- [ ] Core features tested (join room, publish stream, send message, etc.)
