# RoIM with OpenUSD and NVIDIA Omniverse / Isaac Sim

> **Draft, not for implementation.** Part of the RoIM framework under development. See [DISCLAIMER.md](../DISCLAIMER.md).

IFC is how buildings are **delivered**; OpenUSD is how robots are **simulated**. RoIM defines the same robot-readiness data in both, so information checked in a BIM model arrives intact in a simulator, and results can travel back.

| | IFC side | OpenUSD side |
| --- | --- | --- |
| Container | `Pset_RobotReadiness` property set | `RoIMRobotReadinessAPI` applied API schema (codeless) |
| Names | `PositionTolerance` | `roim:positionTolerance` |
| Lengths | Project units (mm or m) | Metres |
| Identity | `GlobalId` | `ifc:globalId` attribute on every prim |
| Semantics | IFC class (`IfcWall`) | `semantics:labels:class = ["wall"]` (UsdSemantics LabelsAPI) |
| Checking | IDS file, `roim_check.py` | USD attributes (validator on the roadmap) |

Full mapping: [`spec/usd/IFC_to_USD_mapping_v0.1.csv`](../spec/usd/IFC_to_USD_mapping_v0.1.csv)

## Why OpenUSD matters for RoIM

- **NVIDIA Isaac Sim, Omniverse and Isaac Lab are built on OpenUSD.** A robot-ready model has to reach the simulator in USD.
- **IFC and USD are converging.** buildingSMART International and the Alliance for OpenUSD (AOUSD) signed a liaison agreement in October 2024, and AOUSD has an AECO Interest Group looking at USD's relationship with IFC. RoIM is designed to sit on both.
- **USD layers fit the RoIM feedback loop.** Design geometry, the RoIM data and each robot mission's results can be separate layers composed on one stage. R4 "closed-loop" maps naturally to a mission layer written by the robot.

## The workflow

```
 Revit / any BIM tool
        │  RoIM shared parameters (spec/revit)
        ▼
   IFC + Pset_RobotReadiness ──► IDS check (spec/ids) ──► fix and re-issue
        │
        │  tools/ifc_to_usd_roim.py
        ▼
   OpenUSD stage (.usd/.usda)
   ├─ geometry (metres, Z-up)
   ├─ RoIMRobotReadinessAPI  roim:* attributes
   ├─ semantics:labels:class  (wall, slab, door…)
   └─ ifc:globalId
        │
        ▼
   NVIDIA Isaac Sim
   ├─ navigation / occupancy from roim:traversable + roim:keepOutZone   (R1)
   ├─ Replicator synthetic data with IFC-derived labels                  (R1–R2)
   ├─ task rehearsal: set-out, drilling, finishing                        (R3)
   └─ ROS 2 bridge → real robot (e.g. FAST-LIO2 localisation)
        │
        ▼
   Mission results layer (deviation, as-built state)  ──► back to IFC by GlobalId  (R4)
```

### 1. Model and check (BIM side)
1. Load `spec/revit/RoIM_SharedParameters_v0.1.txt` in Revit and fill the parameters needed for the target level.
2. Export IFC with `spec/revit/RoIM_IFC_Export_PropertySets_v0.1.txt` as the user-defined property sets file.
3. Check it: `python tools/roim_check.py model.ifc --report report.csv`, or run the IDS file in any IDS checker.

### 2. Convert to OpenUSD
```bash
pip install ifcopenshell usd-core
python tools/ifc_to_usd_roim.py model.ifc model.usda
# only the elements that declare a RoIM level:
python tools/ifc_to_usd_roim.py model.ifc model_roim.usda --roim-only
```
Every element becomes `/World/<Storey>/<IfcClass>_<GlobalId>` with geometry, `roim:*` attributes, a class label and its IFC GlobalId.

**Using a different IFC→USD or Revit→USD exporter?** Keep its geometry and use the RoIM data model on top: apply `RoIMRobotReadinessAPI` and the `roim:*` attributes to matching prims. A RoIM-only overlay-layer tool is on the roadmap.

### 3. Register the RoIM schema (optional but recommended)
The schema is codeless, so nothing needs compiling. Point USD at the plugin folder before starting Isaac Sim or Python:

```bash
# Linux / macOS
export PXR_PLUGINPATH_NAME=/path/to/roim-framework/spec/usd/roimSchema
# Windows (PowerShell)
$env:PXR_PLUGINPATH_NAME="C:\path\to\roim-framework\spec\usd\roimSchema"
```
With it registered, `prim.HasAPI("RoIMRobotReadinessAPI")` works and the attributes show their docs and allowed values. Without it, the `roim:*` attributes still load and can be read normally.

### 4. Use it in Isaac Sim
- Open the `.usda` (File → Open). The model loads in metres, Z-up.
- **Semantics:** IFC classes are already applied as `class` labels through `UsdSemantics.LabelsAPI`, the labelling API Isaac Sim 5.0+ uses. Replicator annotators (segmentation, bounding boxes) pick them up directly. This is the "IFC labels for free" synthetic-data advantage described in the white paper.
- **Reading RoIM data in a script:**
  ```python
  from pxr import Usd
  stage = omni.usd.get_context().get_stage()
  keep_out = [p for p in stage.Traverse()
              if p.GetAttribute("roim:keepOutZone") and p.GetAttribute("roim:keepOutZone").Get()]
  r3_targets = [p for p in stage.Traverse()
                if p.GetAttribute("roim:level") and p.GetAttribute("roim:level").Get() in ("R3", "R4")]
  ```
- **Navigation (R1):** use `roim:traversable` and `roim:keepOutZone` to decide which prims count as obstacles when you generate occupancy maps, and to mark no-go zones.
- **Tasks (R3):** `roim:settingOutPoints`, `roim:approachSide`, `roim:surfaceType` and `roim:substrateMaterial` drive task scripts for layout, drilling and finishing robots.
- **ROS 2:** connect the sim robot to your real stack (e.g. ROS 2 + FAST-LIO2) through Isaac Sim's ROS 2 bridge, so you can test localisation against the model before going on site.

### 5. Close the loop (R4)
Write mission results (`roim:asBuiltState`, `roim:measuredDeviation`, `roim:lastVerifiedDate`, `roim:verificationSource`) into a **separate USD layer** per mission, then push them back to the IFC by `ifc:globalId`. A write-back tool is on the roadmap.

## Learning resources (NVIDIA and OpenUSD)
- NVIDIA *Learn OpenUSD* curriculum: schemas, layers, composition
- NVIDIA Isaac Sim docs: Replicator / synthetic data generation, ROS 2 bridge, occupancy map generation
- NVIDIA SimReady guides: semantic labelling of USD assets
- openusd.org: *Generating New Schema Classes* (codeless schemas)
- AOUSD AECO Interest Group, and the buildingSMART–AOUSD liaison

## Status
v0.1. Tested with OpenUSD (usd-core) 26.11 and IfcOpenShell 0.8 on the sample model in `examples/`. Not yet tested inside Isaac Sim. **Pilot reports are very welcome.**
