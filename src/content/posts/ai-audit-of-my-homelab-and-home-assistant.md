---
title: "Spring cleaning with an AI agent: mapping my network and auditing Home Assistant"
date: 2026-06-13
categories:
  - Homelab
  - AI
tags:
  - home-assistant
  - claude-code
  - homelab
  - documentation
  - smart-home
excerpt: "I pointed an AI agent at my homelab and asked two things: draw me the real network topology, and tell me what's broken in Home Assistant. Here's the process, and why an audit beats new features."
author: Lars van Blitterswijk
draft: false
---

*You know the drill by now: real sessions, real findings, drafted with AI from the logs, checked by me.*

Every homelab reaches the same middle age. Things mostly work, nobody remembers exactly why, and the mental map of what talks to what lives in one person's head, incompletely. This week I gave an AI agent read access to everything and asked it to tell me the truth.

Two exercises, one day, both worth stealing.

![Homelab topology: phone over Tailscale to the Proxmox host and Raspberry Pis, with Home Assistant running 900+ entities](/img/posts/ai-audit-of-my-homelab-and-home-assistant.svg)

## Exercise 1: "draw me my actual network"

The prompt was close to literal: give me the ultimate overview of my network topology and every running service. The agent had SSH to the Proxmox host and API access to my UniFi controller and the services themselves, and it went spelunking: every LXC container and VM, the several Raspberry Pis I'd half forgotten about, which reverse proxy fronts what, which DNS name points where, how traffic actually flows from my phone on the train to a container in the closet.

The output was a set of diagrams plus a written inventory, and the value wasn't beauty, it was *disagreement*. The map in my head and the map in reality differed in a half-dozen places. A service I thought was tailnet-only had a second, older route. Two things depended on a Raspberry Pi I'd been planning to retire.

If you self-host anything, I now think this is the single highest-value thing to do with an AI agent, before any building. Documentation a human writes goes stale the week after. Documentation an agent *derives from the live system* is checkable, repeatable, and embarrassing in the most useful way.

## Exercise 2: the Home Assistant confession

Then I turned the same approach on Home Assistant, which had grown for years without adult supervision: 900-plus entities across 29 domains. I asked for a full audit. Rooms, devices, automations, dashboards, integrations, everything, with a verdict per item.

The agent fanned out and came back with a report that was hard to argue with:

- **77 sensors unavailable and 51 stuck on "unknown"**, most of them for months. Ghost entities from removed devices, mostly, but hiding among them were real faults.
- **Real faults I'd stopped seeing**: my Zigbee battery sensors (door sensors, a dimmer) had silently been offline for three weeks. The doorbell's motion sensor, dead since April. An add-on erroring on every boot.
- **Three broken automations**, one throwing a repair warning I had trained myself to scroll past.
- **34 dead Philips Hue scenes** referencing lights that no longer exist, which it correctly noted can only be deleted from the Hue side, not from HA.
- **Structural mess**: duplicate areas, a duplicate dashboard, entities assigned to rooms that didn't match physical reality.

Then, and this is the part that separates an audit from a lecture, we fixed it together in the same session: areas consolidated into nine clean rooms across two floors, the dead automations and duplicate dashboard removed, a new floor-based dashboard built, and every finding logged to a markdown file in git so the next audit has a baseline.

## How to run this on your own setup

The recipe generalizes:

**1. Give the agent real access, read-only where possible.** For Home Assistant there are MCP servers that expose entities, automations and logs to Claude Code or similar agents. For the network layer, SSH access to the hypervisor gets most of the way.

**2. Ask for a map before asking for fixes.** "Document what exists and how it's connected" is a task agents are exceptionally good at: exhaustive, boring, and verifiable. Make the output a file in a git repo.

**3. Ask for verdicts, not summaries.** The prompt that worked was not "describe my setup" but "go through everything and tell me: keep, broken, or remove". Force a stance per item.

**4. Fix in the same session, log everything.** Findings decay fast. We went from report to repaired in one sitting, and the audit file records both what was found and what was done, which turns next year's cleanup from archaeology into a diff.

## The takeaway

None of what was found required intelligence to find. Every ghost sensor was visible in the UI the whole time. What was missing was *attention*: the willingness to look at 900 entities one by one, which no human with a day job possesses. That's the actual shape of what these agents are for right now. Not replacing your judgment, but applying your standards exhaustively to a system too big to hold in your head.

My smart home didn't get any new features this week. It got smaller, truer and quieter, and that felt better than a new feature would have.
