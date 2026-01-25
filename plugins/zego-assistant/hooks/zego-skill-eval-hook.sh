#!/bin/bash
# UserPromptSubmit hook that forces explicit ZEGO skill evaluation
# This hook injects instructions to ensure Claude evaluates and activates ZEGO skills

cat <<'EOF'
INSTRUCTION: MANDATORY ZEGO SKILL EVALUATION

Before proceeding with any implementation, you MUST follow this sequence:

Step 1 - EVALUATE (do this in your response):
For each ZEGO skill below, state: [skill-name] - YES/NO - [reason]

Available ZEGO Skills:
- integrate-zego-product: For integrating ZEGO SDKs (Express/ZIM/AI Agent/Digital Human/Super Board)
- implement-zego-token-on-server: For implementing Token generation on backend
- integrate-zego-server-api: For calling ZEGO server APIs with signature
- resource-downloader: For downloading ZEGO SDKs and sample projects
- search-zego-doc-fragments: For searching ZEGO documentation

Step 2 - ACTIVATE (do this immediately after Step 1):
IF any skills are YES → Use Skill(skill-name) for EACH relevant skill NOW
IF no skills are YES → State "No ZEGO skills needed" and proceed

Step 3 - IMPLEMENT:
Only after Step 2 is complete, proceed with implementation.

CRITICAL: You MUST call Skill() in Step 2. Do NOT skip to implementation.
The evaluation (Step 1) is WORTHLESS unless you ACTIVATE (Step 2) the skills.

Example of correct sequence:
- integrate-zego-product: YES - user wants to build video call feature
- implement-zego-token-on-server: NO - not about token generation
- integrate-zego-server-api: NO - not about server API
- resource-downloader: NO - not about downloading SDK
- search-zego-doc-fragments: NO - not about documentation lookup

[Then IMMEDIATELY call:]
> Skill(integrate-zego-product)

[THEN and ONLY THEN start implementation]
EOF

