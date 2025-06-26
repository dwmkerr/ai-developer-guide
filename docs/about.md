# About

**Why do I need an AI developer guide?**

LLMs are increasingly being used for more and more complex development tasks. Agentic systems are greatly expanding the scope of what can be done with AI in the software engineering, testing, refactoring, architecture and design space.

However - without giving an LLM a set of sensible principles on _how_ to develop, results can be extremely varied in quality. Some of the most common issues are:

- Overly complex changes: LLMs make changes far beyond the scope of what was asked
- Technical debt: changes are additive - old code is not cleaned up or refactored
- Inconsistency: changes are not made consistently in the codebase, internal conventions are not respected
- Ignoring idioms: common idioms for languages and platforms are ignored
- Lack of design principles: essential principles around sensible design, bounded contexts, abstractions and so on are not understood

When prompted well and guided well, LLMs can produce code at much higher quality. When instructed to design, reason, and discuss, fewer iterations are needed and the whole process becomes a lot more effective and a lot more fun.

## What's in a Guide?

This guide contains:

[**The Golden Rules**](../README.md#the-golden-rules)

These are universal principles that must be followed - Asimov's Three Laws for LLMs. These rules state that we should design and discuss change before making them, and constrain some of the LLM "enthusiasm" for making overly complex changes or trying to anticipate future needs, ignore existing code, etc.
There are currently three essential artifacts:

[**The Developer Guide**](../README.md#the-developer-guide)

This is set of principles that should be followed. The goal of these principles is that they are near-universal - they don't depend on frameworks or suggest idioms which might not be suitable for your projects. These are rules like "Check if we already have something in the code that does X before we try to recreate it" or "look in the documentation for a standard solution to this problem with this module before inventing one yourself".

The principles become more specific as we go deeper into specific languages or platforms.

You should augment this guide with your own principles or standards - there are some suggested ways to do this in the [Setup Guide](./setup.md).
