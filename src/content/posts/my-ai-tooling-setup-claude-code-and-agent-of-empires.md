---
title: "How I actually work with AI: Claude Code, MCP servers and Agent of Empires"
date: 2026-06-14
categories:
  - Tech
  - AI
tags:
  - claude-code
  - agent-of-empires
  - mcp
  - ai-agents
  - tmux
  - workflow
excerpt: "My day-to-day AI setup: Claude Code as the workhorse, MCP servers to give it hands, and Agent of Empires to manage multiple agent sessions from a terminal or my phone. What works, what my rules are, and how to set it up."
author: Lars van Blitterswijk
draft: false
---

*Fair warning that applies to this whole blog: I use AI heavily, including for drafting these posts from my own notes and terminal history. The setup described here is what I actually run, and I've verified every command before publishing.*

A year ago "using AI for code" meant a chat window and a lot of copy-pasting. My current setup looks nothing like that. The AI lives in my terminal, has direct access to my Home Assistant, my n8n instance and my Proxmox host, and I can check on running agent sessions from my phone while walking the dog. This post is the tour.

## The core: Claude Code

Claude Code is Anthropic's terminal agent. You type what you want, it reads files, runs commands, edits code, and shows you diffs. That description undersells it. The real shift is that it operates on *your actual system*: it can SSH into my Proxmox host, inspect a failing container, and fix the config, all in one conversation.

My working rules, learned the mildly painful way:

1. **Plan first, then execute.** For anything non-trivial I make it lay out a plan before touching anything. Reviewing a plan takes a minute. Reviewing a surprise 40-file change takes an hour.
2. **Everything in git.** Not just code: my Home Assistant configs, my infrastructure notes, this website. If the agent can commit it, the agent can also revert it.
3. **Small sessions, clear goals.** "Fix the backup timer on the Proxmox host" beats "improve my infrastructure". Agents are like contractors: vague briefs produce confident nonsense.
4. **Read the diff.** Always. The one time I skipped this it "cleaned up" a workflow that was intentionally weird.

## Giving the agent hands: MCP servers

Out of the box an agent can run shell commands. The Model Context Protocol (MCP) is how you give it proper tools for specific systems. Each MCP server exposes typed operations the agent can call, which beats having it curl JSON APIs blind.

What's wired into my setup:

- **Home Assistant MCP**: the agent can query entities, inspect automations, check logs. "Why did the hallway light not turn on last night" is now a question I ask in plain text and get a traced answer to.
- **n8n MCP**: it can search nodes, validate and deploy workflows. More on what we build with that in a future post; it has become the backbone of my home automation.
- **Playwright MCP**: browser control, mostly for testing web UIs it just built.

Registering one is a single command:

```bash
claude mcp add home-assistant -- npx some-ha-mcp-server
```

If you self-host anything, this is the unlock. The difference between an agent that can "write YAML that might work" and one that can call your actual API, see the actual error and iterate, is night and day.

## The multiplexer: Agent of Empires

Once agents get useful, you stop having one conversation. You have the session refactoring a workflow, the session investigating a Zigbee problem, and the session doing research, all at different stages of needing you. Keeping those in raw terminal tabs falls apart fast.

[Agent of Empires](https://github.com/agent-of-empires/agent-of-empires) (`aoe` on the command line) is an open source manager for exactly this. It sits on top of tmux and gives you:

- A **TUI dashboard** listing all your agent sessions and their status, so you can see at a glance which one is waiting for input.
- **Multi-agent support**: it auto-detects what you have installed. Claude Code and OpenCode, but also Codex CLI, Gemini CLI and a long list of others. Same cockpit regardless of vendor.
- A **web dashboard** (`aoe serve`) with a mobile-friendly view, including rendered plans and diffs.

Install and run:

```bash
brew install aoe    # or the curl installer from the repo
aoe                 # TUI
aoe serve           # web dashboard
```

The web dashboard is the sleeper feature. Mine is served over my Tailscale network with a proper domain, using exactly the reverse proxy setup from [my earlier post](/posts/tailscale-nginx-proxy-manager-cloudflare). Kick off a long-running task at your desk, then approve the plan from your phone in the supermarket queue. It sounds like a gimmick. It is not. Agent work is bursty, you're needed for thirty seconds every ten minutes, and being able to answer from anywhere means the work doesn't stall.

Since sessions run inside tmux, nothing dies when I close my laptop; I attach from another machine and everything is still there.

## The honest limitations

Two things keep this from being fully magic.

**Memory.** Every session starts blank. Claude Code reads a `CLAUDE.md` file per project, and I maintain markdown notes it can consult, but the agent that debugged my network last week has no recollection of it this week unless I paste the context back in. Per-project notes don't cross projects either, and my homelab is one big interconnected project. I'm actively looking for a proper solution here; when I find one that works it'll get its own post.

**Trust calibration.** The failure mode of these tools is not incompetence, it's confident half-correctness. The rules above (plans, git, small scopes, read the diff) exist because I violated each of them exactly once.

## Where to start

If you want to try this shape of working: pick one agent CLI and use it for a week on a low-stakes repo before adding anything else. Then add one MCP server for a system you actually run; that's the moment it clicks. Only reach for Agent of Empires once you catch yourself juggling multiple sessions, because that's the problem it solves, and by then you'll know exactly why you want it.
