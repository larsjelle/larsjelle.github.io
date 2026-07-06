---
title: "Giving Claude Code a long-term memory with MemPalace"
date: 2026-06-29
categories:
  - Tech
  - AI
tags:
  - mempalace
  - claude-code
  - mcp
  - ai-memory
  - self-hosting
excerpt: "AI agents forget everything between sessions. I fixed that with MemPalace: a local, offline memory system that seeded itself from months of my old Claude conversations. Why I picked it over Mem0 and friends, and how to set it up."
author: Lars van Blitterswijk
draft: false
---

*Same deal as always: real setup, really running on my machine, drafted with AI from my own session logs and reviewed by me.*

In [my AI tooling post](/posts/my-ai-tooling-setup-claude-code-and-agent-of-empires) I called memory the honest limitation of agent workflows. Two weeks later I got fed up enough to fix it.

The trigger was catching myself explaining, for the fifth time, that my Proxmox host is the NUC, that n8n runs in its own container, and that no, the Tailscale names are Cloudflare DNS records and not MagicDNS. Every new Claude Code session is a new hire on their first day. Smart, capable, knows nothing about the building.

![Claude Code through the MemPalace MCP server to a local palace store, seeded from past conversations](/img/posts/giving-claude-code-a-memory-with-mempalace.svg)

## What I actually wanted

Before shopping around I wrote down requirements, which I recommend, because the AI memory space is full of shiny things:

- **Local and offline.** My memories include my network layout, my automations, my household. That does not go into someone's cloud.
- **No API key, no extra LLM bill.** Memory writes and searches happen constantly; I don't want a meter running.
- **MCP native**, so Claude Code can read and write memories itself as part of normal work.
- **Able to bootstrap from history.** I had months of Claude Code session logs sitting in `~/.claude/projects`. A memory system that starts empty ignores the best data I have.

I sent an AI research agent out to compare the field properly. The short version: **Mem0** is the most popular and fastest to integrate, but shines brightest as a hosted platform. **Zep/Graphiti** is built around temporal knowledge graphs, great when "what was true when" matters. **Letta** (the MemGPT lineage) wants to own the whole agent runtime. All credible, none a clean match for local-first, key-free, seed-from-my-own-logs.

**MemPalace** matched on every point. It's open source, runs entirely offline with local embeddings, needs no API key, ships an MCP server, and, decisively, has a mining command built exactly for ingesting existing Claude conversation logs.

## The memory palace idea

MemPalace organizes memories the way the ancient mnemonic technique does: a palace with **wings** (broad domains), **rooms** (topics), and **drawers** (individual memories). Search is semantic, so "why did we move n8n off the tunnel" finds the drawer about that decision even though no keyword matches. Under the hood it's SQLite plus a local vector store with a small embedding model; nothing phones home.

The structure sounds like a gimmick until you watch an agent use it. Memories about my infrastructure live apart from memories about my preferences, and the agent can browse ("what rooms exist in the infrastructure wing?") as well as search.

## Setup, start to finish

This took me under half an hour, most of it watching the miner work.

**1. Install and initialize:**

```bash
pipx install mempalace
mempalace init
```

`init` builds the palace structure (mine lives at `~/.mempalace/palace`) and scans your files to propose an initial taxonomy. It correctly guessed my world before I told it anything: it pulled Proxmox, Tailscale, Cloudflare and Telegram out of my existing notes as entities worth tracking.

**2. Mine your history.** The magic step:

```bash
mempalace mine ~/.claude/projects --mode convos --agent claude
```

This chewed through 107 conversation files from my Claude Code history and filed the durable facts into the palace. First run downloads a small embedding model (about 80 MB), then everything is local. When it finished, my agent's memory already contained the container inventory, the DNS decisions, the abandoned experiments. Months of context, recovered from logs I'd never have reread manually.

**3. Wire it into Claude Code:**

```bash
claude mcp add mempalace -- mempalace-mcp
```

That exposes about 19 tools to the agent: search, browse the taxonomy, add memories, write session checkpoints, and so on.

**4. Teach the agent when to use it.** This is the step most people skip and then wonder why nothing changed. I added a section to my global `CLAUDE.md` that says, roughly:

- Before answering anything about my setup, past decisions, or preferences: **search the palace first**, don't guess.
- When a durable fact or decision emerges in a session: **store it** (and check it isn't already there).
- At the end of a substantial session: **write a checkpoint**.
- Never store secrets or credentials.

**5. Keep it fed.** New conversations accumulate, so occasionally I re-run the mining command over recent logs. Same command, it deduplicates.

## Does it work?

The test I did right after setup: opened a completely fresh session and asked "what do you know about my reverse proxy setup?" It answered with the NPM container, the wildcard certificate, the grey-cloud Cloudflare gotcha, and cited which memory it pulled each fact from. First day on the job, already knows the building.

If you run Claude Code or any MCP-capable agent and you're tired of being the memory yourself, this is a genuinely satisfying weekend upgrade. Total cost: zero, and your data never leaves the machine.
