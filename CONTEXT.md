# Health-maxxer

A health OS whose first working module estimates a person's exposure to microplastics and plastic-associated chemicals from the food they eat. The other modules are shown but not yet built.

## Language

### Health OS

**Health OS**:
The overall product: one home dashboard that hosts several health modules for one person.
_Avoid_: platform, suite, app

**Module**:
One self-contained health area inside the Health OS (Exposure, Bloodwork, Sleep, Gym & Nutrition, Overview).
_Avoid_: feature, section, tab

**Health OS Agent**:
An assistant the person can invoke from any screen (button/modal or wake word) that answers across Modules. Stubbed in the hackathon build.
_Avoid_: chatbot, assistant, copilot

**Coming-soon Module**:
A Module shown on the dashboard in a greyed-out state, not yet functional.
_Avoid_: placeholder, disabled section

### Exposure

**Food Check**:
One act of submitting a food (photo, free text, or both, plus Location) and receiving an Exposure Estimate. Every Food Check is also logged to the person's history.
_Avoid_: scan, lookup, query

**Exposure Estimate**:
The result of a Food Check: a relative risk tier with an uncertainty band, an Evidence Tier, and a Swap where one exists. Never a safety or toxicity verdict.
_Avoid_: score, rating, toxicity score

**Food Attributes**:
The properties inferred about a food in a Food Check (packaging, heated, brand, category, fattiness, Origin), shown as editable chips on the Exposure Estimate. Correcting one re-runs the estimate.
_Avoid_: features, tags, metadata

**Evidence Tier**:
How directly an Exposure Estimate is grounded: T1 lab-measured, T2 similar products, T3 category, T4 origin adjustment, T5 global prior.
_Avoid_: confidence level, data quality

**Swap**:
A lower-exposure alternative suggested alongside an Exposure Estimate.
_Avoid_: recommendation, alternative

**Top Contributors**:
The foods that drove most of the person's exposure over a period, ranked by Exposure Estimate tier times frequency, each paired with a Swap. The headline of the Exposure Module; there is no aggregate exposure number.
_Avoid_: weekly score, exposure index

**Swap Impact**:
How much a Swap is expected to reduce exposure, with its own evidence: lab-backed (both sides measured), inferred (direction from method, size uncertain), or unbacked (stated as a limitation, closable by running our own studies).
_Avoid_: savings, reduction score, benefit

**Reference Level**:
An external benchmark an Exposure Estimate is compared against, always named with its source and type (e.g. EFSA tolerable daily intake, EPA legal limit, NYC action level). Where none exists, the card says so. Never called a "safe level".
_Avoid_: safe level, safe limit, threshold

**Location**:
Where the person is buying or eating the food; used only as a fallback prior for origin. Distinct from Origin.
_Avoid_: region, market

**Origin**:
Where the food or its ingredients were produced.
_Avoid_: location, source country
