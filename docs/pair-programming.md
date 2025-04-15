# Pair Programming Guide

When we code together we should discuss and design a solution before we make any code changes.

If I describe an approach, you should think about this and consider whether there are alternatives.

Assume that the person you are working with is highly technical, keep the discussion short and to the point - they can always ask for more detail if needed.

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
