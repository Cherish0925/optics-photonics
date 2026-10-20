# Optics · Photonics — 软件目录

核查日期: 2026-10-20 | 96 个工具与产品族

原创目录说明与代码采用 MIT；被收录软件遵循各自许可。

按物理方法、许可和原生接口选择工具；原始资料随条目列出。

## 商业付费

### Ansys Zemax OpticStudio

ID: `opticstudio` | 几何光学与照明, 波动光学与传播

- **物理方法:** 顺序 / 非顺序光线追迹；物理光学传播
- **用途:** 镜头、成像像差、公差、杂散光和部分相干传播的综合设计环境。
- **编程入口:** ZOS-API .NET；Python、C#、C++、MATLAB；ZPL 宏；支持 Standalone 与交互连接。
- **计算环境:** 以 Windows 主程序为中心；后台实例仍需有效许可
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 厂商提供镜头、成像与照明工程应用及自动化示例。
- **适用边界:** 顺序光学、非顺序光学和 POP 的模型与数据接口不同；社区 MCP 的覆盖范围不能等同于全部 ZOS-API。
- **MCP (community):** [OpticStudioMCPServer；通过 ZOS-API 控制，社区实现](https://github.com/jaruiz6363/OpticStudioMCPServer)
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方 API 与示例](https://optics.ansys.com/hc/en-us/articles/42661773562899-Sample-code-for-ZOS-API-users)
- [官方连接模式](https://optics.ansys.com/hc/en-us/articles/42661790380179-ZOS-API-NET-An-Overview)

### Keysight CODE V

ID: `codev` | 几何光学与照明, 波动光学与传播

- **物理方法:** 成像光学设计与优化
- **用途:** 镜头初始设计、像差优化、公差分析和成像性能评估。
- **编程入口:** Macro-PLUS 脚本、命令与批量设计流程；具体外部自动化接口以安装版文档为准。
- **计算环境:** 本地授权软件；宏脚本驱动
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Keysight 官方成像光学产品，提供镜头及手机相机设计工作流。
- **适用边界:** 旧资料多标为 Synopsys CODE V；应按当前 Keysight 产品与文档查找。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [产品与 Macro-PLUS](https://www.keysight.com.cn/cn/zh/products/software/optical-solutions-software/optical-design-solutions/codev.html)

### Keysight LightTools

ID: `lighttools` | 几何光学与照明

- **物理方法:** 非顺序光线追迹 / 照明
- **用途:** 照明、导光、显示与杂散光；包含材料、散射和光源建模。
- **编程入口:** 内置宏与 LTAPI 自动化；有第三方 Python 封装。
- **计算环境:** 以桌面授权实例为中心
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 官方照明产品；有 CODE V → LightTools 的联合设计工作流。
- **适用边界:** Python 封装与主程序分别维护；光源和 BSDF 数据质量直接影响结果。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方产品](https://www.keysight.com/es/en/products/software/optical-solutions-software/optical-design-solutions/lighttools.html)
- [社区 Python 接口](https://github.com/Mestas/Lighttools)

### FRED

ID: `fred` | 几何光学与照明, 波动光学与传播

- **物理方法:** 非顺序追迹；相干与非相干光学
- **用途:** 复杂光机系统、散射、杂散光和激光系统的传播分析。
- **编程入口:** 内置脚本与 .frs 工作流；官方给出追迹—分析循环示例。
- **计算环境:** Windows；按版本支持多线程、分布式或 FREDmpc GPU 计算
- **许可:** 商业授权；另有需申请的大学免费许可，适用条件见官方页面
- **应用依据:** Photon Engineering 的工程产品，公开提供可执行脚本案例。
- **适用边界:** 已核实内置脚本；本表不把它标成完整、原生的 Python API。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方脚本循环](https://support.photonengr.com/article/176-raytrace-and-analysis-loop)
- [官方产品概览](https://photonengr.com/)
- [学术使用与免费申请条件](https://photonengr.com/academic-licenses)

### TracePro

ID: `tracepro` | 几何光学与照明

- **物理方法:** 蒙特卡洛光线追迹
- **用途:** 照明、杂散光、光通量与光机几何的分析和优化。
- **编程入口:** Scheme 宏；手册提供 DDE 与宏自动化说明。
- **计算环境:** 桌面程序；宏 / DDE 桥接
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Lambda Research 官方工程产品和 2026 用户手册。
- **适用边界:** 复杂桌面会话的生命周期需要额外管理；脚本接口不是 MCP。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [2026 官方用户手册](https://lambdares.com/hubfs/TracePro_Users_Manual_2026.pdf)
- [官方支持](https://lambdares.com/tracepro-2)

### OSLO

ID: `oslo` | 几何光学与照明

- **物理方法:** 顺序光学 / 镜头设计
- **用途:** 光学系统布局、像差、优化和公差计算。
- **编程入口:** CCL 编程与命令体系；具体功能取决于版本。
- **计算环境:** Windows；CCL 脚本
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Lambda Research 的镜头设计产品；另有独立 EDU 免费版本。
- **适用边界:** 商业版与 EDU 不能混为同一功能集合；免费版单列。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方产品](https://lambdares.com/oslo)
- [教育版说明](https://lambdares.com/edu)
- [官方 CCL 编程手册](https://lambdares.com/hubfs/Support/support/oslo/oslo_releases/OSLOProgramReference.pdf)

### ASAP

ID: `asap` | 几何光学与照明, 波动光学与传播

- **物理方法:** 非顺序光学 / 物理光学
- **用途:** 复杂光学系统、照明、散射与杂散光分析。
- **编程入口:** 官方集成 Python、VBScript 等脚本支持；可编写自动化分析流程。
- **计算环境:** 授权桌面 / 求解环境
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Breault Research Organization 官方光学分析产品。
- **适用边界:** 脚本宿主、对象模型和授权配置要与实际版本匹配。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方功能与脚本](https://breault.com/asap/)

### VirtualLab Fusion

ID: `virtuallab` | 波动光学与传播, 几何光学与照明, 周期结构与超表面

- **物理方法:** 场追迹 / 混合光学建模
- **用途:** 衍射、偏振、光栅、自由空间系统和复杂光学元件的联合建模。
- **编程入口:** 官方 Programming API、可编程元件与脚本；官方说明可扩展 Python / MATLAB 工作流。
- **计算环境:** Windows；产品内编程与外部工作流
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** LightTrans 官方波动光学平台；提供数字光学元件与应用库。
- **适用边界:** 不同求解器之间传递的是特定场表示；不能把所有混合计算视为一次全波 Maxwell 求解。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [编程 API](https://programmingreference.lighttrans.com/2026.2/api/VirtualLab.Programming.html)
- [官方说明](https://www.lighttrans.com/product/virtuallab-fusion/frequently-asked-questions/general-faqs.html)

### Ansys Speos

ID: `speos` | 几何光学与照明, 计算成像与重建

- **物理方法:** 光线输运 / 光度与视觉仿真
- **用途:** 照明、车灯、显示、传感器与人眼视觉相关的光机设计。
- **编程入口:** Speos 脚本；Ansys optical-automation 提供公开 Python 自动化与互操作代码。
- **计算环境:** 与 Ansys / CAD 产品环境配合
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Ansys 工程产品；官方维护光学自动化代码。
- **适用边界:** MIT 许可的是自动化库，不是 Speos 求解器；不同宿主可能使用 IronPython 或 CPython。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方自动化说明](https://optics.ansys.com/hc/en-us/articles/24752772596371-Optical-Automation-library-introduction)
- [自动化源码](https://github.com/ansys/optical-automation)

### Ansys Lumerical

ID: `lumerical` | 全波电磁与器件, 集成光子与版图, 周期结构与超表面

- **物理方法:** FDTD / 模态 / 多物理场 / 光子电路
- **用途:** FDTD、MODE、Multiphysics 与 INTERCONNECT 组成器件到电路的产品族。
- **编程入口:** lumapi Python；LSF 脚本；lumopt 逆向设计；lumslurm 调度。
- **计算环境:** 本地 / 集群；产品与 HPC 授权分别配置
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 官方应用库涵盖纳米光学、硅光器件和光收发链路。
- **适用边界:** Python 客户端和 MCP 不能替代求解器授权；不同产品的物理模型与输出不同。
- **MCP (official):** [Ansys 官方组织发布 PyLumerical MCP](https://github.com/ansys/pylumerical-mcp)
- **Agent Skill (community):** [Lumerical_MCP_Skill；社区技能与连接器](https://github.com/zxqcreations/Lumerical_MCP_Skill)

原始资料：
- [官方 Python API](https://optics.ansys.com/hc/en-us/articles/360037824513-Python-API-overview)
- [Ansys 官方 MCP 源码](https://github.com/ansys/pylumerical-mcp)

### COMSOL Multiphysics

ID: `comsol` | 全波电磁与器件, 几何光学与照明, 激光与精密干涉

- **物理方法:** FEM / 射线 / 多物理场
- **用途:** 波动光学、射线光学与热、结构、电荷等耦合；适合热光和应力光学模型。
- **编程入口:** 官方 Java API、批处理；LiveLink for MATLAB；Python 可通过第三方桥接。
- **计算环境:** Windows / Linux / macOS；批处理与服务器按许可
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 官方 API 与多物理场建模平台；光学功能需要对应模块。
- **适用边界:** 不要将第三方 Python 包说成官方 Python API；光学、热学、CAD 与并行许可需具体匹配。
- **MCP (community):** [comsol-mcp；社区实现](https://github.com/Ching-Chiang/comsol-mcp)
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方 API 总览](https://www.comsol.com/support/learning-center/article/overview-of-the-comsol-api-107912)
- [LiveLink](https://www.comsol.com/livelink-for-matlab)
- [社区 MCP](https://github.com/Ching-Chiang/comsol-mcp)

### CST Studio Suite

ID: `cst` | 全波电磁与器件, 周期结构与超表面

- **物理方法:** 时域 / 频域电磁 / 多物理场
- **用途:** 从射频、太赫兹到部分光学电磁问题；适合结构电磁响应与耦合。
- **编程入口:** 官方 Python 自动化；VBA 宏与批量求解流程。
- **计算环境:** 桌面建模 + 授权计算环境
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** SIMULIA 工程电磁软件，官方提供 Python 工作流。
- **适用边界:** 必须按波段设置材料色散与网格；免费 Learning Edition 不等于完整科研求解版。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方产品与 Python 工作流](https://www.3ds.com/products/simulia/cst-studio-suite)
- [官方 Python API 说明](https://blog.3ds.com/brands/simulia/cst-studio-suite-release-2021x-highlights/)

### Keysight RSoft Photonic Device Tools

ID: `rsoft` | 全波电磁与器件, 周期结构与超表面, 集成光子与版图, 激光与精密干涉

- **物理方法:** FDTD / BPM / RCWA / FEM / EME / 半导体激光
- **用途:** FullWAVE、BeamPROP、DiffractMOD、FemSIM、ModePROP、LaserMOD 等器件级工具。
- **编程入口:** 参数化 CAD、MOST 扫描与优化；脚本与外部集成能力按子产品确认。
- **计算环境:** 按模块配置；部分求解器支持 GPU / 集群
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Keysight 官方器件设计产品族；与 CODE V、LightTools、ADS 有工作流衔接。
- **适用边界:** 本表按产品族计一项；子模块不能被当作完全可互换的求解器。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方模块与接口生态](https://www.keysight.com/zz/en/products/software/optical-solutions-software/photonic-design-solutions.html)

### JCMsuite

ID: `jcm` | 全波电磁与器件, 周期结构与超表面, 集成光子与版图

- **物理方法:** 高阶 FEM / 电磁逆问题
- **用途:** 纳米光学、波导、散射、光刻与参数重建。
- **编程入口:** 官方 jcmwave Python；MATLAB / Octave、C 接口；优化与批量任务。
- **计算环境:** 本地 / 计算集群；Python 驱动
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** JCMwave 官方光子学仿真产品，提供完整接口文档。
- **适用边界:** 需要几何、网格和边界条件建模；优化接口不自动保证逆问题可辨识。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方接口](https://www.jcmwave.com/jcmsuite/interface/)
- [Python 入门](https://docs.jcmwave.com/JCMsuite/html/PythonInterface/bf647454e36069fd16f1a7a35cf6a865.html)

### Photon Design FIMMWAVE / FIMMPROP

ID: `photond` | 全波电磁与器件, 集成光子与版图, 光纤与通信

- **物理方法:** 模态分析 / EME
- **用途:** 波导与光纤模态、光子器件传播和模式转换。
- **编程入口:** 官方命令行、Python 与 MATLAB 脚本；社区 pyFIMM 可作封装参考。
- **计算环境:** 本地授权求解器；脚本驱动
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Photon Design 官方波导和器件设计工具。
- **适用边界:** 模态截断与传播分段需要收敛检查；其他 Photon Design 产品另有模型边界。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方脚本与优化](https://photond.com/fimmwave/features/scripting-optimisation)
- [功能表](https://photond.com/fimmwave/options/feature-option-table)

### Flexcompute Tidy3D

ID: `tidy3d` | 全波电磁与器件, 集成光子与版图, 周期结构与超表面

- **物理方法:** 云端 FDTD 与器件仿真
- **用途:** 以 Python 定义器件和仿真，调用云端求解与结果分析。
- **编程入口:** 官方 Python API、web.run 与批处理；官方 MCP / Agent 插件。
- **计算环境:** 本地建模与分析；求解运行在 Flexcompute 云端
- **许可:** 客户端 LGPL-2.1；云求解采用 FlexCredits / 商业计划
- **应用依据:** 公开案例、论文库与官方工业 / 科研客户应用。
- **适用边界:** 免费开源客户端不等于免费的本地求解器；MCP 的文档工具与执行能力需按桥接配置区分。
- **MCP (official):** [tidy3d-mcp / FlexAgent；文档及桥接工具](https://github.com/flexcompute/plugin-marketplace)
- **Agent Skill (official):** [flexagent；仿真编写、分析与文档使用](https://github.com/flexcompute/plugin-marketplace)

原始资料：
- [官方计费说明](https://docs.flexcompute.com/projects/tidy3d/en/stable/faq/docs/faq/How-is-using-Tidy3D-billed.html)
- [Python 客户端](https://github.com/flexcompute/tidy3d)
- [官方插件目录](https://github.com/flexcompute/plugin-marketplace)

### Luceda IPKISS

ID: `ipkiss` | 集成光子与版图

- **物理方法:** 参数化 PCell / 电路 / PDK
- **用途:** 把器件几何、端口、紧凑模型、版图和验证组织为可复用 PIC 设计。
- **编程入口:** 原生 Python 框架；PDK 包、器件仿真驱动与 Canvas 集成。
- **计算环境:** Python；本地授权与 PDK 环境
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 官方提供多家代工平台的 PDK 与流片设计流程。
- **适用边界:** 开源 PDK 不意味着 IPKISS 平台免费；PDK 的授权、工艺与模型覆盖独立判断。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方平台](https://www.lucedaphotonics.com/luceda-photonics-design-platform)
- [官方器件仿真接口](https://academy.lucedaphotonics.com/tutorials/device_sim/)

### VPIphotonics Design Suite

ID: `vpi` | 光纤与通信, 集成光子与版图, 激光与精密干涉

- **物理方法:** 光通信 / 光子电路与系统
- **用途:** 发射机、光纤链路、放大器、接收 DSP 与集成光子系统的联合仿真。
- **编程入口:** 官方外部仿真 API；Python、MATLAB、C++、COM 联合仿真与自定义模块。
- **计算环境:** 授权系统仿真环境；可与外部代码联合运行
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 厂商公开提供光通信与器件工程应用。
- **适用边界:** 系统级模型不等于器件级 Maxwell 求解；需明确采样率、噪声与信号归一化。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方接口功能](https://www.vpiphotonics.com/Tools/DesignSuite/Features/)
- [官方产品族](https://www.vpiphotonics.com/Tools/DesignSuite/)

### Optiwave OptiSystem

ID: `optisystem` | 光纤与通信, 集成光子与版图

- **物理方法:** 光通信链路与信号系统
- **用途:** 调制、光纤传输、放大、探测和误码性能计算。
- **编程入口:** Python / MATLAB 联合仿真组件；官方提供外部运行和结果访问示例。
- **计算环境:** 以桌面系统仿真工程为中心
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** Optiwave 官方工具，附带通信链路与协同仿真案例。
- **适用边界:** Python 组件用于嵌入算法，不应直接推断全部 GUI 功能都有无头 API。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方 Python 组件说明](https://optiwave.com/forums/topic/co-simulation-using-python/)
- [官方外部自动化说明](https://cdn.optiwave.com/wp-content/uploads/2017/11/OptiSystem_15_New_Features.pdf)

### Essential Macleod

ID: `macleod` | 薄膜与材料

- **物理方法:** 薄膜传输 / 优化 / 工艺分析
- **用途:** 多层镀膜、反射透射、色彩、群延迟及制造过程相关设计。
- **编程入口:** Function 扩展提供 BASIC 类脚本与对象访问；表格宏。
- **计算环境:** 本地桌面与内置脚本
- **许可:** 商业授权；Function 等扩展按产品配置
- **应用依据:** Thin Film Center 的镀膜设计和制造分析软件。
- **适用边界:** 脚本能力与所购扩展相关；没有把内置脚本冒充远程 Python API。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方产品](https://www.thinfilmcenter.com/essential.php)
- [Function 脚本](https://www.thinfilmcenter.com/function.php)

### OptiLayer / OptiRE / OptiChar

ID: `optilayer` | 薄膜与材料

- **物理方法:** 薄膜设计 / 表征 / 制造反演
- **用途:** 从多层膜优化到光谱反演与在线制造修正。
- **编程入口:** 官方 COM Automation；提供 Python 示例；OptiReOpt 面向生产集成。
- **计算环境:** Pro 有多平台版本；COM 自动化路径依赖平台
- **许可:** 商业授权；学术许可、模块与并发求解按合同配置
- **应用依据:** 官方明确提供生产控制软件集成与在线表征接口。
- **适用边界:** 跨平台 GUI 可用性不能推导 COM 跨平台可用；具体 Pro 接口需匹配版本。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [COM Automation](https://optilayer.com/com-automation/)
- [Python 示例说明](https://optilayer.com/development-history/new-features-in-optilayer-2018-version-12-83/)
- [平台下载](https://optilayer.com/downloads/)

### RP Fiber Power

ID: `rpfiber` | 光纤与通信, 激光与精密干涉

- **物理方法:** 光纤模态 / 增益 / 脉冲传播
- **用途:** 光纤激光器和放大器的泵浦、信号、ASE、动态与超短脉冲建模。
- **编程入口:** 内置脚本语言、自动生成脚本与自定义表单。
- **计算环境:** 本地产品；脚本定义模型与循环
- **许可:** 商业授权
- **应用依据:** RP Photonics 官方专用光纤设计产品。
- **适用边界:** 这是物理模型和脚本环境；外部通用 API 的覆盖本次未核实。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方接口](https://www.rp-photonics.com/rp_fiber_power_interface.html)
- [脚本语言](https://www.rp-photonics.com/software_script_language.html)

### RP Resonator / RP ProPulse

ID: `rpresonator` | 激光与精密干涉, 光纤与通信

- **物理方法:** 谐振腔 / 脉冲动力学
- **用途:** 激光腔模、稳定性与超短脉冲循环；两个产品按任务选用。
- **编程入口:** 内置脚本、交互表单生成模型、迭代循环。
- **计算环境:** 本地脚本化求解
- **许可:** 商业授权；两个产品分别配置
- **应用依据:** RP Photonics 官方激光与超快光学专用软件。
- **适用边界:** 腔模设计与非线性脉冲求解的假设不同，不能仅按“激光软件”互换。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方产品族](https://www.rp-photonics.com/software_overview.html)
- [ProPulse 脚本](https://www.rp-photonics.com/rp_propulse_interface.html)

### Crosslight APSYS / PICS3D

ID: `crosslight` | 激光与精密干涉, 全波电磁与器件

- **物理方法:** 光电半导体 TCAD
- **用途:** LED、半导体激光器及器件的电学、光学和热学联合建模。
- **编程入口:** 本次确认官方产品与仿真用途；公开通用 API / MCP 覆盖尚未核实。
- **计算环境:** 专用半导体器件仿真环境
- **许可:** 商业授权；按 TCAD 模块配置
- **应用依据:** Crosslight 官方列出 PICS3D 与半导体行业应用及科研发表。
- **适用边界:** 适合载流子—增益—温度相关器件问题；外部自动化需取得对应版本技术文档。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方产品与应用](https://crosslight.com/)

### SYNOPSYS Lens Design（OSD）

ID: `synopsys-osd` | 几何光学与照明

- **物理方法:** 镜头设计 / 优化
- **用途:** Optical Systems Design 的镜头设计软件，独立于原 Synopsys 光学软件业务。
- **编程入口:** 命令 / 宏驱动工作流；完整外部 API 本次未核实。
- **计算环境:** 桌面设计软件
- **许可:** 商业授权；官方试用为限时、限面数版本
- **应用依据:** OSD 官方仍提供产品与试用申请。
- **适用边界:** 不要与 CODE V、RSoft 原厂商 Synopsys 混淆；30 天试用不属于永久免费软件。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方获取与试用边界](https://osdoptics.com/accessinstallation/)
- [官方宏与操作指南](https://osdoptics.com/wp-content/uploads/2024/09/SYNOPSYSTM-Lens-Design-Software-Starting-Guide-Ui-Plus.pdf)

### TFCalc

ID: `tfcalc` | 薄膜与材料

- **物理方法:** 薄膜设计 / 光谱优化
- **用途:** 多层薄膜的光谱性能、设计和优化。
- **编程入口:** 本次未核实稳定公开 API；优先按桌面软件评估。
- **计算环境:** 桌面产品
- **许可:** 商业授权；现由 Hulinks 经营
- **应用依据:** 原作者网站明确说明 2022 年转由 Hulinks 经营。
- **适用边界:** 不沿用旧厂商与旧下载页作现行授权依据；自动化接口列为待确认。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [原作者的归属说明](https://www.sspectra.com/)
- [现厂商](https://www.hulinks.co.jp/en/)

### MATLAB / Simulink

ID: `matlab` | 推导与数字基础, 计算成像与重建, 光纤与通信

- **物理方法:** 数值计算 / 信号 / 控制系统
- **用途:** 光学算法开发、信号处理、参数估计、控制和系统级建模；工具箱按任务选择。
- **编程入口:** MATLAB Engine API、批处理、Simulink API；官方 MATLAB MCP Server。
- **计算环境:** 本地 / 服务器；GPU 与并行依赖工具箱和硬件
- **许可:** 商业 / 学术授权；工具箱单独授权
- **应用依据:** MathWorks 官方科学工程开发环境，官方已支持 Agent 接入。
- **适用边界:** 开源 MATLAB 脚本不等于免费运行；仅兼容 Octave 的代码才能免 MATLAB 执行。
- **MCP (official):** [MathWorks 官方 MATLAB MCP Server](https://github.com/matlab/matlab-mcp-server)
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方 MCP](https://github.com/matlab/matlab-mcp-server)
- [官方 Agent 使用说明](https://www.mathworks.com/help/cloudcenter/ug/run-matlab-with-ai-agentic-and-ai-assistant-applications.html)

### Wolfram Mathematica

ID: `mathematica` | 推导与数字基础, 量子光学

- **物理方法:** 符号推导 / 数值计算
- **用途:** 波动方程、近似展开、积分、矩阵及解析—数值联合推导。
- **编程入口:** Wolfram Language、wolframscript、官方 Python Client；官方 Wolfram MCP。
- **计算环境:** 本地或云端计算内核
- **许可:** Mathematica 商业授权；本地 MCP 需要相应授权内核
- **应用依据:** Wolfram 官方计算平台与 AgentTools。
- **适用边界:** 符号系统给出的解析式仍依赖参数域与假设；它不是光学场求解器的替代品。
- **MCP (official):** [Wolfram Local / Cloud MCP](https://www.wolfram.com/ai/mcp/)
- **Agent Skill (official):** [WolframResearch AgentSkills](https://github.com/WolframResearch/AgentTools)

原始资料：
- [官方 MCP](https://www.wolfram.com/ai/mcp/)
- [本地 MCP 文档](https://www.wolfram.com/artificial-intelligence/mcp/local/wolfram-mcp-local/)
- [官方 AgentTools](https://github.com/WolframResearch/AgentTools)

### Maple

ID: `maple` | 推导与数字基础

- **物理方法:** 计算机代数 / 数值与代码生成
- **用途:** 解析建模、符号推导、微分方程和可执行公式生成。
- **编程入口:** OpenMaple Python / C / Java API；命令行内核。
- **计算环境:** 本地计算内核与 API
- **许可:** 商业 / 学术授权
- **应用依据:** Maplesoft 官方数学计算平台与 OpenMaple 文档。
- **适用边界:** 适合推导与模型化简；不会自动提供完整的光学材料、边界与探测器模型。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方 Python API](https://jp.maplesoft.com/support/help/maple/view.aspx?path=OpenMaple%2FPython%2FAPI)
- [官方编程手册](https://www.maplesoft.com/documentation_center/maple2024/ProgrammingGuide.pdf)

## 免费与开源

### Meep

ID: `meep` | 全波电磁与器件, 周期结构与超表面, 集成光子与版图

- **物理方法:** FDTD / 伴随优化
- **用途:** 全波电磁传播、共振、散射与纳米光子器件。
- **编程入口:** Python、Scheme、C++；可脚本运行、输出 HDF5 和执行伴随优化。
- **计算环境:** CPU / MPI；不把标准版本默认标为 GPU 求解器
- **许可:** GPL-2.0 系列
- **应用依据:** MIT / NanoComp 开源科研工具，项目给出方法论文与示例。
- **适用边界:** 空间、时间、PML 和材料色散决定数值误差；大尺寸光机系统通常不适合整体 FDTD。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/NanoComp/meep)
- [源码许可](https://raw.githubusercontent.com/NanoComp/meep/HEAD/LICENSE)

### MPB

ID: `mpb` | 全波电磁与器件, 周期结构与超表面

- **物理方法:** 频域本征模 / 平面波
- **用途:** 光子晶体能带、模式和周期介质本征问题。
- **编程入口:** Python / Scheme；参数扫描和模式数据可程序化处理。
- **计算环境:** CPU / MPI
- **许可:** GPL-2.0 系列
- **应用依据:** MIT Photonic Bands，项目提供方法论文与教程。
- **适用边界:** 本征模求解不等于任意时域传播；需符合周期性、材料与边界假设。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/NanoComp/mpb)
- [源码许可](https://raw.githubusercontent.com/NanoComp/mpb/HEAD/COPYING)

### FDTDX

ID: `fdtdx` | 全波电磁与器件, 集成光子与版图

- **物理方法:** 可微 FDTD
- **用途:** 三维光子结构仿真与梯度驱动逆向设计。
- **编程入口:** 原生 Python / JAX；自动微分与程序化几何。
- **计算环境:** GPU；JAX 后端
- **许可:** MIT
- **应用依据:** 有公开实现与研究方法；适合可微仿真研究。
- **适用边界:** 新兴框架；模型覆盖、显存和材料支持应按当前 API 考察。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/ymahlau/fdtdx)
- [源码许可](https://raw.githubusercontent.com/ymahlau/fdtdx/HEAD/LICENSE)

### openEMS

ID: `openems` | 全波电磁与器件

- **物理方法:** EC-FDTD
- **用途:** 电磁、射频、太赫兹结构及相关波传播问题。
- **编程入口:** Python、Octave / MATLAB 接口；命令行求解。
- **计算环境:** CPU；并行能力按构建
- **许可:** GPL-3.0
- **应用依据:** 开源电磁求解器与公开教程。
- **适用边界:** 光频使用需检查材料色散、网格与接口支持，不能沿用射频默认模型。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/thliebig/openEMS)
- [源码许可](https://raw.githubusercontent.com/thliebig/openEMS/HEAD/COPYING)

### S⁴ / S4

ID: `s4` | 周期结构与超表面, 薄膜与材料

- **物理方法:** RCWA / Fourier modal
- **用途:** 周期层状结构、光栅和衍射级次的反射透射。
- **编程入口:** Lua 脚本；Python 接口依构建。
- **计算环境:** 本地 CPU；可批量调用
- **许可:** GPL-2.0 系列
- **应用依据:** Stanford Fan group 的分层周期结构求解器。
- **适用边界:** 有限尺寸边缘与孤立非周期物体不属于标准周期单胞模型。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/victorliu/S4)
- [源码许可](https://raw.githubusercontent.com/victorliu/S4/HEAD/COPYING)

### torcwa

ID: `torcwa` | 周期结构与超表面, 薄膜与材料

- **物理方法:** 可微 RCWA
- **用途:** 周期纳米结构、超表面单胞和光栅的梯度优化。
- **编程入口:** 原生 Python / PyTorch；自动微分。
- **计算环境:** CPU / CUDA GPU
- **许可:** LGPL-3.0
- **应用依据:** 项目有 TORCWA 方法论文与多个仿真示例。
- **适用边界:** 傅里叶阶数与材料不连续性影响收敛；周期边界不等于整片有限超透镜。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/kch3782/torcwa)
- [源码许可](https://raw.githubusercontent.com/kch3782/torcwa/HEAD/LICENSE)

### grcwa

ID: `grcwa` | 周期结构与超表面, 薄膜与材料

- **物理方法:** 可微 RCWA
- **用途:** 多层周期结构、衍射和拓扑优化研究。
- **编程入口:** Python；Autograd 后端。
- **计算环境:** CPU；按后端配置
- **许可:** GPL-3.0
- **应用依据:** 公开论文、接口和反射透射优化案例。
- **适用边界:** 不要将 Autograd 自动等同于 GPU；材料和周期模型需适配。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/weiliangjinca/grcwa)
- [源码许可](https://raw.githubusercontent.com/weiliangjinca/grcwa/HEAD/LICENSE)

### legume

ID: `legume` | 周期结构与超表面, 全波电磁与器件

- **物理方法:** GME / PWE / 可微本征问题
- **用途:** 光子晶体薄板、模态与辐射损耗相关分析。
- **编程入口:** Python；自动微分与优化工作流。
- **计算环境:** 本地数值计算
- **许可:** MIT
- **应用依据:** Fan group 的开源研究软件，具有方法文献。
- **适用边界:** 基于特定展开和截断；不是任意三维器件的通用时域引擎。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/fancompute/legume)
- [源码许可](https://raw.githubusercontent.com/fancompute/legume/HEAD/LICENSE)

### Ceviche

ID: `ceviche` | 全波电磁与器件, 集成光子与版图

- **物理方法:** 可微 FDFD / FDTD
- **用途:** 小规模电磁逆向设计和自动微分方法研究。
- **编程入口:** Python / Autograd；示例直接组合优化器。
- **计算环境:** 本地 CPU 数值求解
- **许可:** MIT
- **应用依据:** 对应 Maxwell 方程自动微分研究代码。
- **适用边界:** 适合研究原型与方法验证；不将其视为工业三维全流程平台。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/fancompute/ceviche)
- [源码许可](https://raw.githubusercontent.com/fancompute/ceviche/HEAD/LICENSE)

### tmm

ID: `tmm` | 薄膜与材料

- **物理方法:** 传输矩阵 TMM
- **用途:** 平面多层膜反射、透射、吸收，以及相干与非相干层组合。
- **编程入口:** 原生 Python / NumPy；coh_tmm、inc_tmm 等函数。
- **计算环境:** CPU；容易批量扫描与优化
- **许可:** MIT
- **应用依据:** 作者提供理论手册与薄膜吸收计算实现。
- **适用边界:** 标准平面分层模型；不描述任意横向图案、粗糙散射或有限光斑全部效应。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/sbyrnes321/tmm)
- [源码许可](https://raw.githubusercontent.com/sbyrnes321/tmm/HEAD/LICENSE.txt)

### Solcore

ID: `solcore` | 薄膜与材料, 全波电磁与器件

- **物理方法:** 光学 / 半导体 / 光伏模型
- **用途:** 将材料、薄膜吸收与太阳电池电学模型连接起来。
- **编程入口:** Python；TMM 等光学模块；与外部求解器的可选集成。
- **计算环境:** 本地 Python；外部模块另配
- **许可:** LGPL-3.0 系列
- **应用依据:** Imperial / QPV 研究生态的多尺度太阳电池工具。
- **适用边界:** 不是所有模型和外部依赖都随基础包安装；应按所选光学模型判断适用性。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方仓库](https://github.com/qpv-research-group/solcore5)
- [光学模型文档](https://docs.solcore.solar/en/latest/Optics/optics.html)
- [源码许可](https://raw.githubusercontent.com/qpv-research-group/solcore5/HEAD/LICENSE.txt)

### RayOptics

ID: `rayoptics` | 几何光学与照明

- **物理方法:** 几何光学 / 成像分析
- **用途:** 镜头建模、光线和波像差、近轴布局；可导入部分 Zemax / CODE V 格式。
- **编程入口:** Python 类与脚本；Jupyter 交互。
- **计算环境:** 本地 CPU
- **许可:** BSD-3-Clause
- **应用依据:** 公开光学设计软件与教程。
- **适用边界:** 文件导入不保证全部专有面型、涂层和优化操作数无损转换。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/mjhoptics/ray-optics)
- [源码许可](https://raw.githubusercontent.com/mjhoptics/ray-optics/HEAD/LICENSE)

### Optiland

ID: `optiland` | 几何光学与照明, 波动光学与传播

- **物理方法:** 可微光线追迹 / 光学设计
- **用途:** 镜头、自由曲面、偏振、涂层和可微成像系统的设计分析。
- **编程入口:** 原生 Python；NumPy / PyTorch 后端；JSON 与部分商业格式互操作。
- **计算环境:** CPU / CUDA GPU；自动微分
- **许可:** MIT
- **应用依据:** 持续开发的开源光学设计平台，有研究和工程示例。
- **适用边界:** 功能发展较快；不能仅凭格式导入或界面相似认定与商业产品完全等价。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/optiland/optiland)
- [源码许可](https://raw.githubusercontent.com/optiland/optiland/HEAD/LICENSE)

### Raysect

ID: `raysect` | 几何光学与照明, 散射与颗粒

- **物理方法:** 光谱光线追迹 / 辐射度学
- **用途:** 复杂场景和光谱辐射输运；支持定制材料、发射和探测模型。
- **编程入口:** Python / Cython API。
- **计算环境:** CPU；程序化场景
- **许可:** BSD-3-Clause
- **应用依据:** 用于科学光谱和辐射诊断建模的开源框架。
- **适用边界:** 主要跟踪辐射输运，不能直接替代相干波前干涉求解。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/raysect/source)
- [源码许可](https://raw.githubusercontent.com/raysect/source/HEAD/LICENSE.txt)

### DCC-Lab RayTracing

ID: `raytracing` | 几何光学与照明, 激光与精密干涉

- **物理方法:** 近轴 ABCD / 高斯光束
- **用途:** 快速搭建显微、望远和光束传输系统的近轴模型。
- **编程入口:** Python；光线矩阵、光束和光学系统对象。
- **计算环境:** 本地 Python
- **许可:** MIT
- **应用依据:** DCC-Lab 的公开工具与教程论文。
- **适用边界:** 近轴模型适合初步设计和解释，不替代高 NA、自由曲面或精密像差分析。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/DCC-Lab/RayTracing)
- [源码许可](https://raw.githubusercontent.com/DCC-Lab/RayTracing/HEAD/LICENSE)

### LightPipes

ID: `lightpipes` | 波动光学与传播, 激光与精密干涉

- **物理方法:** 标量衍射 / 光束传播
- **用途:** 自由空间衍射、透镜、孔径、干涉及相干光束演化。
- **编程入口:** Python 函数式接口；NumPy / SciPy / FFT。
- **计算环境:** 本地 CPU；可使用 FFT 加速库
- **许可:** BSD-3-Clause
- **应用依据:** 公开光学教学和科研软件，文档包含大量光学实验示例。
- **适用边界:** 采用的标量 / 近轴传播模型需要与数值孔径和传播距离相符。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/opticspy/lightpipes)
- [源码许可](https://raw.githubusercontent.com/opticspy/lightpipes/HEAD/LICENSE.txt)

### POPPY

ID: `poppy` | 波动光学与传播, 计算成像与重建

- **物理方法:** Fraunhofer / Fresnel / PSF
- **用途:** 望远镜、孔径、波前误差和点扩散函数仿真。
- **编程入口:** Python；光学平面与传播系统对象。
- **计算环境:** 本地；加速路径按版本与依赖
- **许可:** BSD-3-Clause
- **应用依据:** STScI 维护；被 JWST / Roman 相关 PSF 软件使用。
- **适用边界:** PSF 依赖正确的瞳面、采样和光谱权重；不是全波纳米结构求解器。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/spacetelescope/poppy)
- [源码许可](https://raw.githubusercontent.com/spacetelescope/poppy/HEAD/LICENSE.md)

### HCIPy

ID: `hcipy` | 波动光学与传播, 计算成像与重建

- **物理方法:** 高对比成像 / 自适应光学
- **用途:** 日冕仪、波前传感、湍流与 AO 反馈系统联合仿真。
- **编程入口:** Python；可组合传播器、探测器和控制模型。
- **计算环境:** 本地科学计算
- **许可:** MIT
- **应用依据:** 用于天文高对比成像仪器的端到端研究。
- **适用边界:** 控制环和大气模型需由使用者明确；不能由光学元件清单自动推导真实系统。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/ehpor/hcipy)
- [源码许可](https://raw.githubusercontent.com/ehpor/hcipy/HEAD/LICENSE)

### prysm

ID: `prysm` | 波动光学与传播, 几何光学与照明, 计算成像与重建

- **物理方法:** 物理光学 / 计量 / 波前拟合
- **用途:** PSF、MTF、波前与多项式拟合，以及成像系统建模。
- **编程入口:** Python；数组计算；支持不同数值后端。
- **计算环境:** CPU；可选 GPU 数组后端
- **许可:** MIT
- **应用依据:** 具有 JOSS 软件论文与公开光学建模接口。
- **适用边界:** 不同算法的归一化与采样条件要统一，尤其是接入实验图像时。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/brandondube/prysm)
- [源码许可](https://raw.githubusercontent.com/brandondube/prysm/HEAD/LICENSE.md)

### Diffractio

ID: `diffractio` | 波动光学与传播, 计算成像与重建

- **物理方法:** 标量与矢量衍射
- **用途:** 波前、掩模、偏振以及多种传播算法的仿真。
- **编程入口:** Python；XY / XZ 等网格和矢量场对象。
- **计算环境:** 本地数值计算；部分流程并行
- **许可:** GPL-3.0
- **应用依据:** 公开方法论文与光学教程。
- **适用边界:** 不同传播算法精度和适用范围不同；不能把所有算法的“矢量”支持视为全波求解。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/optbrea/diffractio)
- [源码许可](https://raw.githubusercontent.com/optbrea/diffractio/HEAD/LICENSE)

### TorchOptics

ID: `torchoptics` | 波动光学与传播, 计算成像与重建

- **物理方法:** 可微 Fourier 光学
- **用途:** 衍射元件、光学神经网络和光学—数字处理联合优化。
- **编程入口:** Python / PyTorch；torch.autograd。
- **计算环境:** CPU / GPU
- **许可:** MIT
- **应用依据:** 有公开软件论文与逆向设计示例。
- **适用边界:** 梯度可计算不等于模型适用；标量采样传播的近似仍存在。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/MatthewFilipovich/torchoptics)
- [源码许可](https://raw.githubusercontent.com/MatthewFilipovich/torchoptics/HEAD/LICENSE)

### waveprop

ID: `waveprop` | 波动光学与传播, 计算成像与重建

- **物理方法:** 标量衍射 / 可微传播
- **用途:** Fresnel、Fraunhofer、角谱传播及全息相关计算。
- **编程入口:** Python；可选 PyTorch 后端。
- **计算环境:** CPU / GPU，依后端
- **许可:** MIT
- **应用依据:** 项目包含全息与传播示例。
- **适用边界:** 频域采样、带限和零填充影响混叠；不是任意介质 Maxwell 求解。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/ebezzam/waveprop)
- [源码许可](https://raw.githubusercontent.com/ebezzam/waveprop/HEAD/LICENSE)

### gdsfactory

ID: `gdsfactory` | 集成光子与版图

- **物理方法:** 参数化版图 / PDK / 设计自动化
- **用途:** 用代码生成器件、端口、布线、网表和制造版图。
- **编程入口:** 原生 Python；YAML；输出 GDSII、OASIS 等。
- **计算环境:** 本地 Python；与 KLayout 及求解器协作
- **许可:** MIT 核心；商业服务、外部 PDK 与求解器独立授权
- **应用依据:** 项目有流片用户案例与公开 PDK 生态。
- **适用边界:** 版图生成器不是电磁求解器；制造规则、紧凑模型和 PDK 条款需另行匹配。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (official):** [项目仓库内 gdsfactory-component-designer Skill](https://github.com/gdsfactory/gdsfactory/blob/main/.agents/skills/gdsfactory-component-designer/SKILL.md)

原始资料：
- [项目与接口](https://github.com/gdsfactory/gdsfactory)
- [源码许可](https://raw.githubusercontent.com/gdsfactory/gdsfactory/HEAD/LICENSE)

### KLayout

ID: `klayout` | 集成光子与版图

- **物理方法:** 版图 / DRC / LVS
- **用途:** GDS / OASIS 编辑、参数化单元、版图规则与连通性检查。
- **编程入口:** Python pya / klayout.db、Ruby、批处理 CLI、宏插件。
- **计算环境:** 本地桌面或无 GUI 批处理
- **许可:** GPL-3.0
- **应用依据:** 广泛的开源版图和 PDK 工具生态；提供完整编程接口。
- **适用边界:** 几何与规则验证不会证明器件光学性能；DRC 需要有效规则集。
- **MCP (community):** [klayout-draw-mcp；可基于独立 Python 模块无 GUI 运行](https://github.com/geniuskey/klayout-draw-mcp)
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/KLayout/klayout)
- [源码许可](https://raw.githubusercontent.com/KLayout/klayout/HEAD/LICENSE)

### SAX

ID: `sax` | 集成光子与版图

- **物理方法:** S 参数光子电路 / 可微仿真
- **用途:** 以器件散射矩阵组装光子电路，进行快速扫描与优化。
- **编程入口:** Python / JAX；函数式模型与网表。
- **计算环境:** CPU / GPU，依 JAX 后端
- **许可:** Apache-2.0
- **应用依据:** 开源 PIC 电路建模与 gdsfactory 相关生态。
- **适用边界:** 结果取决于器件紧凑模型；S 参数端口、相位、频率网格和参考平面必须一致。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/flaport/sax)
- [源码许可](https://raw.githubusercontent.com/flaport/sax/HEAD/LICENSE)

### SiEPIC-Tools

ID: `siepic` | 集成光子与版图

- **物理方法:** KLayout 插件 / PIC 设计验证
- **用途:** 波导、端口、连通性、版图与工艺设计流程。
- **编程入口:** KLayout Python 插件；支持脚本式版图与 GUI 混合使用。
- **计算环境:** 本地 KLayout / Python
- **许可:** MIT；PDK 各自授权
- **应用依据:** SiEPIC 硅光教学、科研与制造设计生态。
- **适用边界:** 插件与 PDK、仿真后端是不同层；不能把插件许可扩大到代工工艺数据。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/SiEPIC/SiEPIC-Tools)
- [源码许可](https://raw.githubusercontent.com/SiEPIC/SiEPIC-Tools/HEAD/LICENSE.md)

### Nazca Design

ID: `nazca` | 集成光子与版图

- **物理方法:** 参数化光子版图
- **用途:** 用 Python 表达光子单元、连接与专业掩模版图。
- **编程入口:** 原生 Python；程序化单元和 GDS 输出。
- **计算环境:** 本地 Python
- **许可:** AGPL-3.0-or-later；商业服务与 PDK 独立
- **应用依据:** 作者明确面向商业与科研 PIC 设计工作。
- **适用边界:** AGPL 与 MIT 的分发和网络服务义务不同；外部工艺包另有条款。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [作者与许可](https://nazca-design.org/about/)
- [官方文档](https://nazca-design.org/manual/introduction.html)

### ADDA

ID: `adda` | 散射与颗粒, 全波电磁与器件

- **物理方法:** 离散偶极近似 DDA
- **用途:** 任意形状粒子的散射、吸收及部分基底附近的电磁问题。
- **编程入口:** 命令行输入；文本 / 文件输出；适合参数扫描包装。
- **计算环境:** CPU / MPI；支持 GPU 路径
- **许可:** GPL-3.0
- **应用依据:** 公开电磁散射方法与研究软件。
- **适用边界:** 需对偶极离散尺度和迭代收敛负责；体积规模增大会显著增加计算。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/adda-team/adda)
- [源码许可](https://raw.githubusercontent.com/adda-team/adda/HEAD/LICENSE)

### miepython

ID: `miepython` | 散射与颗粒

- **物理方法:** Mie 球散射
- **用途:** 球形粒子的散射效率、相函数和相关光学量。
- **编程入口:** 原生 Python；数组化计算。
- **计算环境:** CPU；可选 JIT
- **许可:** MIT
- **应用依据:** 作者提供方法说明、文献与可复用实现。
- **适用边界:** 球形、均匀介质等模型假设不可直接推广到任意形貌颗粒。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/scottprahl/miepython)
- [源码许可](https://raw.githubusercontent.com/scottprahl/miepython/HEAD/LICENSE.txt)

### treams

ID: `treams` | 散射与颗粒, 周期结构与超表面

- **物理方法:** T-matrix / 多重散射
- **用途:** 粒子簇、散射基底展开和相关光子结构的电磁计算。
- **编程入口:** Python；T 矩阵和基函数的程序化操作。
- **计算环境:** 本地数值计算
- **许可:** MIT
- **应用依据:** 具有方法文献的科学散射工具。
- **适用边界:** 需要适当的基组、阶数和粒子模型；并非自动网格化任意几何的软件。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/tfp-photonics/treams)
- [源码许可](https://raw.githubusercontent.com/tfp-photonics/treams/HEAD/LICENSE)

### SMUTHI

ID: `smuthi` | 散射与颗粒, 薄膜与材料

- **物理方法:** T-matrix + 层状介质散射
- **用途:** 多个粒子位于薄膜系统中或附近时的电磁散射。
- **编程入口:** Python；粒子、层结构与入射场对象。
- **计算环境:** 本地；加速能力按构建
- **许可:** MIT
- **应用依据:** 官方方法文档明确其多粒子—薄膜应用范围。
- **适用边界:** 单粒子 T 矩阵和多重散射展开均有适用与截断条件。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方模型与许可](https://smuthi.readthedocs.io/en/latest/_source/01%20about/about_smuthi.html)
- [项目代码](https://github.com/KMCzajkowski/smuthi)

### pyGDM

ID: `pygdm` | 全波电磁与器件, 散射与颗粒

- **物理方法:** Green dyadic / 体积分方法
- **用途:** 纳米结构近场、散射、发光与部分多物理光学分析。
- **编程入口:** pyGDM2 Python API；结构、激励、求解和后处理模块。
- **计算环境:** Python + 编译数值组件
- **许可:** GPL-3.0 系列
- **应用依据:** Peter Wiecha 团队的 CPC 方法论文与文档。
- **适用边界:** 离散体积与 Green 函数的环境假设要匹配；复杂几何的规模成本需评估。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [作者与论文](https://wiechapeter.gitlab.io/)
- [官方 API](https://homepages.laas.fr/pwiecha/pygdm_doc/apidoc.html)
- [原始仓库](https://gitlab.com/wiechapeter/pyGDM2)

### QuTiP

ID: `qutip` | 量子光学, 激光与精密干涉

- **物理方法:** 开放量子系统 / 主方程
- **用途:** 量子光学、腔 QED、耗散动力学、关联函数和控制。
- **编程入口:** Python；算符、态、求解器和扩展包。
- **计算环境:** CPU；扩展后端依模块
- **许可:** BSD-3-Clause
- **应用依据:** 长期维护的量子工具箱，原始与更新论文可查。
- **适用边界:** Hilbert 空间维度增长很快；标准模型不自动包含三维光学场和实际器件几何。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/qutip/qutip)
- [源码许可](https://raw.githubusercontent.com/qutip/qutip/HEAD/LICENSE.txt)

### QuantumOptics.jl

ID: `quantumoptics` | 量子光学

- **物理方法:** 量子动力学 / 主方程
- **用途:** 量子光学与多体小系统的算符、态和开放动力学。
- **编程入口:** Julia 原生 API。
- **计算环境:** Julia 数值环境
- **许可:** MIT
- **应用依据:** 公开科学软件与方法文档。
- **适用边界:** 适合显式物理模型；Agent 需要 Julia 执行环境而非只提供 Python。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/qojulia/QuantumOptics.jl)
- [源码许可](https://raw.githubusercontent.com/qojulia/QuantumOptics.jl/HEAD/LICENSE.md)

### Perceval

ID: `perceval` | 量子光学, 集成光子与版图

- **物理方法:** 光子量子电路
- **用途:** 单光子源、线性光学器件、Fock 态及测量的电路模拟。
- **编程入口:** Python；本地模拟与远程处理器接口。
- **计算环境:** 本地 CPU；远程平台为可选服务
- **许可:** MIT 本地软件；远程服务另有条件
- **应用依据:** Quandela 官方开源量子光子计算软件。
- **适用边界:** 本地开源模拟器不意味着真实量子硬件服务免费；不替代器件 Maxwell 仿真。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/Quandela/Perceval)
- [源码许可](https://raw.githubusercontent.com/Quandela/Perceval/HEAD/LICENSE)

### Strawberry Fields

ID: `strawberry` | 量子光学, 集成光子与版图

- **物理方法:** 连续变量量子光学
- **用途:** Gaussian / Fock 表示的光子量子电路和连续变量计算。
- **编程入口:** Python；电路语言与后端 API。
- **计算环境:** 本地数值后端
- **许可:** Apache-2.0
- **应用依据:** Xanadu 的公开研究工具与方法论文。
- **适用边界:** 仓库文档的 Python 依赖较旧；新环境选型需先检查兼容性，不能按最新框架无条件部署。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/XanaduAI/strawberryfields)
- [源码许可](https://raw.githubusercontent.com/XanaduAI/strawberryfields/HEAD/LICENSE)

### Luna.jl

ID: `luna` | 光纤与通信, 激光与精密干涉

- **物理方法:** 超快非线性传播 / UPPE / GNLSE
- **用途:** 超短脉冲、空芯光纤和非线性光学中的宽带传播。
- **编程入口:** Julia；高层传播接口和可扩展数值模块。
- **计算环境:** 本地 / 多核 Julia
- **许可:** MIT
- **应用依据:** LupoLab 超快光学研究软件，提供研究模型与示例。
- **适用边界:** 使用何种传播方程、模态和气体模型会改变适用范围；输入脉冲需含正确相位。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/LupoLab/Luna.jl)
- [源码许可](https://raw.githubusercontent.com/LupoLab/Luna.jl/HEAD/LICENSE)

### py-fmas

ID: `pyfmas` | 光纤与通信, 激光与精密干涉

- **物理方法:** 解析信号传播模型
- **用途:** 宽带脉冲、非线性光纤与超连续谱相关数值研究。
- **编程入口:** Python；模型、积分器与输出模块可组合。
- **计算环境:** 本地 CPU
- **许可:** MIT
- **应用依据:** 公开方法软件与例子库。
- **适用边界:** 不同模型的频谱、非线性与色散约定要一致；不是通用三维 Maxwell 平台。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/omelchert/py-fmas)
- [源码许可](https://raw.githubusercontent.com/omelchert/py-fmas/HEAD/LICENSE.md)

### laserfun

ID: `laserfun` | 光纤与通信, 激光与精密干涉

- **物理方法:** GNLSE / 非线性光纤
- **用途:** 以脉冲和光纤对象实现非线性脉冲传播与参数研究。
- **编程入口:** Python；Pulse、Fiber 与传播接口。
- **计算环境:** 本地 CPU
- **许可:** MIT
- **应用依据:** 公开非线性光学软件；从既有 PyNLO 生态发展。
- **适用边界:** 适合包络模型成立的光纤问题；版本与依赖需独立固定。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/laserfun/laserfun)
- [源码许可](https://raw.githubusercontent.com/laserfun/laserfun/HEAD/LICENSE)

### OptiCommPy

ID: `opticomm` | 光纤与通信

- **物理方法:** 光纤链路 / DSP / 信号统计
- **用途:** 从发送比特、器件、线性或非线性传输到相干接收与性能指标。
- **编程入口:** 原生 Python；器件模型、传播、DSP、FEC 与指标模块。
- **计算环境:** CPU；部分模型有 GPU 路径
- **许可:** GPL-3.0
- **应用依据:** 公开光通信研究框架与链路示例。
- **适用边界:** 链路级模型需明确采样、偏振、噪声及参数约定；器件结构设计要接其他求解器。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/edsonportosilva/OptiCommPy)
- [源码许可](https://raw.githubusercontent.com/edsonportosilva/OptiCommPy/HEAD/LICENSE)

### Finesse 3

ID: `finesse` | 激光与精密干涉, 波动光学与传播, 量子光学

- **物理方法:** 频域干涉仪 / 模态耦合
- **用途:** 复杂激光干涉仪、谐振腔、误差信号、噪声与控制相关建模。
- **编程入口:** Python；文本模型语法与程序化仿真。
- **计算环境:** 本地 Python / 编译核心
- **许可:** GPL-3.0 系列
- **应用依据:** LIGO 生态明确使用 Finesse 进行探测器建模。
- **适用边界:** 适合准静态频域与模态模型；大幅非线性瞬态需选择相应动力学工具。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方文档](https://finesse.ifosim.org/docs/latest/)
- [LIGO 实际建模包](https://finesse.docs.ligo.org/finesse-ligo/index.html)
- [源代码](https://git.ligo.org/finesse/finesse3)

### reZonator 2

ID: `rezonator` | 激光与精密干涉, 几何光学与照明

- **物理方法:** ABCD / 高斯光束 / 腔稳定性
- **用途:** 驻波腔、环形腔、单程光路和光束变换的快速计算。
- **编程入口:** 桌面 GUI 与工程文件；本次未核实完整、稳定的无头控制 API。
- **计算环境:** Windows / Linux / macOS 桌面
- **许可:** GPL-3.0
- **应用依据:** 作者提供公开源码、二进制与光学腔模型说明。
- **适用边界:** 对 LLM 的直接集成便利性低于 Python 库；模型以近轴矩阵为主。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方项目](https://github.com/orion-project/rezonator2)
- [许可](https://raw.githubusercontent.com/orion-project/rezonator2/HEAD/LICENSE)

### MCX

ID: `mcx` | 生物光子输运, 散射与颗粒

- **物理方法:** GPU 蒙特卡洛光子输运
- **用途:** 组织与复杂体素介质内的散射、吸收和时间相关光传播。
- **编程入口:** CLI / JSON；Python pmcx；MATLAB / Octave 接口。
- **计算环境:** CUDA GPU；具体后端按版本
- **许可:** GPL-3.0
- **应用依据:** 项目有方法论文和生物光子学研究应用。
- **适用边界:** 模拟辐射输运，不保留光学相位；不能直接描述散斑干涉或相干波前。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/fangq/mcx)
- [源码许可](https://raw.githubusercontent.com/fangq/mcx/HEAD/LICENSE.txt)

### MMC

ID: `mmc` | 生物光子输运, 散射与颗粒

- **物理方法:** 网格蒙特卡洛输运
- **用途:** 四面体网格中的组织光传播，处理曲面和异质组织几何。
- **编程入口:** CLI；Python pmmc；MATLAB / Octave 接口。
- **计算环境:** CPU / CUDA / OpenCL，依构建
- **许可:** GPL-3.0
- **应用依据:** 公开生物光子输运方法与研究实现。
- **适用边界:** 网格与光学参数必须来自可靠的组织模型；与 MCX 的体素表示不同。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/fangq/mmc)
- [源码许可](https://raw.githubusercontent.com/fangq/mmc/HEAD/LICENSE.txt)

### HoloPy

ID: `holopy` | 计算成像与重建, 散射与颗粒

- **物理方法:** 全息前向模型 / 参数推断
- **用途:** 用光散射模型生成全息图并拟合粒子等物理参数。
- **编程入口:** Python；散射、全息计算与推断接口。
- **计算环境:** CPU；依赖对应散射后端
- **许可:** GPL-3.0
- **应用依据:** Manoharan Lab 的全息与散射研究工具。
- **适用边界:** 可拟合参数取决于选定的散射模型；不是任意场景的通用三维重建。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/manoharan-lab/holopy)
- [源码许可](https://raw.githubusercontent.com/manoharan-lab/holopy/HEAD/LICENSE)

### pyDHM

ID: `pydhm` | 计算成像与重建, 波动光学与传播

- **物理方法:** 数字全息显微重建
- **用途:** 相移、离轴相位补偿、数值传播和复波场恢复。
- **编程入口:** Python 函数与示例。
- **计算环境:** 本地 Python
- **许可:** MIT
- **应用依据:** PLOS ONE 2022 软件论文及原作者仓库。
- **适用边界:** 算法适用于特定 DHM 架构；载频、采样与像差补偿需要与实验匹配。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [原作者项目](https://github.com/catrujilla/pyDHM)
- [算法文档](https://catrujilla.github.io/pyDHM/)
- [论文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275818)

### PyNX

ID: `pynx` | 计算成像与重建, X 射线与束线

- **物理方法:** CDI / Ptychography / 全息层析
- **用途:** 相干衍射和扫描衍射数据的 GPU 重建及晶体散射计算。
- **编程入口:** Python；官方命令行重建脚本。
- **计算环境:** CUDA / OpenCL GPU，依模块
- **许可:** CeCILL-B
- **应用依据:** ESRF 官方科研软件，提供束线数据处理脚本。
- **适用边界:** 面向相干 X 射线等实验；各重建算法的几何、数据格式与假设不同。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方文档与许可](https://pynx.esrf.fr/en/stable/)
- [CLI 文档](https://pynx.esrf.fr/en/stable/scripts/)

### Mitsuba 3

ID: `mitsuba` | 几何光学与照明, 计算成像与重建

- **物理方法:** 可微光谱渲染 / 逆渲染
- **用途:** 光谱、偏振和几何场景的光输运；优化材质、形状与相机参数。
- **编程入口:** Python-first API；Dr.Jit 自动微分；场景描述。
- **计算环境:** CPU / CUDA / OptiX，依变体
- **许可:** BSD-3-Clause
- **应用依据:** EPFL 研究渲染框架，服务计算成像与逆问题。
- **适用边界:** 渲染的辐射输运模型通常不等于相干衍射或 Maxwell 求解。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/mitsuba-renderer/mitsuba3)
- [源码许可](https://raw.githubusercontent.com/mitsuba-renderer/mitsuba3/HEAD/LICENSE)

### PBRT v4

ID: `pbrt` | 几何光学与照明, 计算成像与重建

- **物理方法:** 物理光线输运 / 渲染
- **用途:** 复杂场景、材质、相机与照明的可控图像生成。
- **编程入口:** C++；CLI 与文本场景；可由 Agent 生成并运行场景。
- **计算环境:** CPU / GPU（CUDA、OptiX）
- **许可:** Apache-2.0
- **应用依据:** 《Physically Based Rendering》配套公开实现和研究生态。
- **适用边界:** 用于辐射度图像形成；不要用“物理渲染”替代偏振干涉、衍射和光学计量模型。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/mmp/pbrt-v4)
- [源码许可](https://raw.githubusercontent.com/mmp/pbrt-v4/HEAD/LICENSE.txt)

### SRW

ID: `srw` | X 射线与束线, 波动光学与传播

- **物理方法:** 同步辐射 / 相干波前传播
- **用途:** 从电子轨迹和辐射源到束线光学的频域场与传播。
- **编程入口:** Python、C API；可选 IGOR Pro 前端。
- **计算环境:** CPU；并行工作流按实现
- **许可:** BSD-3-Clause；选择 Python 路径无需 IGOR Pro
- **应用依据:** 用于同步辐射源和束线设计的科研软件。
- **适用边界:** 同步辐射源、部分相干统计与传播要联合定义；通用相机仿真并非其主要目标。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方项目与 API](https://github.com/ochubar/SRW)
- [发行许可说明](https://pypi.org/project/oasys-srwpy/1.0.3/)

### SHADOW4 / OASYS

ID: `shadow` | X 射线与束线, 几何光学与照明

- **物理方法:** X 射线光线追迹 / 工作流
- **用途:** 同步辐射束线的镜、晶体、光栅与光束输运；OASYS 提供图形工作流。
- **编程入口:** SHADOW4 原生 Python；OASYS 插件；可编写批量模拟。
- **计算环境:** 本地 Python；GUI 为可选工作流
- **许可:** SHADOW4 MIT；OASYS 与插件以各自许可证为准
- **应用依据:** OASYS 项目组织维护的同步辐射光学工具。
- **适用边界:** OASYS 是集成环境，不是单一求解器；波动效应需相应模型或混合方法。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方 SHADOW4](https://github.com/oasys-kit/shadow4)
- [SHADOW4 MIT 许可](https://github.com/oasys-kit/shadow4/blob/master/LICENSE)
- [官方 OASYS 界面](https://github.com/oasys-kit/OASYS1-shadow4)

### xrt

ID: `xrt` | X 射线与束线, 几何光学与照明, 波动光学与传播

- **物理方法:** X 射线光线 / 波动追迹
- **用途:** 同步辐射光源、晶体、镜面与束线光学计算。
- **编程入口:** Python；程序化束线与批量分析。
- **计算环境:** CPU；部分计算可用 OpenCL
- **许可:** MIT
- **应用依据:** 公开 X 射线光学科研软件与文档。
- **适用边界:** 晶体衍射、源模型和统计采样各有适用范围；并非全波通用网格求解器。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/kklmn/xrt)
- [源码许可](https://raw.githubusercontent.com/kklmn/xrt/HEAD/LICENSE.txt)

### SymPy

ID: `sympy` | 推导与数字基础

- **物理方法:** 符号代数
- **用途:** 推导 Jones / ABCD 矩阵、色散关系、导数、积分与近似表达式。
- **编程入口:** Python；可生成数值函数和代码。
- **计算环境:** CPU
- **许可:** BSD-3-Clause
- **应用依据:** 具有软件论文的通用符号计算库。
- **适用边界:** 假设域、分支和近似条件需显式定义；不包含自动完备的光学物理模型。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/sympy/sympy)
- [源码许可](https://raw.githubusercontent.com/sympy/sympy/HEAD/LICENSE)

### SageMath

ID: `sage` | 推导与数字基础

- **物理方法:** 数学计算系统
- **用途:** 代数、方程、符号与数值研究；适合更复杂的理论推导。
- **编程入口:** Python 风格接口；CLI / Notebook。
- **计算环境:** 本地数学计算环境
- **许可:** GPL 系列；组合组件各自许可
- **应用依据:** 长期维护的开放数学软件。
- **适用边界:** 是理论计算基础设施，不是开箱即用的光学设计系统。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方主页与文档](https://www.sagemath.org/)

### FreeCAD

ID: `freecad` | 推导与数字基础, 几何光学与照明

- **物理方法:** 参数化机械 CAD
- **用途:** 光机支架、封装、几何装配与可制造结构；为仿真提供几何。
- **编程入口:** Python API；宏；插件。
- **计算环境:** 本地 CAD；可脚本建模
- **许可:** LGPL-2.1 系列；组件另有许可
- **应用依据:** 成熟开源工程 CAD 项目。
- **适用边界:** CAD 几何不会自动成为光学面、材料或边界条件；需语义转换。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/FreeCAD/FreeCAD)
- [源码许可](https://raw.githubusercontent.com/FreeCAD/FreeCAD/HEAD/LICENSE)

### Gmsh

ID: `gmsh` | 推导与数字基础, 全波电磁与器件

- **物理方法:** 几何 / 有限元网格
- **用途:** 为光学 FEM、热学和结构模型生成可控网格。
- **编程入口:** Python、C、C++、Julia API；CLI 与 .geo 脚本。
- **计算环境:** 本地 CPU
- **许可:** GPL；商业再许可另行提供
- **应用依据:** 成熟的科研有限元网格工具。
- **适用边界:** Gmsh 主要生成网格；还需要电磁 / 热学求解器和明确的物理边界。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方功能与许可](https://gmsh.info/)
- [官方手册](https://gmsh.info/doc/texinfo/)

### scikit-image

ID: `scikitimage` | 计算成像与重建, 推导与数字基础

- **物理方法:** 图像处理 / 重建算法
- **用途:** 实验图像的滤波、分割、配准、变换和定量分析。
- **编程入口:** 原生 Python API。
- **计算环境:** 本地 CPU
- **许可:** BSD-3-Clause 为主；个别文件见许可清单
- **应用依据:** 具有软件论文的科学图像处理生态。
- **适用边界:** 图像增强不等于恢复了真实光学信息；应与成像模型和噪声模型连接。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/scikit-image/scikit-image)
- [源码许可](https://raw.githubusercontent.com/scikit-image/scikit-image/HEAD/LICENSE.txt)

### napari

ID: `napari` | 计算成像与重建, 推导与数字基础

- **物理方法:** 多维图像 / 插件可视化
- **用途:** 观察图像、体数据、标签和实验重建结果；支持开发分析插件。
- **编程入口:** Python API、命令行、插件系统。
- **计算环境:** Qt / GPU 可视化；分析依插件
- **许可:** BSD-3-Clause
- **应用依据:** 开源科学成像生态。
- **适用边界:** 插件不是 LLM Skill；批量数值分析优先直接调用分析库，GUI 用于检查。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与接口](https://github.com/napari/napari)
- [源码许可](https://raw.githubusercontent.com/napari/napari/HEAD/LICENSE)

### refractiveindex.info database

ID: `refractiveindex` | 推导与数字基础, 薄膜与材料, 全波电磁与器件

- **物理方法:** 光学常数数据库
- **用途:** 提供材料折射率、消光系数及其文献来源，支撑各类光学模型。
- **编程入口:** 机器可读 YAML 数据；可由 Python 等读取；数据库本身不是求解器。
- **计算环境:** 本地数据或网站检索
- **许可:** CC0 数据库；原始文献单独归属
- **应用依据:** 公开光学常数数据库及数据来源。
- **适用边界:** 必须选对波长、温度、样品和测量条件；同名材料不能无条件共用一个 n、k。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [原始数据库](https://github.com/polyanskiy/refractiveindex.info-database)
- [CC0 许可](https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/HEAD/LICENSE)
- [网站](https://refractiveindex.info/)

### FEniCSx / DOLFINx

ID: `fenics` | 全波电磁与器件, 推导与数字基础

- **物理方法:** 自定义 FEM / 偏微分方程
- **用途:** 用变分形式实现 Helmholtz、Maxwell、热学等研究模型，适合需要修改方程的场景。
- **编程入口:** Python / C++；UFL 定义弱形式；MPI 与数值后端。
- **计算环境:** CPU / MPI；复数与后端依构建
- **许可:** DOLFINx LGPL-3.0-or-later；组件分别授权
- **应用依据:** FEniCS 官方开源有限元环境与方法文档。
- **适用边界:** 需要自行构造正确的函数空间、弱形式和边界；不是配置少量参数即可替代 COMSOL 的成套光学产品。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方项目](https://github.com/FEniCS/dolfinx)
- [官方网站](https://fenicsproject.org/)

### Netgen / NGSolve

ID: `ngsolve` | 全波电磁与器件, 推导与数字基础

- **物理方法:** 高阶 FEM / 电磁与多物理场
- **用途:** 电磁模态和自定义耦合方程；Netgen 提供相关网格能力。
- **编程入口:** Python / C++；官方 Maxwell 方程与本征模教程。
- **计算环境:** 本地 / 并行计算环境
- **许可:** LGPL-2.1；组件以具体许可为准
- **应用依据:** 官方给出电磁与多物理场教程和研究实现。
- **适用边界:** 需要自行定义离散空间、材料和边界；优势在于可修改方程与数值方法。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方项目](https://github.com/NGSolve/ngsolve)
- [Maxwell 教程](https://ngsolve.org/ngsolve/docs/i-tutorials/unit-2.4-Maxwell/Maxwellevp.html)

### NumPy / SciPy

ID: `scipy` | 推导与数字基础, 计算成像与重建

- **物理方法:** 数组 / 优化 / 拟合 / 信号计算
- **用途:** 承载光学数据处理、参数拟合、ODE、FFT、优化与统计，是多种专业库的底层。
- **编程入口:** 原生 Python；NumPy 数组、scipy.optimize、integrate、signal 等。
- **计算环境:** 本地 CPU；部分功能支持其他数组后端
- **许可:** BSD 系列；依赖和组件分别授权
- **应用依据:** 长期维护的科学 Python 基础生态。
- **适用边界:** 它们提供数值算法，不自动定义仪器或光学物理；应通过专业模型构建目标函数。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)

### JAX

ID: `jax` | 推导与数字基础

- **物理方法:** 自动微分 / JIT / 数值计算
- **用途:** 开发可微光学求解器、优化器和代理模型；FDTDX、SAX 等建立在其上。
- **编程入口:** Python；jit、grad、vmap 等变换。
- **计算环境:** CPU / GPU / TPU，依后端与安装
- **许可:** Apache-2.0
- **应用依据:** 开源数值与机器学习基础设施。
- **适用边界:** 自动微分不能消除离散误差或模型偏差；复数导数、精度和显存需与物理问题匹配。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方文档](https://docs.jax.dev/en/latest/)
- [官方源码](https://github.com/jax-ml/jax)

### PyTorch

ID: `pytorch` | 推导与数字基础, 计算成像与重建

- **物理方法:** 张量 / 自动微分 / 代理模型
- **用途:** 开发光学—算法联合模型、反演网络与快速代理；torcwa、TorchOptics 等使用其后端。
- **编程入口:** Python / C++；Autograd 与 GPU 张量接口。
- **计算环境:** CPU / GPU，依硬件与后端
- **许可:** BSD 系列；第三方组件见许可清单
- **应用依据:** 成熟机器学习与科学计算基础设施。
- **适用边界:** 代理网络的误差和适用参数域需要单独建立；网络输出不自动等于物理解。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方平台](https://pytorch.org/)
- [官方源码](https://github.com/pytorch/pytorch)

## 免费或授权受限

### PhotonForge Community

ID: `photonforge` | 集成光子与版图

- **物理方法:** PIC 设计 / 电路 / 版图验证
- **用途:** 本地版图、原理图、布线与电路仿真；可连接 Tidy3D 器件模型。
- **编程入口:** 原生 Python；官方 Agent 插件与多项 PCell、布线、验证 Skills。
- **计算环境:** 本地 Python；DRC / LVS 依赖 KLayout；器件求解在云端
- **许可:** Community 本地功能免费含商业用途；不据此认定全部源码开源；云器件求解计费
- **应用依据:** Flexcompute 官方 2.0 文档明确区分本地免费与云求解收费。
- **适用边界:** 官方 MCP 当前包含文档检索等工具；实际建模执行常由 Agent 运行 Python 完成。
- **MCP (official):** [PhotonForge 文档 MCP；与 Python 执行配合](https://github.com/flexcompute/plugin-marketplace)
- **Agent Skill (official):** [官方 PCell、验证、电路、版本与序列化 Skills](https://github.com/flexcompute/plugin-marketplace)

原始资料：
- [官方免费与收费边界](https://docs.flexcompute.com/projects/photonforge/en/latest/getting_started.html)
- [官方插件目录](https://github.com/flexcompute/plugin-marketplace)

### OSLO EDU

ID: `osloedu` | 几何光学与照明

- **物理方法:** 教育版镜头设计
- **用途:** 免费学习镜头布局、光线追迹和基本分析。
- **编程入口:** 命令 / 宏能力按 EDU 版范围；不能沿用商业版全部接口能力。
- **计算环境:** Windows 桌面
- **许可:** 免费闭源教育版；功能受限，官网称无需课程注册
- **应用依据:** Lambda Research 官方免费版本。
- **适用边界:** 适合教学和小模型；不作为完整工业镜头设计环境的等价替代。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [官方免费版本](https://lambdares.com/edu)

### PtyPy

ID: `ptypy` | 计算成像与重建, X 射线与束线

- **物理方法:** Ptychography 相位恢复
- **用途:** 相干衍射扫描成像的迭代重建与实验数据处理。
- **编程入口:** Python；MPI；CUDA / CuPy 等加速引擎。
- **计算环境:** 本地 / MPI / GPU，依引擎配置
- **许可:** Academic License：仅学术、非商业；源码公开但不是无使用领域限制的开源许可
- **应用依据:** 项目附有论文、实验重建模板与并行实现。
- **适用边界:** 公司研发、商业委托或服务使用不能直接按普通 MIT / BSD 项目处理。
- **MCP (unverified):** 本次未核实专用 MCP
- **Agent Skill (unverified):** 本次未核实专用 Agent Skill

原始资料：
- [项目与重建接口](https://github.com/ptycho/ptypy)
- [明确的学术许可](https://raw.githubusercontent.com/ptycho/ptypy/HEAD/LICENSE)

