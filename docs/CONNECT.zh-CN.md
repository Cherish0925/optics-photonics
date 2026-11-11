# 光学与光子学研究工具

Optics & Photonics 独立提供光学软件连接、原生研究程序、后台计算、MCP、Skills 和插件。选择软件、建立模型、求解、优化、保存与读取结果，都通过这个软件包完成。

## 安装与第一次计算

连接程序使用 Python 3.10+，支持 Windows、macOS、Linux。科学软件使用各自支持的 Python、系统与许可；可以为每个软件连接不同的环境。

```sh
python -m pip install "https://github.com/Cherish0925/Optics-Photonics-AI-Lab/releases/download/optics-v0.5.1/optics_photonics-0.5.1-py3-none-any.whl"
optics-photonics search "thin film" --license-group open
optics-photonics info tmm
optics-photonics prepare tmm
```

将输入保存为 `inputs.json`：

```json
{"n":[1,1.45,1.52],"thickness_nm":[100],"wavelength_nm":[450,550,650]}
```

```sh
optics-photonics run tmm spectrum --inputs "@inputs.json"
```

命令返回输出目录、结果和软件版本。光谱保存在 CSV 文件中。也可先下载 Release 中的 wheel，再用 `python -m pip install 文件.whl` 安装；也可用 `python -m optics_photonics` 调用全部命令。

## 科学环境与完整程序

`prepare` 按已有配方建立独立环境；已有环境直接连接：

```sh
optics-photonics bind tmm --python "/path/to/scientific/python" --threads 1 --concurrency 4
optics-photonics environments
optics-photonics resources --cpu 8
```

`threads` 设置常见数值库的线程数；`concurrency` 设置同一软件的并行进程数；`resources` 设置这台计算机上所有后台研究任务共享的 CPU 额度。MPI、GPU、商业许可证和集群队列使用求解器自己的启动配置。

原生 Python 程序接收 `INPUTS`、`OUTPUT_DIR`，并将简洁结果赋给 `RESULT`。程序可以使用完整 API，保留同一软件会话，运行优化、迭代和参数扫描。数组、场、网格和模型写入 `OUTPUT_DIR`。

```sh
optics-photonics run tmm --program research.py --inputs "@inputs.json"
```

原生命令也可以连接。程序从 `OPTICS_REQUEST_FILE` 或标准输入读取 JSON，将文件写入 `OPTICS_OUTPUT_DIR`，把 JSON 结果写入 `OPTICS_RESULT_FILE`。`bind --command-json` 接收可执行文件和参数数组，支持 `{request}`、`{output}`、`{result}` 参数。C、C++、C#、Java、Julia 和商业软件批处理均可沿用其原生实现。

## 持续计算与研究工作流

```sh
optics-photonics submit tmm --program research.py --inputs "@inputs.json" --request-id study-001
optics-photonics runs
optics-photonics status RUN_ID
optics-photonics files RUN_ID
optics-photonics read RUN_ID calculate/attempt-1/result.json
optics-photonics download RUN_ID calculate/attempt-1/spectrum.csv spectrum.csv
```

提交后立即返回任务编号。后台进程继续执行，CLI 或 MCP 关闭不会结束计算。再次提交同一请求时沿用 `request-id`，会返回原任务。运行期间已经写出的文件可以直接读取。

工作流是 JSON 数组。每一步包含 `id`、`tool`、`inputs`，以及 `action` 或 `source`。`after` 指定前置步骤；`bindings` 把前一步结果写入下一步输入，并自动建立依赖。例如：

```json
[
  {"id":"a","tool":"tmm","action":"spectrum","inputs":{"n":[1,1.45,1.52],"thickness_nm":[100],"wavelength_nm":[550]}},
  {"id":"b","tool":"tmm","action":"spectrum","inputs":{"n":[1,1.45,1.52],"thickness_nm":[120],"wavelength_nm":[550]}},
  {"id":"compare","tool":"tmm","source":"RESULT={'delta_R':INPUTS['b']-INPUTS['a']}","bindings":{"a":{"step":"a","path":["result","first",1]},"b":{"step":"b","path":["result","first",1]}}}
]
```

```sh
optics-photonics submit-workflow workflow.json --request-id comparison-001
optics-photonics submit-workflow next-steps.json --run-id RUN_ID
optics-photonics cancel RUN_ID
optics-photonics resume RUN_ID
```

没有依赖的步骤按资源设置并行；后续步骤等待依赖完成。追加步骤保留同一个研究任务。`resume` 保留已完成步骤，重新运行未完成步骤，每次尝试的文件独立保存。云端求解器的任务编号和接续方式由原生程序保存与处理。

## 从插件市场安装

| 宿主 | 添加来源与安装 |
| --- | --- |
| Agentic Research OS | **Extensions → Plugins → Add from link**，填写 `https://github.com/Cherish0925/Optics-Photonics-AI-Lab/tree/main/connect/agentic-research-os`，安装 `optics-photonics`，激活返回的修订。 |
| Codex | `codex plugin marketplace add Cherish0925/Optics-Photonics-AI-Lab`，再执行 `codex plugin add optics-photonics@optics-photonics`。 |
| Claude Code | `claude plugin marketplace add Cherish0925/Optics-Photonics-AI-Lab`，再执行 `claude plugin install optics-photonics@optics-photonics`。 |

Research OS 包携带连接器、目录与 Skills，使用宿主自带的 Python。
Codex/Claude 的 GitHub 插件通过工具执行端 PATH 中的 `python`（3.10+）运行包内代码。
解释器名称或路径不同时，使用该解释器安装连接器，再生成下面的宿主包。
科学软件通过 `prepare_environment` 准备，或通过 `bind_environment` / `bind_native_software` 接入。

更新时在 Research OS 刷新来源，安装其新修订。Codex 使用
`codex plugin marketplace upgrade optics-photonics` 刷新来源并安装更新；Claude 使用
`claude plugin marketplace update optics-photonics`，再执行
`claude plugin update optics-photonics@optics-photonics`。
新连接加载新版插件；科学环境与研究记录保留在 `OPTICS_HOME`，已提交的计算继续使用启动时的程序。

这些入口是项目维护的 GitHub 插件市场；OpenAI、Anthropic 审核后的公共目录另有提交与收录流程。

## Agent、MCP 与插件

```sh
optics-photonics connect agentic-research-os --output optics-plugin
```

| 系统 | 接入形式 |
| --- | --- |
| Agentic Research OS | 安装含 `plugin.json` 的目录，激活对应修订；Release ZIP 解压后直接得到这个目录。 |
| Codex | `connect codex` 生成原生插件和 MCP 注册命令。 |
| Claude Code | `connect claude`；使用 `claude --plugin-dir PATH` 或生成的 MCP 命令。 |
| DeepSeek Harness | `connect deepseek`；使用 `dsh web --patch PATH/optics.cordis.yml`。 |
| Qiushi | 研究系统版本使用其原生插件包；其他版本使用 `connect qiushi` 生成的 MCP 或命令入口。 |
| 其他 MCP 宿主 | `connect mcp`，按宿主格式注册 stdio 命令。 |

MCP 包含软件检索、环境准备、连接、资源设置、提交、任务查询、取消、继续、文件读取与下载。`prepare_environment` 在后台安装已有配方，返回任务编号；安装完成后软件环境自动登记。完整研究方法由两个 Skills 和 14 个领域参考文件按需提供。

计算发生在 MCP 服务所在的计算机。远程机器可通过 SSH 启动 stdio 服务，保持连接程序与科学环境在同一台机器：`ssh -T USER@HOST /path/to/python -m optics_photonics mcp`。`read_result` 把内容传回 Agent；`download_result` 写入服务所在机器的目标路径，大文件可通过 SSH/SFTP 取回。

更新时安装新版本并生成新的插件目录，由宿主更新和激活。科学环境、研究记录和结果保留在 `OPTICS_HOME` 或 `~/.optics-photonics`。

## 软件覆盖与扩展

软件目录包含商业、开源和受限许可三组，每项保留原始接口文档及已有 MCP、Skill 的来源。可执行计算在交互指南中单独筛选。`software_details` 返回原生 API、安装配方、示例输入和物理约定。

新增软件时补充连接记录、环境说明和原生程序，沿用共同的任务与文件接口。涉及商业 SDK、GUI、远程计算或 MPI 时，把对应启动与会话管理放在软件适配程序中。跨软件传递场、光谱、S 参数和模型时，同时保存单位、坐标、采样、归一化与材料来源。

[本机商业软件：发现、会话、项目与结果](NATIVE.zh-CN.md)。

长时间研究任务应运行在持续存在的计算主机上。独立工作进程可以在提交程序退出后继续计算；如果宿主回收整个容器或进程组，工作进程也会结束。此类 Agent 环境应通过 SSH 连接科学工作站上的 MCP，将计算留在工作站。

## 接入目录之外的研究工具

通过 `register_software` 登记本地软件的名称、用途、Python 模块与资料来源，再用 `bind_environment` 连接已经安装的解释器或可执行程序。`registered_software` 列出本地工具，`software_details` 读取其说明。目录中的已有软件 ID 保持原有含义。

Python 示例：

```python
import sys
from optics_photonics import environments
environments.register('lab-wave-model', '实验室波动模型',
    '研究组开发的波动传播程序', modules=['numpy'], distributions=['numpy'])
environments.bind('lab-wave-model', python=sys.executable, threads=2, concurrency=4)
```

随后用该 ID 提交完整研究程序、并行工作流或 episode 采样。C/C++、Java、Julia 等可执行程序使用 `kind='command'` 登记并绑定命令数组，沿用请求文件、输出目录和 JSON 结果接口。程序应将输出写入该任务的 OUTPUT_DIR，避免并行计算共享临时文件。登记不代替软件本身的安装与许可。

`optics-photonics connect portable --output DIR` creates an Agent Plugins package with root plugin.json, mcp.json and skills/.
MCP resources `optics://guides/optical-computation` and `optics://guides/optical-research` provide instructions on demand.
