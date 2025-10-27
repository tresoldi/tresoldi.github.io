---
layout: post
title: "Before the Priors: On the Trees We Think With"
date: 2025-10-15 08:00:00 +0200
tags: [bayesian inference, stemmatology, historical linguistics, methodology, phylogenetics]
---

I am old enough to have worked on a research project that used expert systems. Not machine learning, not neural nets, but *if-then-else* logic multiplied by the hundreds. We were building a linguistic engine: thousands of lexical entries, dozens of statistical checks, and then layer after layer of hand-crafted rules. It was closer to watchmaking than to factory production. The system worked. Slow, but transparent. You could point to any given behavior and say: this happens because of this rule. You could test a single condition, rewrite it, watch the effects ripple through.

Looking back, we were at the edge of what would become standard machine learning, with decision trees written by humans instead of gradient descent. We had all the ingredients: data, statistics, feedback loops. The professor leading it preferred transparency over black-box elegance (and we are talking about mid-2000s, where this was hardly a topic in that field). The goal was to understand, not just to predict. He was right. The work never got published and is surely lost -- he passed away almost a decade ago -- but I learned more from those hand-written rule cascades, which also involved an embrionary machine-translation system, than from any parameter-optimized model I've built since.

## The Comfort of the Tree

In stemmatology and especially in historical linguistics, our trees have become too comfortable. We load data into BEAST2 or MrBayes, set the priors to "uninformative" (already a choice, not neutral), and wait for the MCMC sampler to decide what history looked like. Science by delegation, the kind Lem and other good scifi authors warned about: we build the oracle and then ask it to tell us what we already decided to believe. A ritual where we submit to the random walk, our computational *sortes*, and call the output inference.

We get our trees, our posterior probabilities, our summary statistics. But something essential goes missing. The hermeneutic act, the human work of deciding what counts as plausible ancestry, has been quietly exiled to .xml files that are acknowledged but never consulted. It doesn't help that BEAUTI, the tool BEAST2 offers to create models, cannot read the models it generates. You can only cast the spell once.

The algorithm is Bayesian, absolutely. The researcher often isn't. True Bayesianism, in the older philosophical sense, was about belief revision. Gadamer understood this better than most statisticians: we come to every act of interpretation with *Vorverständnis*, with pre-understanding, with prejudice. The hermeneutic circle is Bayesian before Bayes. You start with what you expect, you encounter the data, you revise. The circle closes when your horizon of expectation and the horizon of the text fuse, when prior and evidence speak the same language.

What we do instead is start from uniform ignorance and call it unbiased objectivity. That's not Bayesianism. It's refusal to commit. Pretending we approach the past without prejudice, when we've already made the consequential choices: what to code as a character, what to treat as missing, what substitution model to use, whether change is symmetric or directional.

## On Asymmetry and Forgetting

As I seem bound to repeat in every post, linguistic and cultural evolution is not symmetric. The probability that /p/ becomes /f/ is not the probability that /f/ becomes /p/. Languages lose grammatical gender far more easily than they gain it. Manuscripts accumulate scribal errors. Entropy works on vellum as it works on everything: one direction, downhill.

In stemmatology, "changes" are "errors." Lachmann knew it. Maas knew it. Even Bédier, who spent a career arguing against Lachmann's binary fetish, never disputed the directionality of error. When you're reconstructing a stemma from manuscript witnesses, you work from the assumption that innovation is directional. A scribe introduces an error; that error propagates to descendants unless actively corrected by another scribe, whether returning to the original or introducing a new corruption. The *lectio difficilior* principle rests on asymmetry: scribes simplify, normalize, corrupt. They do not, as a rule, complexify or archaize spontaneously. You can trace contamination, horizontal transmission, but even contamination has a direction. The borrowed reading flows from one witness to another, not simultaneously in both directions.

Yet the computational models we use, for convenience, for legacy code, for mathematical tractability, start from symmetry. Every character state change is equally probable until the data "teach" the model otherwise. But that's already an epistemic choice: to erase directionality, to flatten time, to pretend evolution is a random walk in an undirected graph. When we treat evolution as symmetric, we're not being neutral. We're imposing a world where all paths are reversible, where history has no preferred direction. This is not Bayesianism. It's refusal to let our understanding of the process inform the inference.

## Opacity Versus Understanding

The story of expert systems is the story of all AI: the move from understanding to automation, from clarity to scale. From LISP machines in university basements to cloud GPUs training on the entire web. When my professor chose rules over weights, he was choosing interpretability over elegance, symbolism over connectionism, the kind of choice Fodor and Pylyshyn were still arguing about when the debate had already been lost. Scholastics arguing fine points on the sex of the angels while the printing press was being built down the street. He was choosing to know *why* something worked, even if it meant the system was slower, more brittle, harder to extend.

Machine learning gives us results, often impressive ones. But in historical linguistics and stemmatology, we're not chasing performance metrics. We're reconstructing stories -- divergence, contact, drift, innovation, scribal error, contamination. Our job is not only to model change but to understand it.

When I see a Bayesian phylogenetic tree, I think of the old expert system. It was maddeningly slow to maintain, but interpretable to the bone. You could ask *why* it thought something, and it would show you the chain: this rule fired, which triggered this condition, which led to this conclusion. A tree built by BEAST2 with the standard approach gives you posterior probabilities and an apologetic shrug.

The opacity of parameter explosion -- the thousands of substitution rates, the clock models, the priors nobody revises because the default worked well enough last time -- is not just technical nuisance. It's epistemological surrender. We've built systems that simulate belief without ever making us articulate it.

The stemmatological tradition understood this. Debate over a stemma was debate over assumptions: should we privilege *usus scribendi*? How much weight do we give to geographical distribution of manuscripts? When is a shared error conclusive evidence of filiation, and when might it be polygenesis? These aren't questions you answer by adding more data. You answer them by clarifying your pre-understanding, by making the hermeneutic circle explicit.

We've lost that in computational phylogenetics. We treat the addition of more characters, more taxa, more parameters, more priors, more constraints as if it solves the interpretive problem. It doesn't. It buries the text under the apparatus.

## Few Characters, Deep Priors

This isn't nostalgia, also because there is no golden age to yearn for. It's a reminder that scientific insight does not scale linearly with data. Sometimes it scales with understanding. Sometimes you learn more from thirty well-chosen features and a defended set of directional priors than from five hundred binary characters dumped into a likelihood function.

Maas built stemmata by hand, from diagnostic errors. Champollion worked with fragmentary inscriptions. Ventris cracked Linear B with a grid and educated hunches. They succeeded with understanding, not data. I am not arguing against statistical approaches: language models, diffusion systems, machine translation all prove that when you have enough data, interpolation in high-dimensional space works beautifully. But that is precisely the point: *when you have enough data*. In small datasets, in historical linguistics, in stemmatology, we cannot generalize through interpolation of known points in multivectorial space. We are not smoothing over a manifold. We are reconstructing from fragments, the way you reconstruct a temple from scattered stones or an entire dinosaur from a broken tooth. That requires a different epistemology.

I think a lot about what Billing & Elgh (2023) did for Anatolian historical linguistics using parsimony, in the work they presented in Heidelberg and that made its way to Oscar's thesis. They worked with very few characters, chosen not for bulk but for phylogenetic signal, and crucially, they used an asymmetric weighting matrix that recognized change has direction. The work breathes understanding. It doesn't drown the signal in hundreds of features hoping something floats to the surface. It starts from the idea that data is fragile, that modeling them well is itself an act of interpretation.

Erik would say this contradicts the spirit of parsimony, that going "full Bayesian" misses the point, that their approach is what biologists were doing fifty years ago when genetic data was a dream and the best you had was a handful of morphological characters. He's probably right in his own frame. But I can't help wanting a Bayesian system in that same spirit -- not in the mechanical sense of running MCMC until convergence, but in the philosophical sense of making expectations explicit, of treating priors the way humanists treat footnotes: each one an argument you're willing to defend in the apparatus.

We do this already in stemmatology, though not always computationally. When you build a stemma by hand, you decide: this reading is prior, this one is derived. You argue for directionality. You defend why manuscript A could not have descended from manuscript B based on what you know about scribal practice, about dialect, about paleography. That argumentation is your prior. The Gadamerian pre-understanding you bring to the text. Morelli did this for art history, reading the diagnostic details -- how an ear was painted, how drapery folded -- to reconstruct attribution. We do it for linguistic change and scribal habits.

We can do the same, but computationally. Bayesian inference is not antithetical to humanistic scholarship. It's hermeneutics formalized. Priors are *Vorverständnis* made explicit. Posterior distributions are revised belief. The fusion of horizons, rendered probabilistic. Gadamer with a likelihood function.

## What We Should Build Instead

The system I imagine -- and which I have been very slowly developing for the past years -- is not large or fancy. It won't outperform BEAST2 (it's written in Python, it doesn't even use Beagle). It won't scale to thousands of data points. It will aim to teach us to think Bayesianly, to make every choice, every prior, every assumption about directionality or missing data, visible and contestable.

What I want is a tool where you write priors like you write critical apparatus: as interpretive gestures that others can contest. Where you can change a prior -- say, assign higher probability to loss of the Greek dual than to its spontaneous re-emergence -- and see immediately, visually, what that belief revision does to the tree, to the reconstructed readings, to the dating of splits. Not a black box. An interpretive instrument, something closer to the memory theaters of Renaissance hermeneutics than to a statistical package. A structure that externalizes thought so you can examine it. Something you can play with, setting absurd values to see how they bend history.

Instead of throwing hundreds of poorly understood characters at a sampler, you'd choose a few that carry real phylogenetic signal, and weight them in terms of confidence: a sound correspondence you understand, a morphological innovation with clear directionality, a syntactic shift whose path you can defend. In stemmatology: a significant error, a transposition, a gloss incorporated into the text. Each with a prior you can argue for, a direction you can justify. Every prior is a wager on how the world works.

Not a black box, amirror -- Perseus's polished shield, a surface that lets you see what you couldn't look at directly. The criticism will come: this just reifies the researcher's biases, it only shows what you already believed. But the goal is exactly to make those biases explicit, not to hide behind the supposed agnosticism of the Bayesian package we downloaded, as if our poor choices would be refined and corrected by sheer volume of data, by the model's capacity to "learn."

Gadamer knew: you can't escape the hermeneutic circle. You come to understanding through pre-understanding. The question is whether you acknowledge it, whether you make it part of the interpretive work, or whether you pretend to a view from nowhere.

## After the Tree

I have done my share of Bayesian phylogenetics, including the forthcoming paper on Arawan. When I look at a tree of languages, or a stemma of manuscripts, I don't see branches and nodes. I see the ghosts of choices -- what was coded as a character, what was ignored, what was treated as symmetric or directional, what prior was set to uniform out of convenience or principle.

Every reconstruction carries the shadow of its method. Every tree is an argument, not a discovery. The data doesn't speak for itself. We speak through it, and the models we build are the grammar of that speech.

The true Bayesian spirit is not in letting the chain converge. It's in watching how our beliefs change as we revise them, as we bring them into contact with evidence, as we test what our assumptions entail. That's what Gadamer meant by the hermeneutic circle. That's what science is. That's what history is.

We need tools that make that process explicit and I am trying to build one. Fewer characters, deeper priors, asymmetric by default, interpretable to the bone. A system where you can argue with the model the way you argue with a text, where every assumption is a footnote waiting to be challenged.

The trees we think with should show us how we think. We shape our models, and thereafter our models shape what we can see.
