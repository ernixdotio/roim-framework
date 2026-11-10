#!/usr/bin/env python3
"""Generate examples/roim_sample.ifc: a tiny IFC4 model with elements at R1-R3 (one deliberately incomplete)."""
import ifcopenshell, ifcopenshell.api as api, ifcopenshell.api.project
m = ifcopenshell.api.project.create_file(version="IFC4") if hasattr(ifcopenshell.api, "project") else ifcopenshell.file(schema="IFC4")
proj = api.run("root.create_entity", m, ifc_class="IfcProject", name="RoIM sample")
api.run("unit.assign_unit", m, length={"is_metric": True, "raw": "METERS"})
model = api.run("context.add_context", m, context_type="Model")
body = api.run("context.add_context", m, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=model)
site = api.run("root.create_entity", m, ifc_class="IfcSite", name="Site")
bldg = api.run("root.create_entity", m, ifc_class="IfcBuilding", name="Building")
storey = api.run("root.create_entity", m, ifc_class="IfcBuildingStorey", name="Level 01")
api.run("aggregate.assign_object", m, products=[site], relating_object=proj)
api.run("aggregate.assign_object", m, products=[bldg], relating_object=site)
api.run("aggregate.assign_object", m, products=[storey], relating_object=bldg)

import numpy as np
def place(e, x, y, rot=0):
    mat = np.eye(4); c, s_ = np.cos(np.radians(rot)), np.sin(np.radians(rot))
    mat[:2, :2] = [[c, -s_], [s_, c]]; mat[0, 3], mat[1, 3] = x, y
    api.run("geometry.edit_object_placement", m, product=e, matrix=mat)
def el(cls, name, props, geom):
    e = api.run("root.create_entity", m, ifc_class=cls, name=name)
    kind, args, pos = geom
    rep = api.run(f"geometry.add_{kind}_representation", m, context=body, **args)
    api.run("geometry.assign_representation", m, product=e, representation=rep)
    place(e, *pos)
    api.run("spatial.assign_container", m, products=[e], relating_structure=storey)
    ps = api.run("pset.add_pset", m, product=e, name="Pset_RobotReadiness")
    api.run("pset.edit_pset", m, pset=ps, properties=props)

el("IfcSlab", "Slab L01", {"RoIM_Level": "R1", "RoIM_TaskScope": "Navigate;Scan", "Traversable": True, "KeepOutZone": False, "ControlPointRef": "CP-01"},
   ("slab", {"depth": 0.25}, (0, 0)))
el("IfcWall", "Core wall W-12", {"RoIM_Level": "R2", "RoIM_TaskScope": "Scan", "Traversable": False, "KeepOutZone": False, "ControlPointRef": "CP-02",
   "PositionTolerance": m.create_entity("IfcLengthMeasure", 0.010), "AsDesignedState": "Approved for construction", "RegistrationTarget": True},
   ("wall", {"length": 6.0, "height": 3.0, "thickness": 0.3}, (0, 0)))
el("IfcWall", "Partition P-07", {"RoIM_Level": "R3", "RoIM_TaskScope": "SetOut;Drill", "Traversable": False, "KeepOutZone": False, "ControlPointRef": "CP-02",
   "PositionTolerance": m.create_entity("IfcLengthMeasure", 0.005), "AsDesignedState": "Approved for construction", "RegistrationTarget": False,
   "SettingOutPoints": "SOP_P-07.csv", "SurfaceType": "Gypsum board", "SubstrateMaterial": "Steel stud", "FixingMethod": "Screw",
   "ApproachSide": "Front", "ScheduleTaskRef": "T-3.4.2"},
   ("wall", {"length": 4.0, "height": 3.0, "thickness": 0.1}, (3.0, 0.3, 90)))
el("IfcWall", "Partition P-08 (incomplete)", {"RoIM_Level": "R3", "RoIM_TaskScope": "SetOut", "Traversable": False, "ControlPointRef": "CP-02",
   "PositionTolerance": m.create_entity("IfcLengthMeasure", 0.005), "AsDesignedState": "Design"},
   ("wall", {"length": 4.0, "height": 3.0, "thickness": 0.1}, (5.0, 0.3, 90)))
m.write("examples/roim_sample.ifc")
print("wrote examples/roim_sample.ifc")
