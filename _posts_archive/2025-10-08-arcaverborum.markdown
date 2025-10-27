---
layout: post
title: "Arca Verborum"
date: 2025-10-08 14:00:00 +0200
tags: [arca verborum, data infrastructure, computational linguistics, lexibank]
---

There's a scene in *The Lifecycle of Software Objects* where Ted Chiang's characters debate whether their digital pets should live in optimized code or messy, human-readable structures. Speed versus comprehensibility, efficiency versus debuggability. [Arca Verborum](https://www.tresoldi.org/arcaverborum) is that choice made flesh in tabular format. There's a technical choice at the heart of it, and it's the wrong one by every database design principle: I took Lexibank's beautifully structured relational model and flattened it into single-file CSVs. Denormalization. Data people will wince. But here's the thing: when you're outside academia, when research happens in stolen hours, when you need to prototype a phonological model or test a sound change hypothesis before the day job reasserts itself, setup time is everything. There's not much time for relational schemas when you're programming via an SSH connection on your phone, waiting for the bus downtown.

I built this originally for teaching, but I'm the one who uses it most. Series A combines 149 datasets from Lexibank, 2.9 million forms in total, ready to use. You lose the elegance of the relational model, the integrity constraints, the clean separation of concerns but you gain speed. It is a pragmatic infrastructure, the scaffolding for the kind of work I am trying to do: modeling sound change, prototyping phylogenetic methods, building tools that need linguistic data. None of this could exist without Lexibank's extraordinary curatorial work, but I needed a different interface to that same foundation. Sometimes the wrong design is the right tool.
