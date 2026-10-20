# Interface examples / 接口示例

These are short interface demonstrations, not complete experiments. / 以下为接口示例。

| File | Prerequisites | Output |
| --- | --- | --- |
| `thinfilm.py` | `numpy`, `tmm`; illustrative constant refractive indices | `thinfilm.npz`, thickness and wavelength in nm |
| `layout.py` | Current `gdsfactory`; generic PDK for illustration only | `straight.gds`, geometry in micrometers |
| `lumerical.py` | Licensed Lumerical with `lumapi`; existing `device.fsp` containing `core` and `transmission` | `result.npz`, wavelength in meters |
| `symbolic_abcd.py` | `sympy`, `numpy` | Printed ABCD matrix, lengths in meters |

For real devices, supply measured material dispersion, a valid process PDK, appropriate boundaries and a calibrated observation model. Read the primary documentation linked by the catalogue for version-specific installation.
