---
abbreviations:
  FRX: Frictionless Research Exchange
---

# About Frictionless Data Exchanges

This page describes some of the background and inspiration for this project as defined in [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865).

## The core idea

In [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865), the author describes three key aspects of a Frictionless Data Exchange (FRX):

> The three initiatives are related but separate; and all three have to come together, and in a particularly strong way, to provide the conditions for the new era. Here they are:
>
> **[FR-1: Data] datafication of everything**, with a culture of research data sharing. One can now find datasets publicly available online on a bewildering variety of topics, from chest x-rays to cosmic microwave background measurements to uber routes to geospatial crop identifications.
>
> **[FR-2: Re-execution]** research code sharing including the ability to exactly re-execute the same complete workflow by different researchers.
>
> **[FR-3: Challenges]** adopting challenge problems as a new paradigm powering scientific research. The paradigm includes: a shared public dataset, a prescribed and quantified task performance metric, a set of enrolled competitors seeking to outperform each other on the task, and a public leaderboard. Thousands of such challenges with millions of entries have now taken place, across many fields.
>
> -- [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865)

Together, these three components provide a powerful framework for sharing and accelerating scientific discovery:

> We see a new institution arising spontaneously; let’s call it a Frictionless Research Exchange (FRX).
> FRX is an exchange, because participants are constantly bringing something (code, data, re- sults), and taking something (code, data, new ideas), from the exchange; and various globally visible resources - task leaderboards, open review referee reports - broadcast information to the whole com- munity about what works and what doesn’t. Of course, this is a very different type of exchange from those involved in financial markets; it involves intellectual engagement, not money. Finan- cial exchanges produce price discovery. Frictionless Research Exchanges produce community critical review.
>
> -- [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865)

However, there's a common missing link that requires an unnecessary amount of work to enable:

## Enabling Data Challenges is our goal

Donoho describes how the most common "missing piece" of FRX is to leave out the Data Challenge ([FR-3]) component.

> The most common leave-one-out setting is surely Reproducible Computational Science (RCS) where we combine [FR-1: Data Sharing] and [FR-2: Code Sharing], without [FR-3]. Here there is a scientific question but no underlying challenge problem being considered; we might simply be doing an exploratory data analysis and reporting what we saw, and giving others access to the data and the analysis scripts. RCS lacks the ability to focus attention of a broad audience on optimizing a performance measure.
>
> -- [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865)

We believe that this is in-part because there are no clear tools or standards for enabling this aspect of FRX without a lot of custom work and infrastructure orchestration.

This is the gap that this project aims to fill. The `frx-challenges` project allows a data challenge organizer to enable **[FR-3: Challenges]** by leveraging open datasets ([FR-1]) and computational infrastructure for reproducible execution ([FR-2]).

Enabling all three of these components is a key aspect of realizing Frictionless Data Exchanges:

> Without all three triad legs [FR-1]+[FR-2]+[FR-3], FR is simply blocked.
>
> Less clear is what we might be missing without [FR-3 – Challenges]. We would be missing the task definition which formalized a specific research problem and made it an object of study; the competitive element which attracted our attention in the first place; and the performance measure- ment which crystallized a specific project’s contribution, boiling down an entire research contribution essentially to a single number, which can be reproduced. The quantification of performance – part of practice [FR-3] – makes researchers everywhere interested in reproducing work by others and gives discussion about earlier work clear focus; it enables a community of researchers to care intensely about a single defined performance number, and in discussing how it can be improved.

> -- [Donoho, 2023](https://doi.org/10.48550/arXiv.2310.00865)
