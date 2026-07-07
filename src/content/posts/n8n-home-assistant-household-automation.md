---
title: "n8n + Home Assistant: a household agent for groceries, dinner plans and heat warnings"
date: 2026-07-04
categories:
  - Homelab
  - Automation
tags:
  - n8n
  - home-assistant
  - telegram
  - nextcloud
  - llm
  - smart-home
excerpt: "Two real systems from my house: a Telegram agent that manages our shopping list, dinner planning and projects, and a heat advisory workflow that predicts how hot the upstairs will get and learns from its own mistakes. Architecture, gotchas, and how to build your own."
author: Lars van Blitterswijk
draft: false
---

*These systems were designed and built in conversation with Claude Code, which has direct access to my n8n and Home Assistant through MCP. This post was drafted the same way, from the actual build logs, and reviewed by me.*

Home Assistant is great at reacting: motion means light, door open means notification. Where it gets clumsy is anything that needs state over time, external APIs, language understanding, or logic you'd rather write as a flow than as YAML. That's the gap n8n fills in my house. HA is the eyes and the screen; n8n is the brain.

Both run on my Proxmox box (HA as a VM, n8n in a container), both reachable only over Tailscale. That constraint shapes the architecture in a useful way, as you'll see.

Two systems came out of this combination, one mundane and one nerdy.

![Telegram to n8n to Nextcloud and Home Assistant, all self-hosted on Proxmox behind Tailscale](/img/posts/n8n-home-assistant-household-automation.svg)

## System 1: the household agent

Shopping lists, dinner ideas, chores and "we should really fix the gutter" all live in different apps, or in nobody's head. My requirement was a system my girlfriend would actually use, which rules out anything that needs opening the right app in the right mode.

What we ended up with: a **Telegram group chat with a bot in it**. You type like you'd type to a housemate:

> "we're out of olive oil and we should book the electrician for the kitchen"

and the bot splits that, puts olive oil on the shopping list, drops the electrician on the renovation board, and replies with what it did. The pieces:

**Storage is Nextcloud, not a custom database.** Shopping list, chores and an inbox are Nextcloud Tasks lists (CalDAV under the hood). Bigger projects are Deck boards. Dinner planning is a "Meals" calendar, and recipes live in Nextcloud Cookbook. Open standards pay off twice: any CalDAV app can see the lists, and Home Assistant has native integrations for both to-dos and calendars, so everything shows up in HA for free.

**n8n is the middleman.** A workflow polls Telegram, feeds new messages to an LLM that classifies and extracts items, writes to Nextcloud via CalDAV and the Deck/Cookbook APIs, and replies in the group. When the agent needs a decision ("I found three curry recipes, which one?") it renders the options as inline keyboard buttons, so answering is one tap.

**The display is a Home Assistant dashboard.** A "household planner" dashboard shows the shopping list, chores and the dinner week at a glance, on the wall tablet and in the HA app. Keep the roles separate: chat is for *doing* things, the dashboard is for *seeing* things. That separation is what made the system stick.

**The clever bit: purchase memory.** Every item checked off the shopping list is logged to an n8n data table. When meal planning adds ingredients for a recipe, the workflow skips things bought in the last week and pantry staples, and mentions the skip ("you bought parmesan on Tuesday"). This removes the main annoyance of automated shopping lists: they don't know what your kitchen already contains.

**The gotcha worth stealing: outbound-only Telegram.** The standard way to run a Telegram bot is a webhook, but my n8n is tailnet-only, so Telegram can't reach it, and I wasn't going to open a hole for it. The solution is the `getUpdates` API in long-polling mode: a schedule fires every 30 seconds and holds a request open for 25, so Telegram delivers messages into the open connection nearly instantly. Sub-second response latency, zero inbound exposure, no tunnel. If you self-host behind a VPN, this pattern applies to far more than Telegram.

## System 2: the heat advisory that learns

Dutch houses are built to keep warmth in, which is lovely for nine months of the year. During the heatwave of 18 to 27 June our upstairs hit 36°C in the bedroom, and at night it was still 31°C inside while the outside air was 21°C. All that cool air, unused, because you never know in the morning whether today is a "close everything at 10:00" day or a "doesn't matter" day.

So we built a workflow that tells us. Every morning at 06:45 the household group gets a message like: predicted upstairs max 31°C, tier "hot", ventilate fully until 09:00, then close windows and blinds upstairs, open up again after 21:00. Quiet days produce no message at all, because a bot that pings you daily gets muted by week two.

Under the hood it's four scheduled branches in one n8n workflow:

1. **06:45, the advice.** Pull today's forecast (temperature and solar radiation) from the free Open-Meteo API, read the current per-room temperatures from our Tado radiator thermostats via Home Assistant, and predict today's upstairs maximum with a small linear model. Above the "warm" threshold it messages Telegram; either way it always writes the advice to a persistent notification in HA.
2. **19:30, the heads-up.** Looks a week ahead and warns once (deduplicated) when a stretch of two or more hot days is coming, so we can prepare.
3. **Hourly, the sampler.** From 08:00 to 23:00 it records the actual indoor peak of the day into a data table.
4. **23:30, the learning loop.** Compares this morning's prediction with the day's measured maximum and nudges the model weights (a normalized least-mean-squares update). Wrong predictions literally teach the model.

The model itself is deliberately tiny: predicted indoor max is a weighted sum of forecast outdoor max, total solar radiation, and the indoor temperature that morning. No neural anything. I seeded the weights by regression over 18 real hot days pulled from Home Assistant's long-term statistics matched against Open-Meteo's historical archive, which got the average error down to about 0.6°C before the online learning even starts. A three-coefficient model you can read beats a black box here: when it's wrong you can see why.

## The patterns underneath both

If you want to build in this direction, the reusable ideas are these:

- **HA senses and displays, n8n thinks.** Don't force complex logic into HA automations, and don't make n8n talk to Zigbee. Each tool where it's strong.
- **n8n data tables are your state.** Model weights, purchase history, dedup flags, bot offsets. No extra database needed.
- **Open standards for storage.** CalDAV lists and calendars mean HA, phones and bots all see the same truth with zero custom sync code.
- **Outbound-only everything.** Long-poll instead of webhooks and none of your automation needs to be reachable from the internet.
- **Prefer silence.** Notify on threshold, not on schedule. The heat bot's best feature is the days it says nothing.
- **Let an AI agent do the n8n clicking.** Describing the workflow to Claude Code with an n8n MCP server attached and reviewing what it deploys is faster than building nodes by hand, and it writes the validation logic you'd skip.

The unglamorous truth is that the household agent gets used more than any other automation I've built, and it's mostly a shopping list. Build for the boring case first; the machine-learning weather model can come after.
