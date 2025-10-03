# AI Developer Guide Review

Review current uncommitted changes against AIDG standards. Terminal-optimized output.

## Instructions:

1. **Get uncommitted changes**: Use `git status --porcelain` and `git diff --name-only` to identify only unstaged/staged files

2. **Fetch AIDG guides** (only if not already in memory): Use MCP tools if needed:
   - `mcp__ai-developer-guide__fetch_main_guide`
   - `mcp__ai-developer-guide__fetch_guide` for relevant file types

3. **Analyze current work**: Read modified files and review against AIDG standards

## Output Format:

**Changes Summary:**
- 2-3 bullets describing what files/changes are being made

**AIDG Improvements:**
- Terse, actionable suggestions for current uncommitted work only
- Format: `file:line - suggestion`

Keep output minimal and terminal-friendly.