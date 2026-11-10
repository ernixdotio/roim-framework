# Contributing to RoIM

> **Draft, not for implementation.** Part of the RoIM framework under development. See [DISCLAIMER.md](DISCLAIMER.md).

Thanks for helping build Robotics Information Modelling. RoIM is at **v0.1, draft for public comment**, so the most valuable contributions right now are evidence and critique.

## Ways to contribute

| You are… | Best contribution | How |
| --- | --- | --- |
| BIM manager / coordinator | Try the property set on a real model; tell us what's missing, redundant or unclear | Issue → **Spec proposal** |
| Contractor / site team | Run a robotic task on an R1–R3 model and report results | Issue → **Pilot report** |
| Robotics company / integrator | Tell us what your robot actually reads from a model | Issue → **Robot data requirements** |
| Researcher | Validate tolerances and levels, publish studies | Discussions → *Research* |
| Developer | Improve `roim_check.py`, add Dynamo/pyRevit/Grasshopper tools | Pull request |
| Simulation / OpenUSD developer | Isaac Sim pilots, USD schema and converter improvements | Pull request or **Pilot report** |

Questions and ideas that aren't ready for an issue go in **Discussions**.

## How changes are made

1. **Discuss first.** Open an issue using a template before changing the spec.
2. **Propose.** Open a pull request that changes the JSON/CSV in `spec/pset/`, and update the IDS, Revit, OpenUSD schema (`spec/usd/`) and docs to match.
3. **Review.** Spec changes stay open for comment for at least 7 days.
4. **Release.** Accepted changes are grouped into versions (v0.2, v0.3…). Each spec version gets a Zenodo DOI and lists its contributors.

### Versioning
- **Patch** (0.1.x): wording, typos, tooling fixes.
- **Minor** (0.x): properties added or changed, level criteria refined.
- **1.0** of the spec: after at least one validated field pilot per level R1–R3.

### Spec conventions
- Property names: PascalCase, no spaces (`PositionTolerance`).
- Every property has: type, IFC data type, `fromLevel`, description, allowed values where they're enumerated.
- Lengths in project units; mm recommended.
- Keep `spec/pset/*.json` as the single source of truth. Other files are generated from it or kept in sync with it.

## Credit

Every accepted contribution is credited in [CONTRIBUTORS.md](CONTRIBUTORS.md) and in the release notes of the next spec version.

## Licensing of contributions

By contributing you agree that:
- contributions to the spec and docs are licensed under **CC BY 4.0**
- contributions to code are licensed under **MIT**

## Conduct

Be constructive and specific, and respect other people's time and expertise. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
