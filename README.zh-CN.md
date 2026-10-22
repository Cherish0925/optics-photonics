<p align="right"><b>中文</b> · <a href="README.md">English</a></p>

![Optics · Photonics — 软件、物理模型与可编程接口](docs/assets/readme-header.webp)

# 光学与光子学软件目录

面向光学科研、工程开发与 AI Agent 的双语工具目录，并加入贯穿全部子领域的统一物理基础：**场 + 物质 + 相互作用**。

**96 个工具与产品族 · 14 个领域 · 200 个文档与接口资料入口**

| 阅读与浏览 | 数据与资料 | 参与开发 |
| --- | --- | --- |
| [中文 HTML](https://cherish0925.github.io/optics-photonics/index.zh.html) · [English HTML](https://cherish0925.github.io/optics-photonics/) | [中文 JSON](data/catalogue.zh.json) · [English JSON](data/catalogue.en.json) | [Agent 入口](llms.txt) · [贡献说明](CONTRIBUTING.md) |
| [中文 Markdown](docs/catalogue.zh.md) · [English Markdown](docs/catalogue.en.md) | [资料索引](data/resources.zh.json) · [数据结构](data/schema.json) | [代码示例](examples/) · [本地开发](#本地开发) |
| [基础框架](docs/foundations.zh.html) · [Foundations](docs/foundations.html) | [中文源文件](foundations/README.zh-CN.md) | **场 · 物质 · 相互作用** |

也可以下载[中文 HTML](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/docs/index.zh.html)或[英文 HTML](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/docs/index.html)，直接用浏览器打开。两个文件分别内嵌完整数据、样式、脚本和中文字体子集，搜索、筛选、比较与导出均可离线使用；原始网站与文档链接需要联网。

## 统一物理基础

本仓库使用一个简洁但可以贯穿不同尺度与理论层级的物理框架：

> **光学 / 光子学 = 场 + 物质 + 相互作用**

这里的**场**包括经典与量子化电磁场及其状态；**物质**包括微观自由度、材料、器件与探测器；**相互作用**描述二者之间的能量、动量与信息交换。自由传播属于场动力学；光学器件是结构化物质；测量本质上是被设计好的场—物质相互作用。这个框架同时覆盖量子光学、纳米光子学、激光、光纤、成像、光谱、波动光学与几何光学，同时保留各有效理论的适用边界。

完整内容见[中文基础框架](docs/foundations.zh.html)与 [English Foundations](docs/foundations.html)，可维护的 Markdown 源文件位于 [`foundations/`](foundations/)。

## 包含什么

- **29 项商业付费、64 项免费开源、3 项免费但授权或功能受限**。开源客户端、收费求解器、学术专用许可和外部 PDK 分别说明。
- 每项记录物理方法、用途、编程接口、运行环境、许可、应用依据、适用边界与原始资料。
- API、命令行、宏与 **官方／社区／未核实的 MCP、Agent Skills** 分别标注；文档检索 MCP 不被当成求解器执行接口。
- 按任务、软件名称和接口检索，按领域与授权筛选，最多四项并排比较，导出 CSV 或 JSON。
- 集中的资料目录把官网、手册、代码、许可证和 Agent 接入资料关联到对应软件。
- 七类物理模型、六条可组合工作流、数字孪生与代理模型说明，以及四组实际接口示例。

## 从物理模型连接数字实验室

| 任务链 | 软件之间传递什么 | 目录中的工具示例 |
| --- | --- | --- |
| 镜头 → 图像 → 反演 | 瞳面复场、像差、PSF、采样与探测器响应 | OpticStudio、CODE V、Optiland、prysm、POPPY |
| 单胞 → 超表面 → 系统 | 复数透反射、偏振、角度和波长依赖 | torcwa、grcwa、Meep、Lumerical、Tidy3D、Diffractio |
| 版图 → 器件 → 电路 | 工艺层、端口、参考平面和归一化 S 参数 | gdsfactory、KLayout、IPKISS、JCMsuite、SAX |
| 脉冲 → 链路 → 接收 | 复包络、时间网格、色散、非线性与噪声 | Luna、py-fmas、RP Fiber Power、VPI、OptiCommPy |
| 光机热 → 腔模 → 读出 | 热致形变、折射率变化、工作点和噪声谱 | COMSOL、Finesse、HCIPy |
| 样品 → 传播 → 重建 | 实际观测量及其对应的前向算子 | MCX、MMC、PyNX、pyDHM、HoloPy |

这些是建模组合建议。统一物理量、单位、参考系和近似条件，才能把不同软件连接成可信的计算链。

## 给 AI Agent 的入口

先读取 [`llms.txt`](llms.txt)，再按任务读取完整 [Markdown](docs/catalogue.zh.md)、[`llms-full.txt`](llms-full.txt) 或 JSON。两种语言使用同一套稳定编号 `id`，便于搜索、引用和自动更新。

```python
import json
from urllib.request import urlopen

url = "https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/catalogue.zh.json"
tools = json.load(urlopen(url))
candidates = [t for t in tools
              if t["group"] == "open"
              and "periodic" in t["cats"]
              and t["route"] == "api"]
for tool in candidates:
    print(tool["id"], tool["api"], tool["sources"])
```

读取对应原始文档、准备运行环境，再调用软件原生接口。连接器分别标注功能范围及官方、社区、未核实三种来源状态。

## 本地开发

需要 Python **3.10+**，构建仅使用标准库：

```bash
git clone https://github.com/Cherish0925/optics-photonics.git
cd optics-photonics
python scripts/build.py
python -m unittest discover -s tests
python -m http.server 8000 --directory docs
```

浏览 `http://localhost:8000/index.zh.html`。修改 `data/catalogue.zh.json` 与 `data/catalogue.en.json` 后重新构建；数据、翻译和页面渲染分别维护。生成的 HTML 一并提交，读者无需安装开发环境。

目录说明、技术细节和英文项目介绍见 [README.md](README.md)。欢迎补充遗漏工具、修正许可和接口、增加可复现示例及改进翻译，具体格式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 范围与许可

资料核查日期为 **2026-10-20**，依据厂商文档、维护者仓库、许可证与作者资料。每项保留应用依据、模型条件和来源链接。

本项目原创代码与目录说明采用 [MIT](LICENSE) 许可。被收录软件、外部文档、PDK 和数据仍遵循各自许可；内嵌字体采用 [SIL OFL 1.1](docs/assets/FONT_LICENSE.txt)。详见 [NOTICE](NOTICE)。
