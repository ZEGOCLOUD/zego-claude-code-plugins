# ZEGO Claude Code Plugins

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README_EN.md) [![中文](https://img.shields.io/badge/lang-中文-red.svg)](README.md)

> **⚠️ This repository is no longer evolving.** The `zego-assistant` plugin is superseded by the standalone **[zego-integration Agent Skill](https://github.com/ZEGOCLOUD/zego-integration)** — install that instead (works with Claude Code, Codex, Cursor, and other agents):
>
> ```bash
> npx skills add ZEGOCLOUD/zego-integration
> ```

## What changed

Starting with v2.0.0, the `zego-assistant` plugin no longer ships the legacy five skills or the ZEGO docs MCP server. It keeps a single **migration-guide skill**: when users of the old plugin raise a ZEGO task, the agent guides them to install the new zego-integration Skill. The legacy MCP workflow (`search_zego_docs`, `get_doc_links`, …) has been removed.

After installing the new skill, existing users are advised to remove the legacy plugin:

```text
/plugin uninstall zego-assistant@zego-claude-code-plugins
/plugin marketplace remove zego-claude-code-plugins
```

## Still want to install this plugin (migration guidance only)

```bash
/plugin marketplace add https://github.com/ZEGOCLOUD/zego-claude-code-plugins
/plugin install zego-assistant@zego-claude-code-plugins
```

## Why the migration

The new zego-integration Skill caches the official docs repo locally and lets the agent search the source files directly, replacing the previous RAG + MCP approach. It drops the MCP dependency and covers error codes, API parameters, token04/signature implementation, SDK downloads, and scenario playbooks — independent of any specific coding agent. See [Using AI Coding](https://www.zegocloud.com/docs/ai-coding/using-ai-coding).

## License

MIT License

## Contact

- Issues: [GitHub Issues](https://github.com/ZEGOCLOUD/zego-claude-code-plugins/issues)
- Email: docuo@zego.im
