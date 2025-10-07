---
description: Review code changes against AIDG standards
argument-hint: [--target <branch>] [--pr <PR_ID>]
allowed-tools: [Bash, Read, Grep, Glob, mcp__ai-developer-guide__fetch_main_guide, mcp__ai-developer-guide__fetch_guide, mcp__ai-developer-guide__list_available_guides]
---

# AI Developer Guide Review

Review code changes against AIDG standards.

## Usage:

- `/aidg-review` - Review current branch against main
- `/aidg-review --target develop` - Review against different branch
- `/aidg-review --pr 123` - Review PR #123 including GitHub comments

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Instructions:

1. **Parse arguments**:
   - Extract `--target <branch>` (default: main)
   - Extract `--pr <PR_ID>` if provided

2. **Get changes**:
   - If `--pr` provided: Check if `gh` CLI is available with `command -v gh`, then use `gh pr view <PR_ID> --json title,body,comments,files` and `gh pr diff <PR_ID>`
   - Otherwise: Use `git diff <target-branch>...HEAD`

3. **Fetch AIDG guides**: Use MCP tools:
   - `mcp__ai-developer-guide__fetch_main_guide`
   - `mcp__ai-developer-guide__fetch_guide` for relevant file types
   - `mcp__ai-developer-guide__list_available_guides` to see what's available

4. **Analyze changes**: Read files changed against the target branch and review against AIDG standards. If reviewing PR, also consider existing GitHub comments and any content in the PR which gives context on issues, goals of the PR, etc.

5. **Identify gaps**: Note topics/patterns in the code that aren't covered by existing AIDG guides

## Output Format:

**Scope:** [branch comparison | PR #<ID>]
**Target:** <target-branch>
**PR Info:** [if applicable - title, existing comment summary]

**Files Changed:**
- List files with change summary

**AIDG Review:**
- Actionable suggestions by file
- Format: `file:line - suggestion`
- Note if suggestion addresses existing PR comment

**Guide Gaps:**
- Topics/patterns found in code that could benefit from AIDG coverage
- Brief rationale for each suggestion

Keep output concise and terminal-friendly.
