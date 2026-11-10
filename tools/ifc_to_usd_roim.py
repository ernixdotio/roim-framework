#!/usr/bin/env python3
"""
ifc_to_usd_roim.py - convert an IFC model to OpenUSD with RoIM data (v0.1)

Produces a USD stage ready for NVIDIA Omniverse / Isaac Sim:
  * triangulated geometry for every IfcElement (metres, Z-up)
  * prims grouped by storey: /World/<Storey>/<IfcClass>_<GlobalId>
  * RoIMRobotReadinessAPI applied, carrying Pset_RobotReadiness as roim:* attributes
  * semantic class labels (UsdSemantics LabelsAPI, instance "class") from the IFC class,
    e.g. IfcWall -> "wall", for Isaac Sim Replicator synthetic data
  * ifc:globalId / ifc:class attributes so results can be written back to the IFC

Usage:
    python tools/ifc_to_usd_roim.py model.ifc model.usda [--roim-only]

  --roim-only   only export elements that declare a RoIM level

Requires: pip install ifcopenshell usd-core
Optional: set PXR_PLUGINPATH_NAME to spec/usd/roimSchema to register the RoIM schema.
Licence: MIT (see LICENSE-CODE)
"""
import argparse
import json
import re
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element as eu
import ifcopenshell.util.unit as uu
from pxr import Gf, Sdf, Usd, UsdGeom, Vt

try:
    from pxr import UsdSemantics  # OpenUSD 24.11+
except ImportError:  # older USD builds
    UsdSemantics = None

ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "spec/pset/Pset_RobotReadiness_v0.1.json").read_text(encoding="utf-8"))
API = "RoIMRobotReadinessAPI"


def usd_name(prop):
    if prop == "RoIM_Level":
        return "roim:level"
    if prop == "RoIM_TaskScope":
        return "roim:taskScope"
    return "roim:" + prop[0].lower() + prop[1:]


def valid(name):
    name = re.sub(r"[^A-Za-z0-9_]", "_", name or "Unnamed")
    return name if not name[0].isdigit() else "_" + name


def semantic_label(ifc_class):
    # IfcWallStandardCase -> wall_standard_case ; IfcSlab -> slab
    n = ifc_class[3:] if ifc_class.startswith("Ifc") else ifc_class
    return re.sub(r"(?<!^)(?=[A-Z])", "_", n).lower()


def write_roim(prim, pset, length_scale):
    prim.AddAppliedSchema(API)
    for p in SPEC["properties"]:
        if p["name"] not in pset or pset[p["name"]] is None:
            continue
        v = pset[p["name"]]
        a, t = usd_name(p["name"]), p["ifcDataType"]
        if p["name"] == "RoIM_TaskScope":
            vals = [s.strip() for s in str(v).replace(",", ";").split(";") if s.strip()]
            prim.CreateAttribute(a, Sdf.ValueTypeNames.TokenArray, custom=False, variability=Sdf.VariabilityUniform).Set(Vt.TokenArray(vals))
        elif t == "IFCBOOLEAN":
            prim.CreateAttribute(a, Sdf.ValueTypeNames.Bool, custom=False, variability=Sdf.VariabilityUniform).Set(bool(v))
        elif t == "IFCLENGTHMEASURE":
            prim.CreateAttribute(a, Sdf.ValueTypeNames.Double, custom=False, variability=Sdf.VariabilityUniform).Set(float(v) * length_scale)
        elif "allowedValues" in p:
            prim.CreateAttribute(a, Sdf.ValueTypeNames.Token, custom=False, variability=Sdf.VariabilityUniform).Set(str(v))
        else:
            prim.CreateAttribute(a, Sdf.ValueTypeNames.String, custom=False, variability=Sdf.VariabilityUniform).Set(str(v))


def convert(ifc_path, usd_path, roim_only=False):
    model = ifcopenshell.open(ifc_path)
    length_scale = uu.calculate_unit_scale(model)  # project length unit -> metres

    stage = Usd.Stage.CreateNew(str(usd_path))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    world = UsdGeom.Xform.Define(stage, "/World")
    stage.SetDefaultPrim(world.GetPrim())
    stage.GetRootLayer().customLayerData = {
        "roim:schemaVersion": SPEC["version"],
        "roim:source": Path(ifc_path).name,
        "roim:doi": SPEC["doi"],
    }

    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    shapes = {}
    it = ifcopenshell.geom.iterator(settings, model)
    if it.initialize():
        while True:
            s = it.get()
            shapes[s.guid] = s
            if not it.next():
                break

    n_total = n_roim = 0
    for el in model.by_type("IfcElement"):
        pset = eu.get_pset(el, SPEC["name"]) or {}
        if roim_only and "RoIM_Level" not in pset:
            continue
        storey = eu.get_container(el)
        parent = f"/World/{valid(storey.Name if storey else 'Unassigned')}"
        UsdGeom.Xform.Define(stage, parent)
        path = f"{parent}/{valid(el.is_a())}_{valid(el.GlobalId)}"

        shp = shapes.get(el.GlobalId)
        if shp is not None:
            mesh = UsdGeom.Mesh.Define(stage, path)
            v = shp.geometry.verts
            f = shp.geometry.faces
            pts = [Gf.Vec3f(v[i], v[i + 1], v[i + 2]) for i in range(0, len(v), 3)]
            mesh.CreatePointsAttr(pts)
            mesh.CreateFaceVertexCountsAttr([3] * (len(f) // 3))
            mesh.CreateFaceVertexIndicesAttr(list(f))
            mesh.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none)
            prim = mesh.GetPrim()
        else:
            prim = UsdGeom.Xform.Define(stage, path).GetPrim()

        prim.CreateAttribute("ifc:globalId", Sdf.ValueTypeNames.String).Set(el.GlobalId)
        prim.CreateAttribute("ifc:class", Sdf.ValueTypeNames.Token).Set(el.is_a())
        if el.Name:
            prim.SetDisplayName(el.Name)

        label = semantic_label(el.is_a())
        if UsdSemantics is not None:
            UsdSemantics.LabelsAPI.Apply(prim, "class").CreateLabelsAttr([label])
        else:
            prim.CreateAttribute("semantics:labels:class", Sdf.ValueTypeNames.TokenArray).Set([label])

        if "RoIM_Level" in pset:
            write_roim(prim, pset, length_scale)
            n_roim += 1
        n_total += 1

    stage.GetRootLayer().Save()
    print(f"Wrote {usd_path}: {n_total} elements, {n_roim} with RoIM data")


def main():
    ap = argparse.ArgumentParser(description="Convert IFC to OpenUSD with RoIM robot-readiness data.")
    ap.add_argument("ifc")
    ap.add_argument("usd", help="Output .usd/.usda/.usdc")
    ap.add_argument("--roim-only", action="store_true", help="Only export elements declaring a RoIM level")
    a = ap.parse_args()
    convert(a.ifc, a.usd, a.roim_only)


if __name__ == "__main__":
    main()
