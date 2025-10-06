---
layout: post
title: "On Asymmetry and a New Measure"
date: 2025-10-06 08:00:00 +0200
tags: [asymmetry, computational linguistics, methodology, asymcat]
---

As part of my [`asymcat`](https://github.com/tresoldi/asymcat) library (which is required by my `malign` library and which supports a lot of my work and ideas on computational modelling of phonology and sound change) I have been working on a new measure for asymmetric categorical associations. But before I get to the technical details, let me indulge in what has become something of a Borgesian obsession: the problem of asymmetry in scientific thinking.

You know the type. Borges gave us the cartographers who drew maps at 1:1 scale until they covered the entire empire. I seem to have developed a similar condition, except my encyclopedic compulsion is to see asymmetry everywhere, to insist on its importance in every project, to refuse the comforting simplifications of symmetric thinking. It's a bit exhausting, honestly, and it has made publish less (not good) and get fewer requests to be a reviewer (perhaps not that bad). 

## The Undervalued Arrow

Here's the thing about asymmetry: it's everywhere, it's fundamental, and we keep ignoring it. Not universally, of course. Physics learned this lesson early with thermodynamics, where entropy gave us time's arrow, that irreversible drift toward disorder that makes the past distinguishable from the future. You can't unscramble an egg (at least, not without **a lot** of energy). The universe remembers which direction it's going.

Biology absorbed the lesson differently. Gould's thought experiment about rewinding the tape of life captured something essential: evolution is not a symmetric process that could run backward or forward with equal probability. If you rewound and replayed, you wouldn't get the same species, the same body plans, the same outcomes. History matters. Contingency matters. The path taken constrains the paths available. Information theory has known this from Shannon onward: channel capacity is asymmetric. The amount of information you can send from X to Y is not necessarily the same as from Y to X. The structure of the channel, the noise, the encoding possibilities, they all impose directionality on information flow. And in philosophy of science, causation itself is inherently asymmetric. Pearl, Woodward, the whole interventionist tradition: causes don't work backward. If X causes Y, that's a directional relationship. You can intervene on X to change Y, but not the reverse. Correlation might be symmetric, but causation never is.

Yet somehow, in computational historical linguistics and phylogenetics, we keep reaching for symmetric measures. We model relationships as if they could run equally well in either direction. We treat associations as undirected graphs when the linguistic processes we're studying, sound changes, lexical borrowings, morphological innovations, are all deeply, irrevocably asymmetric.

Maybe it's just easier. Symmetric measures are mathematically simpler. They fit into frameworks we already understand. They don't require us to think about direction, about before and after, about which thing influences which. But easier isn't the same as correct.

## The "Me" Measure

So, the measure. I've been calling it the Tresoldi measure for lack of a better name, though naming something after yourself always feels a bit presumptuous -- I promise to rename it to something adequare if anyone else ever uses it. It's an asymmetric association measure that combines information content with conditional probability to evaluate directional associations in categorical data.

The formula looks like this:

```
Tresoldi(X→Y) = sign(PMI) · |PMI(X,Y)|^(1 - P(Y|X))
```

Let me unpack that. The measure balances two different intuitions about what makes an association meaningful. On one side, you have **Pointwise Mutual Information** (PMI), which captures surprise, the degree to which two categories co-occur more or less than you'd expect if they were independent. PMI is about information content: how much does knowing X tell you about Y that you didn't already know?

On the other side, you have **conditional probability** P(Y\|X), which is about reliability. Given X, how often do you actually see Y? This is your standard maximum likelihood estimate, the empirical frequency of the association.

The clever bit, and pardon me being so self-congratulatory, is how these two components interact. The conditional probability acts as an exponent modifier on the PMI. When P(Y\|X) is low (the association is unreliable, you rarely see Y given X), the exponent (1 - P(Y\|X)) is close to 1, and the PMI gets dampened. When P(Y\|X) is high (the association is reliable, you almost always see Y given X), the exponent approaches 0, and you're left with something closer to the raw information content.

What this means in practice: rare but surprising associations get downweighted. Common and reliable associations get emphasized. The measure adapts dynamically based on how trustworthy the pattern is.

And crucially, it's asymmetric. Tresoldi(X→Y) is not the same as Tresoldi(Y→X). The directionality is baked in. If you're modeling sound changes, where /p/ regularly becomes /f/ but not vice versa, or grapheme-to-phoneme mappings, where <ch> maps to /k/ in some contexts and /tʃ/ in others, you need a measure that respects that asymmetry. Symmetric measures will mislead you. They'll tell you there's an association, but they won't tell you which way it points.

I've been writing up the [full technical documentation](https://raw.githubusercontent.com/tresoldi/asymcat/refs/heads/master/docs/TRESOLDI_MEASURE.md) with all the mathematical details, examples, and computational considerations. The measure is implemented in `asymcat`, which you can find on [GitHub](https://github.com/tresoldi/asymcat), and it's already doing work in my alignment and sound change modeling projects.

## Why This Matters

I realize this might seem like a small technical contribution, at most another measure in the toolkit. But I think it gestures toward something larger: the need to take asymmetry seriously as a foundational principle rather than an inconvenient complication. We build symmetric models not because the world is symmetric, but because symmetric mathematics is easier to work with. That's a choice, a somewhat lazy one, and it has consequences.

In historical linguistics, directionality is everything. Languages don't change randomly in all directions with equal probability. There are pathways, tendencies, preferences. Sound changes follow patterns. Morphological reanalysis goes certain ways and not others. If our methods can't capture that, if they treat forward and backward as interchangeable, we're missing the actual structure of the phenomena we're studying.

So yes, I keep coming back to asymmetry. In every project, in every library, in every method I develop. It's my Borgesian curse, I suppose: to see the thing that everyone else treats as a detail and insist that it's the whole point. Maybe I'm wrong. More likely, t's just another form of academic obsession. Call me Tiago.

But I don't think so. I think the world is asymmetric, and our models should be too.

Let's see how this one works out.
