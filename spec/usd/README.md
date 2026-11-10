# RoIM OpenUSD schema

> **Draft, not for implementation.** Part of the RoIM framework under development. See [DISCLAIMER.md](../../DISCLAIMER.md).

`roimSchema/` is a **codeless** OpenUSD plugin defining the single-apply API schema `RoIMRobotReadinessAPI`. It mirrors IFC `Pset_RobotReadiness` v0.1 as `roim:*` attributes.

- `schema.usda`: source definition
- `generatedSchema.usda` + `plugInfo.json`: what the USD runtime loads

Register it with `PXR_PLUGINPATH_NAME=<path>/spec/usd/roimSchema`. Verified with OpenUSD 26.11 (usd-core).

```python
from pxr import Usd
prim.ApplyAPI("RoIMRobotReadinessAPI")
prim.GetAttribute("roim:level").Set("R3")
```

Lengths are stored in **metres**. Enumerated values are `token` attributes with `allowedTokens`. Each attribute's `customData` records its IFC property name and the RoIM level it is required from.

Mapping table: [IFC_to_USD_mapping_v0.1.csv](IFC_to_USD_mapping_v0.1.csv) · Workflow: [docs/openusd-nvidia-workflow.md](../../docs/openusd-nvidia-workflow.md)
