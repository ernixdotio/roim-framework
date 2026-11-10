# Robotics Information Modelling (RoIM)

**A framework for robot-ready building information.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24099902.svg)](https://doi.org/10.5281/zenodo.24099902)
![Status](https://img.shields.io/badge/status-in%20development%20%E2%80%94%20not%20for%20implementation-red)
![Spec licence](https://img.shields.io/badge/spec-CC%20BY%204.0-blue)
![Code licence](https://img.shields.io/badge/code-MIT-green)

> [!WARNING]
> **Framework in development: not ready for implementation.** RoIM v0.1 is a draft proposal for discussion and research. It has not been validated on live projects or with robots, and must not be used to specify, check, accept or operate real work or to make safety decisions. Everything here will change. See [DISCLAIMER.md](DISCLAIMER.md).

Construction robots are arriving on site faster than the information they need. Building models are written for human readers, so they lack the survey-grade geometry, machine-readable semantics and live site state that layout robots, scanning quadrupeds, drones and finishing robots need to act safely.

**Robotics Information Modelling (RoIM)** is the structured creation, management and exchange of building information to the geometric accuracy, semantic depth and currency that an autonomous or semi-autonomous machine needs to localise, navigate, set out, build, inspect or verify work in the built environment.

📄 **White paper:** [RoIM v1.1 (PDF)](docs/white-paper/RoIM_White_Paper_v1.1.pdf) · [Zenodo record, DOI 10.5281/zenodo.24099902](https://doi.org/10.5281/zenodo.24099902)

---

## The framework at a glance

**Four pillars**

| Pillar | What it adds to BIM |
| --- | --- |
| Machine-readable geometry | Survey control, tolerance per element, design vs as-built kept apart |
| Robot semantics | Traversable / keep-out, surface and substrate, fixing method, approach side |
| Site state over time | What exists now, linked to the 4D programme |
| Feedback loop | Scans, deviations and task logs written back into the model |

**Five RoIM Levels of Information**, set per element and per robotic task:

| Level | Name | A robot can… | Example task |
| --- | --- | --- | --- |
| R0 | Visual | Nothing autonomous | Design review |
| R1 | Navigable | Localise and move through the space | Autonomous progress scan |
| R2 | Verifiable | Compare as-built with design | Weekly deviation analysis |
| R3 | Actionable | Set out or work on an element | Layout printing, drilling, drywall |
| R4 | Closed-loop | Write results back and keep the model current | Robot-maintained digital twin |

Full definitions: [docs/levels.md](docs/levels.md)

---

## What's in this repository

| Path | Contents |
| --- | --- |
| [`spec/pset/`](spec/pset) | `Pset_RobotReadiness` v0.1 property set (JSON + CSV) |
| [`spec/ids/`](spec/ids) | buildingSMART IDS 1.0 file that checks R1–R4 compliance |
| [`spec/revit/`](spec/revit) | Revit shared-parameter file + IFC export property-set mapping |
| [`spec/usd/`](spec/usd) | **OpenUSD** codeless schema `RoIMRobotReadinessAPI` + IFC↔USD mapping |
| [`tools/roim_check.py`](tools/roim_check.py) | Python checker: reports which elements meet their declared level |
| [`tools/ifc_to_usd_roim.py`](tools/ifc_to_usd_roim.py) | IFC → OpenUSD converter for NVIDIA Omniverse / Isaac Sim: geometry, RoIM data and semantic labels |
| [`examples/`](examples) | Sample IFC and USD models (R1–R3, one deliberately incomplete) |
| [`docs/`](docs) | White paper, level definitions, [OpenUSD + NVIDIA workflow](docs/openusd-nvidia-workflow.md) |

## IFC for delivery, OpenUSD for simulation

RoIM defines the same robot-readiness data in **IFC** (`Pset_RobotReadiness`) and **OpenUSD** (`RoIMRobotReadinessAPI`). A model checked in BIM therefore reaches **NVIDIA Isaac Sim / Omniverse** with its RoIM data, semantic labels and IFC GlobalIds intact, ready for navigation, synthetic data generation and task rehearsal. See the [OpenUSD + NVIDIA workflow](docs/openusd-nvidia-workflow.md).

## Quick start

**Check an IFC model**

```bash
pip install ifcopenshell
python tools/roim_check.py your_model.ifc --report roim_report.csv
```

Or load `spec/ids/RoIM_Levels_R1-R4_v0.1.ids` into any IDS-capable checker (e.g. ifctester, BIMcollab Zoom, Solibri, usBIM.IDS).

**Convert to OpenUSD for Isaac Sim**

```bash
pip install ifcopenshell usd-core
python tools/ifc_to_usd_roim.py your_model.ifc your_model.usda
```

**Use it in Revit**

1. Manage → Shared Parameters → browse to `spec/revit/RoIM_SharedParameters_v0.1.txt`.
2. Add the `RoIM_*` parameters you need as instance parameters to the relevant categories.
3. On IFC export, under *Property Sets*, tick *Export user defined property sets* and point it to `spec/revit/RoIM_IFC_Export_PropertySets_v0.1.txt`. The parameters export as `Pset_RobotReadiness`.

---

## 🤝 Help build RoIM

RoIM v0.1 is a proposal, not a usable standard. It needs testing on real projects with real robots. Contributions are welcome from:

- **BIM managers and coordinators**: test the levels on live models and refine the property set
- **Contractors and site teams**: pilot a robotic task on an R2 or R3 model and report back
- **Robotics companies and integrators**: tell us what information your platforms actually consume
- **Researchers**: validate tolerances, run studies and co-author future versions
- **Simulation and OpenUSD developers**: Isaac Sim pilots, USD tooling, alignment with AOUSD AECO work
- **Standards contributors**: help take RoIM to buildingSMART (bSDD and use cases)

👉 Start with [CONTRIBUTING.md](CONTRIBUTING.md), open a [proposal or pilot report](../../issues/new/choose) or join the [Discussions](../../discussions).

See the [ROADMAP](ROADMAP.md) for what's planned.

## Citing RoIM

> Mandisodza, E. (2026). *Robotics Information Modelling (RoIM): A Framework for Robot-Ready Building Information* (Version 1.1). Zenodo. https://doi.org/10.5281/zenodo.24099902

GitHub's **"Cite this repository"** button uses [`CITATION.cff`](CITATION.cff).

## Disclaimer

RoIM is a framework under development and **nothing in this repository is ready for implementation**. See [DISCLAIMER.md](DISCLAIMER.md).

## Licence

- Specification, documentation and white paper: [CC BY 4.0](LICENSE). You may share and adapt them, including commercially, with attribution.
- Code in `tools/` and `examples/`: [MIT](LICENSE-CODE).

Initiated by **Ernest Mandisodza**, BIM Coordinator, Dubai, UAE.
