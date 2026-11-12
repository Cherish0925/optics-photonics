# Optics-Photonics-AI-Lab 0.7.0

Scientific arrays now travel with units, coordinates and physical conventions. `data.quantity`, `data.save` and `data.load` write and read NPZ arrays with JSON descriptions; `read_array` returns the coordinates belonging to the requested slice, including reversed and downsampled selections. Existing plain arrays remain supported.

Programs can explicitly convert units, spectral quantities, complex time dependence and wavefront sign while retaining their source description. A runnable HCIPy → POPPY example exchanges an aberrated pupil and reproduces image displacement and Strehl ratio after converting path-difference sign and units. See [the example](https://github.com/Cherish0925/Optics-Photonics-AI-Lab/tree/optics-v0.7.0/examples/exchange).

Scientific worker environments support Python 3.9+, including package-version collection after a calculation. The connector still uses Python 3.10+. Claude marketplace entries include description and author information. Contributor commits from `data-descriptions` and `host-launch` are retained.

Downloads: ResearchOS, Connect, Codex, Claude and Portable ZIP packages, a Python wheel/source archive and a TypeScript package. Universal bundles include native executors for Windows, macOS and Linux on x86_64 and ARM64. Managed Codex/Claude/Portable launchers use uv; Research OS uses its host Python. Existing solver bindings and runs remain under the same OPTICS_HOME.

Independent solver integration packages, remote-job attachment, additional cross-program research paths and licensed-workstation execution remain separate development work. This release does not claim new native-host runs for Research OS, Qiushi or DeepSeek.

## 中文

科学数组可以携带单位、坐标与物理约定跨程序传递。`data.quantity`、`data.save`、`data.load` 保存和读取 NPZ 数组及 JSON 说明；`read_array` 同时返回切片、倒序或降采样后的对应坐标，原有普通数组继续可用。

单位、光谱量、复振幅时间约定和波前符号均可显式转换并保留来源。HCIPy → POPPY 示例实际交换带像差的光瞳，转换光程差符号与单位后，得到一致的像点偏移和 Strehl 比。

求解器环境支持 Python 3.9 以上，修复计算完成后读取软件版本时报错的问题；连接器仍要求 Python 3.10 以上。补齐 Claude 市场描述和作者信息，保留两项贡献的提交历史。各宿主发行包随同一版本更新，已有环境配置和研究记录继续保留。
