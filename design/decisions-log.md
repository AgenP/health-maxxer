# Design decisions log

Grilling session, 2026-10-11. Research basis: self-interview (Philip) only, a hackathon constraint. Treat every user need here as an **assumption** (Jacquie D#59), not a finding.

| # | Decision | Choice | Notes |
|---|---|---|---|
| 1 | Core moment of use | Both: the dashboard is home, with "Check a food" on it | Every Food Check feeds the weekly view |
| 2 | Exposure headline | Top Contributors with Swaps; no aggregate number | Unrated checks are counted and shown |
| 3 | Health OS Agent | Invokable from any screen (button/modal, later a wake word); **stubbed** this round | |
| 4 | Coming-soon Modules layout | **C. Sidebar nav**: modules listed in a left nav, the others greyed out | Options: `wireframes/q-coming-soon-layout.html`. Trade-off accepted: the vision is less visible in screenshots |
| 5 | Food Check confirmation | Result first; Food Attributes shown as editable chips on the result, and editing one re-runs the estimate | Chips double as the trust signal (A#41) |
| 6 | Result card | **A. Tier word + range bar**, plus an Evidence Tier badge; no point dot below T2 | Options: `wireframes/q-result-card.html` |

## Jacquie conflicts acknowledged

- Self-only research (D#55, B A28): mitigated by labelling the needs as assumptions.
- Greyed modules vs focus (D#29, B4): resolved by the sidebar nav choice.
- Flows before screens (C#31): flows are mapped before the wireframes.
