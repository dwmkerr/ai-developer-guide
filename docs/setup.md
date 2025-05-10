# Setup

This page describes how to set up specific tools and editors, as well as how to create your own guides or project specific guides.

<!-- vim-markdown-toc GFM -->

- [Tools](#tools)
    - [Visual Studio Code](#visual-studio-code)
    - [Cursor](#cursor)
    - [Claude Code](#claude-code)
- [Creating Custom or Project Specific Guides](#creating-custom-or-project-specific-guides)
- [Installing Locally](#installing-locally)
- [Forking](#forking)

<!-- vim-markdown-toc -->

## Tools

Instructions for common tools are below. [Open an issue](#todo) if you'd like to see others.

### Visual Studio Code

Use [Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode).

Create a local [GitHub Copilot Instructions file](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot) with the prompt:

```bash
cat << EOF > .github/copilot-instructions.md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.
EOF
```

You can also drop the prompt directly in the chat:

<img alt="Screenshot of an introduction to how the developer guide works for Visual Studio Code" width="600px" src="images/vscode.png" />

### Cursor

Paste the following prompt it to the chat box:

```
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.
```

### Claude Code

Create a `CLAUDE.md` file in your project directory. Load the guide and add any additional instructions:

```bash
cat << EOF > ./CLAUDE.md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.

# Additional Instructions
# - Item 1
# - Item 2
# - ...etc
EOF
```

## Creating Custom or Project Specific Guides

Create a file in your project directory, point at the developer guide and then extend with your own requirements:

```md
cat << EOF > ai-developer-guide.md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide.

You MUST also follow the rules below which apply to this project:

- Example rule 1
- Example rule 2
- Link to a more detailed guide: https://whatever.com
```

Then prompt your AI to read this guide.

## Installing Locally

To install a local copy of the guide you can run the script below:

```bash
curl -O https://raw.githubusercontent.com/dwmkerr/ai-developer-guide/main/README.md \
    > ai-developer-guide.md
```

Then prompt your AI to use it:

```
Read the developer guide at:
  ./ai-developer-guide.md
You MUST follow the rules in this guide. Summarise its intent in three lines.
```

## Forking

Please feel free to [fork](https://github.com/dwmkerr/ai-developer-guide/fork) the guide and adapt to your needs. The code is MIT Licensed.
