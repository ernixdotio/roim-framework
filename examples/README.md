# Examples

`roim_sample.ifc` is a tiny IFC4 model with four elements:

| Element | Declared level | Result |
| --- | --- | --- |
| Slab L01 | R1 | PASS |
| Core wall W-12 | R2 | PASS |
| Partition P-07 | R3 | PASS |
| Partition P-08 (incomplete) | R3 | FAIL: 8 properties missing |

Regenerate it with `python examples/make_sample.py`. Check it with:

```bash
python tools/roim_check.py examples/roim_sample.ifc
```

**Wanted:** anonymised real-world examples at R1–R4. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## OpenUSD version

`roim_sample.usda` is the same model converted for NVIDIA Omniverse / Isaac Sim:

```bash
python tools/ifc_to_usd_roim.py examples/roim_sample.ifc examples/roim_sample.usda
```

It has geometry, `RoIMRobotReadinessAPI` with `roim:*` attributes, `semantics:labels:class` labels and `ifc:globalId` on every prim. See [docs/openusd-nvidia-workflow.md](../docs/openusd-nvidia-workflow.md).
