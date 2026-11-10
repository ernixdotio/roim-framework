# RoIM Levels of Information (R0–R4)

A RoIM level states what a machine can safely do with a model. Levels are set **per element and per task**, as Level of Information Need is, not for the whole model. One project can need R3 for slab set-out and R1 for façade inspection.

Levels are cumulative: R3 includes everything from R1 and R2.

| Level | Name | A robot can… | Minimum information | Example task |
| --- | --- | --- | --- | --- |
| R0 | Visual | Nothing autonomous; humans interpret the model | Standard design BIM, any LOD | Design review |
| R1 | Navigable | Localise and move through the space | Georeferenced model, survey control points, floors, walls, openings and stairs with traversable or blocked status, keep-out zones | Autonomous progress scan |
| R2 | Verifiable | Compare as-built with design and report deviation | R1 + tolerance per element, IFC class and GUID kept stable, as-designed state flagged, scan-to-model registration targets | Weekly deviation analysis |
| R3 | Actionable | Set out or work on an element | R2 + survey-grade setting-out points, fixing method, surface and substrate data, approach side and reach envelope, task sequence linked to 4D | Layout printing, drilling, drywall |
| R4 | Closed-loop | Write results back and keep the model current | R3 + as-built state per element, robot task log, deviation records and evidence links written to the model, version control on state | Robot-maintained digital twin |

## Properties required per level

| Property | R1 | R2 | R3 | R4 |
| --- | :-: | :-: | :-: | :-: |
| RoIM_Level | ● | ● | ● | ● |
| RoIM_TaskScope, Traversable, KeepOutZone, ControlPointRef | ● | ● | ● | ● |
| PositionTolerance, AsDesignedState, RegistrationTarget | | ● | ● | ● |
| SettingOutPoints, SurfaceType, SubstrateMaterial, FixingMethod, ApproachSide, ScheduleTaskRef | | | ● | ● |
| AsBuiltState, MeasuredDeviation, LastVerifiedDate, VerificationSource | | | | ● |

The machine-readable version is [`spec/pset/Pset_RobotReadiness_v0.1.json`](../spec/pset/Pset_RobotReadiness_v0.1.json).
