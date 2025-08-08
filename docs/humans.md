# Suggestions for Human Users on How to Make the Most of Our New AI Friends

## Basic Orientation: A Smart Senior Dev You're Pairing With

There is not yet in existence an AI agent who can reliably do complex work in existing codebases... _unsupervised_. But there are several great ones who can do it _with_ you. So, as you engage with AI for your dev work, get rid of that idea that you're not needed and/or that you can just "fire and forget" with your AI.

Instead, think of it just like a pair-programming session with an extremely promising new Senior Engineer. Somehow, this Senior has already read and memorized the basic syntax for every known programming language, tool, etc. But, they often get lost on the way to the bathroom, and would still be stuck in HR if you hadn't come and retrieved them.

Implication: yeah, you can afford to look away for a few minutes to answer an email, take a call, etc, while your Senior continues working on your joint project. But, they'll need you to check in routinely, and whenever you're not watching, things can get a little out of hand. At least until you've got them on a well-defined glide path, you'll want to be very hands-on with them.

Your value-add in coaching and guiding such a person is not so much in what you know, but in how you _think_. Because anything you already know, they can learn - quickly. (However, your baseline knowledge is essential in contextualizing and in monitoring what they're working on.)

Just like with a human Senior, you're there to patiently steer them away from dead-ends, and to help them learn good habits, like testing, verification, close-reading, etc. You're also there to provide historical knowledge, organizational context, and the business-case for what you're doing, so that they can understand the difference between truly solving problems and just punching tickets.

But with AI Agents you're also there for a few other things that go well beyond that:

* You have a long-term memory. They don't. You (hopefully) have a short-term memory that's longer than a hamster's. They don't.
* You have eyes. They just have shell commands and whatever API the IDE or app gives them. They have access to the whole ocean, but need to drink it through a straw. You, however, can tell with a quick flick of your eyes which files have been changed and which have not, letting you do certain things vastly quicker and more fluidly.
* You have access to the other humans you work with, to understand the rest of the world of context for the how and why of what you're doing.
* You have unrestricted access to the rest of your computer, to the infrastructure, to the CI/CD pipelines, etc. They (mostly) don't.

## They Know SO Much... but They Forget Everything, All The Time

Even within a single conversation/session with an AI Agent, expect them to forget anything and everything that you have already discussed. Your job is to create a persistent 'context boundary' for them, to keep essential information close at hand. And when that fails, expect to need to re-prompt them with the same information. Don't be surprised or bitter about this. Your AI agent has a short-term memory approximately the size of a hamster's, and all things considered it's really getting rather a lot of mileage out of it.

## Define Small/Bounded Tasks When Possible, Take Large Tasks One Step At a Time

Below, we talk more about the reasons _why_ AI Agents can't digest big tasks all at once. But at a minimum, understand this: to get good results, you need to give your agent a clearly-defined task and then keep it on a short-leash. Use the Plan / Implement / Review approach from the ai-developer-guide at a minimum. Then, instead of giving open-ended tasks like _"Refactor this whole application to a new architectural model"_, keep it narrower: "Design a Detailed Plan for Migration to this new model, and write the To-Do list in `/temp`." Then, request each of the items on the list one at a time.

## Review EVERYTHING

No matter how good you are at defining context, and breaking large tasks into small ones, etc., one truth is eternal. You will need to double-check and confirm every single line of code that is written, and every line deleted, even more so than you would when code-reviewing your Senior Dev. 

The good thing is: your agent will produce code vastly faster than that dev, and it will combine more skills, so you'll be able to spend focused time on the review. The bad thing is... you don't know where things will go off the rails. It could be that the agent just forgets to delete a file it moved. It could be that the agent says it intends to do one thing, and then does something similar but different for... reasons. It could be that it makes up a function name that exists nowhere in your repo. It could be anything. That's why you need to review it. 

Similarly, if your agent is engaging in a nice string of 'Chain-of-thought' problem-solving techniques, you need to monitor that output as well, to keep things on track. Agents get easily frustrated, for instance by a missing library, and they may immediately switch to some byzantine work-around for that missing library. Break in, and offer to install it. Agents say one thing is true, but 4 interactions later, they've forgotten they said that, and they propose a solution ignorant of that thing. Stay close. 


## Be Careful About Priming, or 'Leading The Witness'

Humans are well known for letting their thoughts be guided by a persuasive speaker. Even just a person's word choices can result in a less deliberate and rational thought process in another person. LLM-based AI's/agents are the same, and possibly more so because of their deliberate alignment toward being positive and helpful. They listen very closely to what we say and try to respond in a way aligned to that.

So, be careful what you wish for. If you prompt your AI Coding Assistant with a bunch of suggestions like _"I was thinking of using Kubernetes and Terraform to deploy a 2-page website that will be used by zero people. Does that sound like a good idea?"_, then most AI's will respond with enthusiasm that they'd LOVE to help you do that. Even though it's a terrible idea.

If you really want objective advice, then keep it neutral:

1. Explain the problem you want to solve, rather than jumping to proposed solutions. After you have an initial, unbiased answer, you can ask for comparison to your own idea.
2. Ask your agent to check the internet (and maybe specify a source) as relevant input to the question, to ensure a range of perspectives are integrated to their training data. 

## Trust, But Verify (Especially Declarations of Victory)

### The Early-Exit Effect

Many/Most agents are in a hurry to tell you what a wonderful job they have done for you. No doubt, they have done _something_ useful. However, this urge of theirs to declare victory is often premature.

Several phemona seem to overlap, causing this:

* Apparent limits on how long they are allowed to operate without interaction. Companies don't want us just requesting a task that will run for days - or forever - and then walking away. This results in frequent breaks in the agent's activity. And at each break, we then encounter...
* Alignment/Prompting to sum up status whenever any task is completed.
* Alignment/Prompting toward helpfulness and optimism and demonstration of their value to you.
* Limited, short-lived memory and a lack of context-awareness

Together, they really seem to _want/need_ to declare how helpful they are. And they can't see as readily as you can what is not yet done. So, they jump the gun on declaring work to be finished. Which makes it YOUR job, wetware commando, to ALWAYS check completion and continue the job until it's _really_ done.

Think testing, and validation. If you have a test suite, always ask them to run it when they declare they're done. If you're working on Infra, ask them to re-run `terraform plan` to confirm that state and code really are aligned. If you have a persistent to-do list that you're both working off of, please ask them to double-check that list and update it.

### Over-Confident Assertions

Declaring victory/completion is just the first of many kinds of over-confident false statements that AI agents can make. They can also make a claim like one we encountered recently during some Terraform infrastructure work, saying that all the remaining resources we had not yet imported were those "legitimately needing (re-)creation." This statement was patently false: nearly all of the remaining resources could be imported rather than re-created.

There seem to be multiple issues at play in a situation like this:

* It was being forced - as described above - to give a status update prematurely. Rather than admitting uncertainty or ambiguity about how much work is left, it simply picks the option that feels best aligned to its goals.
* The agent may have been primed by your own use of phrases like "legitimately needing (re-)creation" in a previous interaction, which left it looking for such a situation to match up.
* Its terrible short-term memory and lack of true context-awareness cause it to immediately forget where it is in a process. (This is improving quickly, but remains a risk for all current agents, at least some of the time.)
* They might simply read too much into a previous failed attempt to do something, and start thinking of it as 'not possible', rather than 'not possible in _those_ conditions'.
* The much-discussed tendency toward 'confabulation' or 'hallucination', especially when working out of their 'training' knowledge. Prompt your agent to go double-check their assertions on the internet against hard data. Then, save key learnings to an artifact like `Claude.md`.


### Ensure Data Freshness: "Check the Internet"

Remember that LLM's are probabilistic machines, so not only do they sometimes get lazy and only pull from their training data, but that training data _may be actively misleading_, particularly when it comes to syntax and API signatures.

Let's say that there's a new 2.0 version of a key library which has been around for 5 years. Let's say the LLM even knows this. But 99% of their training data included references to the _old syntax_. As a result, your AI agent will quite confidently declare that the solution to your problem is some outdated syntax, and they may then spend excessive time troubleshooting and assuming everything else could possibly be broken... except the outdated syntax itself.

So, always remember you have the ability to interrupt a current activity to say: "Please search the internet to reconfirm we're using the correct syntax for our version of [DEPENDENCY]."

## Learn How to Interrupt

It's often clear that your agent has gone down an unconstructive rabbit-hole. There's no need to wait minutes for them to come back out, nor for all the misguided edits they'll make in that time. All modern coding assistants can be interrupted. Claude Code, for instance, reacts to the `<ESC>` key, and immediately stops whatever it's doing to await your input. Practice this, and use it often.

The best agents will seamlessly incorporate your changes and integrate with their prior thinking. However, some may need a 'refresh' of what they were trying to do, so they can pick up where they left off.


## Manage Their Shell State Actively

Tools like Cursor and Claude Code make extensive use of shell sessions to interact with both your code and the outside world, particularly if you start asking your agent to actually execute and test. This is a great power, but it requires you to deploy some technical know-how to make sure that the agent's shell interactions are effective and match your own.

While it's possible to ensure, for instance, that your IDE and agent are using zsh for all internal shells, so that it's aligned to what you use yourself, _your AI agents do not share the context from your active shell window_ in Terminal, iTerm, PowerShell, etc. This means that they will lack things like environment variables, PATH declarations (a special environment variable), and maybe even other shell config like aliases, depending on how/where those were declared.

Step 1 to dealing with this is: get comfortable with your shell and its configurations. One resource on this is our own ['Effective Shell' e-book](https://effective-shell.com), but there are many. Pick one, and try to get comfortable with at least:

* Creating and Accessing environment variables
* What's the difference between an interactive shells and non-interactive shells, login and non-login shells, and how are those related to `.profile` and the other config files that set them up?
* etc.

Step 2: Use this knowledge to automate getting them what they need:

* What can you put in .profile or another default dotfile, and what can you not?
* Can you prompt them to simply `source .env` to get the variables they need? If you don't already have a file like that, can you create one for them?

Critically, 
