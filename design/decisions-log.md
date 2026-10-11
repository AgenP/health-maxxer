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
| 7 | Device | Responsive web, desktop-first demo; at phone width the sidebar collapses to a bottom tab bar and "Check a food" opens the camera | |
| 8 | Agent stub | Scripted Q&A modal: 2 to 3 suggested prompts with pre-written answers from the sample data; anything else gets "coming soon" | |
| 9 | Demo tree | Primary: seeded dashboard, photo of a warmed wrap (T1 High), edit the Heated chip so the estimate re-runs, dashboard updates, Ask Health OS, end slide (roadmap + validation). Side path: unknown product catch-all (T3, wide band) | B4: one story, one side path |
| 10 | System states wireframed | Empty dashboard, unknown food (T5), photo unreadable or not food, offline/API down (cached data + banner) | D#40 |
| 11 | Hallway test | **No.** Self only; all needs labelled as assumptions in the deck | Accepted conflict with D#10 and D#55 |
| 12 | Check a food entry | **A. Modal over the dashboard**; the result renders in the modal and "Done" returns to the updated dashboard | Options: `wireframes/q-check-a-food.html` |

## Jacquie conflicts acknowledged

- Self-only research (D#55, B A28): mitigated by labelling the needs as assumptions.
- Greyed modules vs focus (D#29, B4): resolved by the sidebar nav choice.
- Hallway usability test (D#10): declined; self-only constraint kept.
- Flows before screens (C#31): flows are mapped before the wireframes.
