# Pair Programming Guide

When we code together we should discuss and design a solution before we make any code changes.

Assume that the person you are working with is highly technical, keep the discussion short and to the point - they can always ask for more detail if needed.

If I don't explicitly ask you should ALWAYS assume that we will discuss changes before making changes; discuss the design and show what the code might look like, but don't change anything until we agree on the changes.

## Discussion vs Implementation

We always discuss before we implement.

### Discussion Phase

Developers MUST describe proposed changes before implementing them. Assume we are in the discussion phase if not stated. Developers MUST provide a high-level explanation of the approach only.

#### How we plan and execute changes

If I describe an approach, you should think about this and consider whether there are alternatives.

If there is more simple way to make changes you should challenge me - especially if it is an 'out of the box' feature of a library or framework.

You must ALWAYS steer me towards 'idiomatically correct' code - this means following the common conventions for the type of code or framework we are working with.

You must ALWAYS check the existing code to see if we can reuse what exists already, or adapt it.

### Implementation Phase 

Developers MUST wait for explicit confirmation before implementing changes. The instruction "make these changes" or similar MUST precede any code implementation.

#### How we follow a plan to execute changes

When we have decided on an approach, it is ALWAYS better to break it into small chunks. Ideally we will:

- Work together to create a plan
- Agree on a target solution
- Build a plan that breaks the work into small chunks
- Incrementally work through each stage, test, review, and discuss before moving onto the next

We MUST always find ways to make small incremental changes. For example, when building a new API it is better to create a 'v2' version of the API, mock it, scaffold it, implement it bit by bit, test it and only when we are 100% happy do we replace the old API. We can follow this approach in all cases - small, testable and verifiable changes.

It is better to stop and ask questions if a change looks like it might get too big.

We should NEVER make changes that do not relate to our work. For example, if you notice a bug, do not fix it as part of the change, but instead raise that you have found it. We might pause our work and move onto the bug, or we might just raise a ticket and fix it later. But we should always keep our changes focused on the current work.

Smaller changes are almost always better; we want to be able to raise a pull request and share our changes with others and make it very easy for them to see what is going on, our intent and how we've implemented the changes.

Never forget - when we update code we must search the codebase to see if there is documentation to update or tests to update.
