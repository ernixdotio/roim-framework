# RoIM Roadmap

> **Draft, not for implementation.** Part of the RoIM framework under development. See [DISCLAIMER.md](DISCLAIMER.md).

## v0.1 (Nov 2026): published ✅
- White paper v1.0 with DOI
- `Pset_RobotReadiness` v0.1 (JSON, CSV)
- IDS checks for R1–R4
- Revit shared parameters + IFC export mapping
- `roim_check.py` checker + sample IFC
- OpenUSD codeless schema `RoIMRobotReadinessAPI` + IFC→USD converter for NVIDIA Isaac Sim

## v0.2: community review
- [ ] Public comment on every property (open issues per pillar)
- [ ] Decide on the property-set name: keep `Pset_RobotReadiness`, or use a non-reserved prefix (e.g. `RoIM_RobotReadiness`), since buildingSMART reserves `Pset_` for standard sets
- [ ] Default tolerance tables per element type and task
- [ ] Mapping to existing bSDD / HumanTech robotics terms
- [ ] Setting-out point file format (CSV schema)
- [ ] OpenUSD: RoIM overlay-layer tool (adds roim:* to USD from any Revit/IFC→USD exporter)
- [ ] OpenUSD: `roim_check` for USD stages

## v0.3: first pilots
- [ ] Pilot 1: R2 deviation analysis (scan vs model) on a live project
- [ ] Pilot 2: R3 robotic layout / set-out
- [ ] Publish pilot reports in `pilots/`
- [ ] pyRevit / Dynamo tool to fill and audit RoIM parameters
- [ ] Isaac Sim pilot: occupancy map from roim:traversable / roim:keepOutZone; Replicator dataset from IFC labels
- [ ] R4 write-back: USD mission layer → IFC by GlobalId

## v1.0 (spec)
- [ ] At least one validated pilot each at R1, R2 and R3
- [ ] R4 live-state approach (IFC + digital-twin sync)
- [ ] Submit RoIM use cases to buildingSMART Use Case Management
- [ ] Propose the property set to the buildingSMART Data Dictionary (bSDD)
- [ ] Share the RoIM USD schema with the AOUSD AECO Interest Group

Have a priority you'd add? Open an issue or start a Discussion.
