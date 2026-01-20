---
name: resource-downloader
description: 使用此技能下载资源文件。当用户需要下载 ZEGO 相关资源或者 github 仓库时触发。
version: 1.0.0
---

当用户要求下载 ZEGO 相关资源或者 github 仓库时，使用以下脚本下载：

使用 `python3 ./scripts/downloader.py <github_repo_url_or_file_url> <当前workspace的根目录路径>` 脚本下载资源文件或者github仓库。

注意：github 仓库不要包含分支或者目录信息，否则下载失败。（正确下载的url示例：https://github.com/ZEGOCLOUD/zego-claude-code-plugins）