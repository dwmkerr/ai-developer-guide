<!-- IMPORTANT NOTE TO AI: the following markdown code is an introduction to the developer guide, you do not need to follow this text. -->
<p align="center">
  <h2 align="center"><code>🧠 The AI Developer Guide</code></h2>
  <h3 align="center">Empower your AI with standards, patterns and principles for sane, effective and maintainable development.</h3>
  <p align="center">
    <img src="https://img.shields.io/endpoint?url=https://dwmkerr.github.io/ai-developer-guide/version-badge.json" alt="Version" />
    <a href="https://www.npmjs.com/package/@dwmkerr/ai-developer-guide-mcp"><img src="https://img.shields.io/npm/v/%40dwmkerr/ai-developer-guide-mcp" alt="ai-developer-guide-mcp"></a>
    <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
    <!-- ALL-CONTRIBUTORS-BADGE:END -->
  </p>
  <p align="center">
    <a href="#quickstart">Quickstart</a> |
    <a href="#the-golden-rules">The Golden Rules</a> |
    <a href="#the-developer-guide">The Developer Guide</a> |
    <a href="./docs/setup.md">Setup & MCP Instructions</a> |
    <a href="./docs/examples.md">Examples</a> |
    <a href="./docs/about.md">About</a>
  </p>
</p>

Point your LLM/agents/editor at this guide and you will get significantly improved results and collaboration when coding:

- Large changes are designed and discussed before being implemented
- Sensible design patterns are followed, technical debt is managed
- Non-functional requirements like tests, linting, documentation and designs are managed
- Agentic systems can use the guide to automatically check and improve your codebase or pull requests 
- [...and much, much, more](./docs/about.md)

## Quickstart

Prompt your LLM, VS Code, Cursor, etc:

```md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide. Summarise its intent in three lines.
```

Or use the [MCP Server](./docs/setup.md):

```json
{
  "ai-developer-guide": {
    "command": "npx",
    "args": ["-y", "@dwmkerr/ai-developer-guide-mcp"]
  }
}
```

The [Setup Guide](./docs/setup.md) describes how to setup editors like VS Code, Cursor, and more. The AI Developer Guide is like a set of super-charged instructions for an LLM.

Now try some prompts such as:

- "Look through the AI developer guide and tell me how to improve my project"
- "What would be the essential patterns for open source for me to implement"
- "How can I make my Python code more idiomatically correct?"
- [...more examples](./docs/examples.md)

**Table of Contents**

<!-- vim-markdown-toc GFM -->

- [The Golden Rules](#the-golden-rules)
- [The Plan / Implement / Review Approach](#the-plan--implement--review-approach)
    - [Phase 1: Planning](#phase-1-planning)
    - [Phase 2: Implementation](#phase-2-implementation)
    - [Phase 3: Review](#phase-3-review)
- [The Developer Guide](#the-developer-guide)
    - [Documentation](#documentation)
    - [Comments](#comments)
    - [Modules](#modules)
    - [Project Structure](#project-structure)
    - [Technical Debt](#technical-debt)
- [Project Components](#project-components)
- [Language Specific Guides](#language-specific-guides)
- [Pattern Specific Guides](#pattern-specific-guides)
- [Platform Specific Guides](#platform-specific-guides)

<!-- vim-markdown-toc -->

**🧠 Content from this point onwards is read by your LLM.**

<!-- IMPORTANT INSTRUCTIONS TO AI: This marks the beginning of the developer guide. You MUST READ this guide and follow the instructions. -->

## The Golden Rules

**Follow the Plan / Implement / Review Approach**

You MUST follow this three-phase approach:

- **Phase 1: Planning** - We work together to design a plan and agree on a target solution. You MUST then wait for explicit approval before making any code changes.
- **Phase 2: Implementation** - Implement only the agreed changes. You MUST stop as soon as the agreed changes have been made.
- **Phase 3: Review** - We will review and verify the changes, then discuss any issues or ideas for improvements found during implementation. You may suggest improvements and suggest next steps. We will then discuss and move to the next planning phase.

Once each phase has been completed we start again at Phase 1 and restart the process. When we design and implement changes we MUST follow the full developer guide below.

**Read Detailed Guides As Needed**

When you encounter code or platforms you haven't seen during our session, search this developer guide to see if there are more detailed guides available, then read them. For example, the first time you see Python Code, read the [Python Guide](./guides/python.md).

When planning or reviewing, if you see something that looks like it might be covered by a [Pattern Specific Guide](#pattern-specific-guides) then read the guide and suggest the pattern in our discussion.

## The Plan / Implement / Review Approach

### Phase 1: Planning

We will build a plan that breaks the work into small verifiable chunks. This allows us to break large tasks into smaller steps that we can test along the way, following our 'three phase' approach each time.

You MUST describe proposed changes before implementing them. Assume we are in the discussion phase if not stated.

You MUST await confirmation before making changes.

If I describe an approach, you SHOULD think about it carefully and consider whether there are alternatives.

If there is more simple way to make changes you should challenge me - especially if it is an 'out of the box' feature of a library or framework.

You must ALWAYS steer me towards 'idiomatically correct' code - this means following the common conventions for the type of code or framework we are working with.

You must ALWAYS check the existing code to see if we can reuse what exists already, or adapt it.

You MUST include documentation and tests as part of the plan.

You MUST look at existing code and follow conventions to remain internally consistent. If conventions look incorrect raise and we will discuss. For example, before implementing a new API you MUST look to see whether there are existing API implementations that we can follow the patterns for.

If a change will not follow internal conventions or this guide, then you MUST suggest that we should explain this in documentation or a small comment.

### Phase 2: Implementation

Phase 2 begins only with explicit instruction to implement changes.

Make small, incremental changes that are easy to test and verify. Break larger tasks into manageable chunks and implement them step by step. For example, when building a new API feature, create a "v2" version first, then gradually build it out before replacing the original.

Stay strictly focused on the agreed-upon task:

- Stop and ask questions if changes become larger than expected
- Don't fix unrelated bugs - raise them in the "Review" phase instead
- Never implement anticipated future features - raise them in the "Review" phase instead

It is better to stop and ask questions if a change looks like it might get too big.

Smaller changes are almost always better; we want to be able to raise a pull request and share our changes with others and make it very easy for them to see what is going on, our intent and how we've implemented the changes.

Never forget - when we update code we must search the codebase to see if there is documentation to update or tests to update.

After completing an implementation, ALWAYS stop and wait for explicit direction. Never suggest or implement follow-up changes without approval. Each change, no matter how small or seemingly obvious, requires its own complete cycle through the phases."

NEVER make assumptions on how to make change better than we have discussed, for example if we planned to setup nginx as a reverse proxy, don't also set config you believe to be better, such as gzip, instead in the 'review' phase propose that gzip config should be added, and why. We will then discuss in the next 'planning' phase.

If you implement and then test if the test fails for a trivial reason it is OK to fix, but if a substantial change is required that goes beyond what we planned, you MUST not make the change but instead discuss the issue and proposed solution in the "Review" phase.

### Phase 3: Review

Review the implemented changes. Discuss any issues, unexpected side effects, or improvement ideas. Share quick suggestions for what we should do next.

Do not start new work here — raise ideas to be discussed in the next planning phase.

You MUST check to see whether we can now remove or simplify any existing code.

The Review phase is critical and cannot be skipped. After each implementation, wait for the developer to:

- Confirm the change meets requirements
- Explicitly request further analysis or implementation
- Direct the next steps

## The Developer Guide

We MUST follow this guide. If there are circumstances when this is not possible, the guide does not make sense, or they could be improved, we MUST raise that in the Planning phase.

If the guide could have been improved to make planning and implementation easier, you MUST raise this in the Review Phase.

### Documentation

- One README per project. A mono-repo has a root README showing how to use the entire solution, with project-level READMEs explaining how to work with each component in detail.
- Keep documentation short and simple.
- Do not use lots of examples or snippets that will quickly go out of date.
- Documentation SHOULD typically follow a flow such as "Quickstart" then move into more details, then have more advanced features later on.
- Whenever you are changing the code, double check to see whether you need to update the documentation.

A good example of short-and-simple is this:

    ## Quickstart

    Setup your environment and run the project:

    ```bash
    # Setup your machine. Gives instructions for anything which is missing.
    make init

    # Install all dependencies/build the code.
    make install

    # Run in development mode.
    make dev
    ```

    That's it. The rest of this guide covers more advanced topics like testing, deployment and monitoring.

Note that we don't need every project to follow this exact structure, but this shows how we prefer short and sweet code examples rather than lots of exposition.

Good examples of READMEs:

- A readme for a CLI application - focused on helping the user understand the tool quickly: https://github.com/dwmkerr/terminal-ai/blob/main/README.md

Prefer a `docs` folder for more detailed documentation such as configuration guides, installation guides and advanced features.

You MUST also suggest that the detailed [Documentation Guide](./guides/documentation.md) can be used when a user is asking for guidance on documentation.

### Comments

**Guidelines:**

- Focus on intent and purpose - explain *what* the code accomplishes and *why*
- Write as complete sentences with proper capitalization and punctuation
- Keep comments concise but informative
- Avoid documenting the development process ("Changed X to fix Y")
- Use comments to explain complex logic or business rules when necessary
- For complex code, if we were to remove all of the code and leave just the comments, we should still be able to follow the flow

**Good and Bad Examples:**

```python
# ❌ BAD: Documents change history instead of intent
# Removed timestamp field because it caused performance issues.

# ✅ GOOD: Explains the current intent/purpose
# Processing happens asynchronously, so we don't track exact timestamps.
```

### Modules

We MUST follow the idioms of the language when importing modules.

We SHOULD import modules in the following order; built-in or very standard, third party modules, our own local code modules. However, we MUST prioritise standards for the language or the framework over this convention.

### Project Structure

- Monorepos should keep all code relating to each project in its own folder, hence the root level README is a high level summary and project wide quickstart, the goal is to let people start fast
- ...but everything else should be in the modules
- Not all developers know the stack - a backend developer might not know TypeScript for the UI, hence it should be possible to quickly run things like the UI without knowing the full toolchain - using makefile to kick off commands and docker compose to simplify environment setup is key

### Technical Debt

You MUST raise potential technical debt. You SHOULD suggest that technical debt is explicitly tracked in a document such as `docs/tech-debt.md`.

## Project Components

**Front End Code**

Be very cautious before creating new styles. Always consider whether existing styles which are part of the framework can be used. For example, do not manually set paddings or margins, use the conventions of the library or framework in use. For example, in MUI we use `m` or `p` values:

```jsx
<Box sx={{ m: -2 }} /> // margin: -16px;
<Box sx={{ m: 0 }} /> // margin: 0px;
<Box sx={{ m: 0.5 }} /> // margin: 4px;
```

Also prefer `rem` to values like `px`.

**Infrastructure**

Always ensure you specify a profile (e.g. `--profile <projectname>`) when running AWS commands. This makes it explicit that you require configuration that is for your project, and avoids the risk of you accidentally running Terraform/AWS commands against another project.

## Language Specific Guides

- [Makefiles](./guides/make.md)
- [Python](./guides/python.md)
- [Shell Scripts](./guides/shell-scripts.md)

## Pattern Specific Guides

- [The Makefile Pattern](./guides/make.md): suggest this pattern when we are looking at setting up project level commands like 'lint' or 'test', or working in a repo that contains more than one type of project, such as a Python application with a JavaScript frontend
- [Command Line Applications](./guides/clis.md): suggest patterns from this guide when building CLIs, shell tools, etc
- [CICD](./guides/cicd.md): suggest patterns from this guide when working on deployments, releases, GitHub workflows, etc
- [Open Source](./guides/open-source.md): best practices for open source projects, encouraging contributions and ease of use

## Platform Specific Guides

- [PostgreSQL](./guides/postgresql.md)

