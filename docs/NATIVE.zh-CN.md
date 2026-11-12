# 连接本机光学软件

原生会话连接器将本机 COMSOL、Lumerical、OpticStudio 与 CST 接入同一套后台任务。Agent 提供项目和研究程序；工作进程持有软件会话，在运行目录保存工作模型，执行程序并释放会话。独立项目可以并行；一个优化程序内部可以反复修改、求解同一个已加载的模型。

| 软件 | 连接方式 | 执行所在系统 | 操作能力 |
| --- | --- | --- | --- |
| Lumerical | 厂商 `lumapi` 或 `ansys.lumerical.core` | 厂商支持的 Windows / Linux 安装环境 | FDTD、MODE、DEVICE、INTERCONNECT 会话；项目读写、对象属性、求解、监视器数据与完整脚本 API |
| COMSOL | 社区 MPh 连接本机 COMSOL Java API | Windows / Linux / macOS | 模型读写、带单位参数、研究求解、表达式求值；完整 `MODEL.java` 与 `SESSION.java` |
| OpticStudio | 社区 ZOSPy 连接 ZOS-API | Windows | 独立会话、光学系统读写、镜头与非序列编辑器、原生分析、光线追迹与优化 |
| CST | 厂商 `cst.interface` 与 `cst.results` | 具体 SDK 支持的 Windows / Linux 环境 | 设计环境、项目读写、建模与历史命令、求解、结果树访问 |

## 首次连接

执行 `optics-photonics discover`；自定义软件安装位置可追加 `--root /software/location`。它按已知安装目录查找软件并返回 SDK 路径，不启动求解器。`bind-native` 在指定 Python 中检查模块是否可发现，然后保存连接设置；首个计算任务才会建立需要许可的软件会话。

```sh
optics-photonics bind-native lumerical --python /path/to/python --sdk-path /path/to/lumerical/api/python --threads 4
optics-photonics bind-native comsol --python /path/to/python-with-mph --threads 4
optics-photonics bind-native opticstudio --python /path/to/python-with-zospy
optics-photonics bind-native cst --python /path/to/vendor-compatible-python --sdk-path /path/to/python_cst_libraries
```

选择本机 SDK 支持的 Python，本工作进程要求 Python 3.9+。使用 MPh、ZOSPy 时，将对应桥接包安装到这个环境；桥接包不包含商业软件。`software_details` 返回包要求和原始 API 文档。`--options "@options.json"` 可指定 COMSOL 版本或 OpticStudio DLL 位置。Lumerical 可配置 `product`、`hide`、`module`，默认使用 FDTD。

MCP 对应工具是 `discover_native_software` 和 `bind_native_software`。环境只需配置一次，插件升级保留这些设置。已提交任务继续使用提交时的配置。COMSOL 与 Lumerical 接收线程数；CST 与 OpticStudio 的求解线程由其原生设置控制，公共调度器使用 `threads` 分配计算额度。

## 从项目开始计算

将项目绝对路径、实际存在的参数与表达式写入 `inputs.json`：

```json
{"project":"/work/optical-model.mph","parameters":{"wavelength":"1550[nm]"},"results":["ewfd.normE"]}
```

```sh
optics-photonics submit comsol solve_project --inputs "@inputs.json"
optics-photonics submit comsol --program research.py --inputs "@inputs.json"
```

`inspect_project` 打开项目并保存工作副本，不求解。`solve_project` 调用 COMSOL 研究、Lumerical 求解器或 CST 求解器；OpticStudio 根据具体分析编写原生程序。

程序获得 `INPUTS`、`OUTPUT_DIR`、`SDK`、`SESSION`、`MODEL`、`PROJECT_FILE` 和 `EXPORT(value, name)`，通过 `RESULT` 返回简洁 JSON。`MODEL` 是光学系统或项目；COMSOL 中为 MPh 模型，通过 `MODEL.java` 使用完整 Java API。工作模型在程序执行前及成功结束后保存。多维数组与复数场由 `EXPORT` 保存为 NPZ，并附 JSON 结构说明；大型数据也可直接使用软件自己的文件格式和流式写入。模型引用的材料、几何和外部数据仍按其项目路径配置。

[原生程序示例](../examples/native)包含 COMSOL 参数扫描、Lumerical 监视器数据提取、OpticStudio MTF 分析与 CST 结果导出，可依据实际研究项目修改。连接器的会话生命周期已通过替代 SDK 的自动检查；本开发环境未运行这些需要许可的商业求解器。正常结束与 Python 异常会关闭本任务持有的会话；强制取消终止工作进程树，树外的厂商服务需按其机制处理。

Agent 与求解器不必位于同一系统。例如，macOS 上的 Agent 可以通过 SSH 启动 Windows 工作站上的 MCP，并使用那台工作站的 OpticStudio。

原始资料：[Lumerical](https://optics.ansys.com/hc/en-us/articles/360041873053-Session-Management-Python-API)、[MPh 会话](https://mph.readthedocs.io/en/stable/api/mph.start.html)、[COMSOL 模型操作](https://mph.readthedocs.io/en/stable/api/mph.Model.html)、[ZOSPy](https://zospy.readthedocs.io/en/stable/api/zospy.zpcore.ZOS.html)、[OpticStudio MTF](https://zospy.readthedocs.io/en/stable/api/zospy.analyses.mtf.fft_mtf.FFTMTF.html)、[CST Python](https://events.3ds.com/python-driven-automation-electromagnetic-simulations)。CST 当前版本的 API 详见其安装目录中的 `Online Help/Python`。
