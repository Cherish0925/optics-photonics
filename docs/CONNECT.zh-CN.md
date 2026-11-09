# 光学与光子学接入

这个软件包提供软件检索、原生程序执行、MCP 和研究 Skills。IOP 提供持续运行、进程管理、并行与串行调度、实验记录。光学软件保留自己的完整 API 和安装环境。

## 安装

连接器使用 Python 3.10 或更新版本，可运行于 Windows、macOS、Linux。具体求解器的系统、架构、Python 版本和许可要求，由对应软件决定。

```sh
python -m pip install "git+https://github.com/Cherish0925/optics-photonics.git@optics-v0.1.0"
optics-photonics search "thin film" --license-group open
optics-photonics info tmm
optics-photonics prepare tmm
```

将输入保存为 `inputs.json`：

```json
{"n":[1,1.45,1.52],"thickness_nm":[100],"wavelength_nm":[450,550,650]}
```

```sh
optics-photonics run tmm spectrum --inputs @inputs.json
```

Release 中的 wheel 可以直接安装，无需 Git。也可以用 `python -m optics_photonics` 调用全部命令。`prepare` 为已提供安装配方的软件建立独立环境；已有软件环境可直接连接：

```sh
optics-photonics bind tmm --python /path/to/scientific/python --threads 1 --concurrency 4
optics-photonics environments
```

不同软件可以使用不同的解释器和虚拟环境。配置默认保存在 `~/.optics-photonics`；`OPTICS_HOME` 可指定其他目录。

## 接入 Agent 系统

```sh
optics-photonics connect agentic-research-os --output optics-plugin
```

| 系统 | 生成内容 | 使用方式 |
| --- | --- | --- |
| Agentic Research OS | `plugin.json`、完整程序、Skills | 安装目录或 ZIP，激活已安装的修订；使用宿主的 `${RESEARCH_PYTHON}`。 |
| Codex | `.codex-plugin/plugin.json`、`.mcp.json`、Skills | 原生插件，或生成的 `INSTALL.md` 中的 MCP 注册命令。 |
| Claude Code | `.claude-plugin/plugin.json`、`.mcp.json`、Skills | `claude --plugin-dir PATH`，或 MCP 注册命令。 |
| DeepSeek Harness | `optics.cordis.yml` | `dsh web --patch PATH/optics.cordis.yml`，使用其原生 MCP 客户端。 |
| Qiushi | MCP 配置和命令入口 | 基于 Agentic Research OS 的版本使用原生包；其他版本通过 MCP 或 `tools` / `call`。 |
| 其他 MCP 宿主 | `mcp.json` | 按宿主自己的配置格式注册 stdio 命令。 |

命令中的系统名称可以替换为 `codex`、`claude`、`deepseek`、`qiushi`、`mcp`。本地配置记录选定的解释器和绝对路径，移动目录后重新生成。插件包含程序、资料和 Skills，不依赖源码目录；已有宿主设置不会被覆盖。

更新时安装新 wheel 或 Git 标签，生成新的插件目录，再由宿主更新并激活。`OPTICS_HOME` 和科学计算环境保留。云端产品如果不能启动本地进程，需要自己的执行环境或转接服务；本地 stdio 配置不能直接变成云端连接器。

## 完整研究程序与持续计算

原生 Python 程序获得 `INPUTS`、`OUTPUT_DIR`，并将简洁的 JSON 结果赋给 `RESULT`。程序可以使用软件的完整 API、优化算法和持续会话；数组、网格、模型和图像写入输出目录。示例位于 [`examples/programs`](../examples/programs)。

```sh
optics-photonics run tmm --program research.py --inputs @inputs.json
```

长期计算在计算机上安装 [IOP Runtime](https://github.com/Cherish0925/AI4Instruments/releases)，然后在同一台计算机上连接软件：

```sh
optics-photonics attach tmm
optics-photonics submit tmm --program research.py --inputs @inputs.json --request-id study-001
optics-photonics status RUN_ID
optics-photonics files RUN_ID
optics-photonics download ARTIFACT_ID spectrum.csv
```

Agent 断开后任务仍由 IOP 执行。重试同一次提交时沿用 `request-id`。本地使用 IOP 已保存的地址和凭据；远程连接使用 `IOP_ENDPOINT`、`IOP_TOKEN`。环境注册必须在计算机一侧完成，因为解释器和程序路径属于该机器。

工作流的每一步包含 `id`、`device`、`operation`、`arguments`、`after`，需要传递结果时增加 `bindings`。明确写 `after: []` 可并行；依赖关系决定先后，`bindings` 决定数据传递。`submit-workflow --run-id RUN_ID` 可向已有的持续实验追加一批操作。同一次实验可以同时包含真实仪器和数字计算。必须维持同一软件会话的迭代放在一个原生程序中执行。

首次本地连接会按可用 CPU 数量建立缺失的 CPU 额度，保留已有设置。`threads` 控制常见数值库线程，`concurrency` 控制某软件同时执行的进程数。MPI、GPU、商业许可证和集群队列由实际求解器及其启动程序配置。

IOP 0.8.5 在工作流结束后登记命令生成的文件；持续实验需要提前读取时，可通过 IOP 的文件上传接口保存。第三方云计算的任务编号应及时保存，并用其原生恢复接口接续；当前不会自动重建任意远程软件会话。

## 已提供的内容

| 范围 | 内容 |
| --- | --- |
| 96 项软件与产品族 | 连接说明、原始文档、已有官方或社区 MCP / Skill 入口。 |
| 13 个已执行计算的软件 | tmm、miepython、raytracing、LightPipes、POPPY、HCIPy、QuTiP、SymPy、SciPy、scikit-image、KLayout、grcwa、legume；带安装配方和可运行计算。 |
| 58 项 Python API，包括上述 13 项 | 模块发现、独立解释器配置、完整原生程序执行；其余软件尚未全部实跑。 |
| 33 项原生命令或厂商接口 | 统一进程接入方式；仍需对应软件的启动程序、运行环境与许可。 |
| 4 项自动化接口未明确的软件 | 保留资料，不标记为自动执行。 |
| 1 个材料数据库 | 数据与来源，不作为求解器。 |
| 14 个研究领域 | 模型选择、物理量、单位、软件间数据传递，按任务读取。 |

原生命令程序从 `IOP_REQUEST_FILE` 或标准输入读取 JSON，将文件写入 `IOP_OUTPUT_DIR`，将 JSON 结果写入 `IOP_RESULT_FILE`。通过 `--command-json` 指定可执行文件和参数。C、C++、C#、Java、Julia、商业软件批处理均可采用这一方式，不需要重写其计算核心。

MCP 共 11 个工具，覆盖软件选择、环境配置、登记、提交、状态、取消与文件。大数组保存在文件中。原始 MCP 和 Skill 保留其作者及用途说明；本项目的插件由本仓库维护。

开发、三系统运行检查和宿主格式原始资料见 [English guide](CONNECT.md)。
