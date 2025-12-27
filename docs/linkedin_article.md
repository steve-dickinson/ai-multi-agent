# 🤖 I Built an AI Newsroom (So I Could Argue With It)

I’ve spent the last few days running an experiment. My goal wasn't just to build a tool, but to answer a question: **"Where do AI Multi-Agent systems actually fit in the real world?"**

We know monolithic LLMs (like ChatGPT) are jacks-of-all-trades. But complex workflows, like government content publishing,require specialists.

So, with a little help from Google Antigravity to handle the wiring, I set out to test the power of **Specialised AI Agents**. Could I build a digital team where each agent has a distinct role to manage complex environmental guidance?

## 🎭 The Solution: A Team of Specialists

The result is a production line powered by **LangGraph** & **Python 3.13**. Here's how it solves real problems:

### 1. The "Messy Middle" Problem
Updating guidance is hard when the source material is everywhere, PDFs, emails, legal texts.
**The AI Solution:** Use an **Ingest Agent** that unifies the input. It scrapes live content from URLs, fetches structured pages from the GOV.UK API, or accepts raw text, normalising everything so the team can start working immediately.

### 2. The "Blank Page" Syndrome
Starting a new guide for a "Grant" is daunting.
**The AI Solution:** The **Content Architect** doesn't guess. It uses the official "Start Page" template to structure the user needs first—"Check eligibility" -> "What you can buy" -> "How to claim"—ensuring the "Apply" button isn't buried at the bottom.

### 3. The Quality Bottleneck
Before we get to the nuance, someone has to check the basics: Style Guide compliance, structure, and readability. It's necessary but tedious.
**The AI Solution:** The **Core Review Engine**. Every piece of content goes through a rigorous, automated critique *before* a human sees it. It flags specific issues: "You used 'dispatch' instead of 'send'" or "This paragraph fails the inverted pyramid test". It handles the hygiene factors so humans can focus on the message.

### 4. The Tone War
How do you balance clarity with legal accuracy on a topic like "Nutrient Neutrality"?
**The AI Solution:** A **Debate Club**. We pit a "Simplifier" agent (who hates jargon) against a "Legalist" agent (who fears lawsuits). A "Mediator" synthesises their arguments into a draft that is legally precise but readable. **Iron sharpens iron.**

### 5. The Silo Problem
It's easy to write advice that unintentionally contradicts another department (eg. Forestry vs Peatland policies).
**The AI Solution:** The **Silo Breaker**. It searches a vector database of *all* cross-government policies in real-time. If you tell users to plant trees where Natural England says "Stop", it flags the conflict immediately.

### 6. The "Curse of Knowledge"
We often forget how confusing our content is for a user (like a skipper checking fishing quotas at sea).
**The AI Solution:** The **Persona Lab**. We simulate an "Anxious User" trying to read the content. If the agent can't find the answer because of complex language or missing references, it fails the test, forcing us to fix it before a human ever sees it.

## 🔮 What's Next? (The Feature Wishlist)
This is just the MVP. Here is where the functionality could go next:
*   **Tone Heatmaps**: Visualizing Passive Voice in <span style="color:red">red</span> directly on the canvas.
*   **Multi-Modal Review**: Agents that can "see" images in PDFs and check alt-text.
*   **Chat Interface**: Moving from a dashboard to a Slack/Teams bot. Imagine just tagging `@ConsistencyAgent` in a thread.

## 🚀 The Verdict: Empower, Don't Replace
What I learned is that AI agents don't replace the need for human strategy. They automate the **drudgery**. By handling the style checks and consistency searches, they free up content designers to do what they do best: **Strategy. Empathy. Nuance.**

Check out the code:
🔗 [GitHub Repo Link]
🔗 [Documentation Site Link]

#AI #LangChain #LangGraph #Python #Defra #GovTech #GenerativeAI

---
*Disclaimer: This is a personal experimentation project to explore the capabilities of AI agents in content workflows. It is not an official tool and is not currently in use by any department.*
