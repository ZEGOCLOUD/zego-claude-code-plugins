---
name: zego-integration-migration
description: DEPRECATED legacy-plugin migration notice. Use when the user asks to integrate ZEGO, 即构, ZEGOCLOUD, Express SDK, ZIM, RTC, video call, voice call, 1v1 call, live streaming, instant messaging, in-app chat, AI Agent, digital human, interactive whiteboard; or to generate ZEGO tokens, call ZEGO server APIs with signature, look up ZEGO error codes, or download ZEGO SDKs (实时音视频、直播、即时通讯、数字人、白板、错误码、token 生成、鉴权、服务端 API、签名). This plugin is superseded by the zego-integration Agent Skill.
version: 2.0.0
---

# This plugin is superseded by the zego-integration Agent Skill

The legacy five-skill + MCP workflows are gone. Do NOT try to call `get_doc_links`, `search_zego_docs`, or any `mcp__ZEGO__*` tools — they no longer exist. Instead:

1. **If the `zego-integration` skill is already available in this environment** (check the installed skills list): use it directly for the user's task, and suggest uninstalling this legacy plugin to avoid duplicate triggering.
2. **Otherwise, stop and tell the user** (in their language) that this plugin has stopped evolving and has been replaced by the standalone `zego-integration` Agent Skill, which works across Claude Code, Codex, Cursor, and other agents. Ask them to install it and restart the session:

   ```bash
   npx skills add ZEGOCLOUD/zego-integration
   ```

   One-line alternative (also recommended for networks without direct GitHub access):

   ```bash
   curl -fsSL https://raw.githubusercontent.com/ZEGOCLOUD/zego-integration/main/install.sh | bash
   # China mainland mirror:
   curl -fsSL https://gh-proxy.com/https://raw.githubusercontent.com/ZEGOCLOUD/zego-integration/main/install.sh | bash
   ```

   More install options: https://github.com/ZEGOCLOUD/zego-integration

3. **Optionally suggest removing the legacy plugin** after the new skill is installed:

   ```text
   /plugin uninstall zego-assistant@zego-claude-code-plugins
   /plugin marketplace remove zego-claude-code-plugins
   ```

Do not attempt ZEGO integration tasks from memory while the new skill is missing — its local docs cache and playbooks are what make integrations accurate. Ask the user to install it first.
