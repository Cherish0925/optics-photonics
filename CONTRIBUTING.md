# Contributing / 参与贡献

Contribute to the independent optical research environment: execution, scientific software, research programs, host connections and source-backed software descriptions.
欢迎参与执行机制、科学软件接入、研究程序、宿主连接和软件资料的开发。

## Development work / 开发任务

[Development handoff](docs/DEVELOPMENT.md) · [中文接力任务](docs/DEVELOPMENT.zh-CN.md)

Read current main, open PRs and related branches before starting. Use a separate branch for each coherent change and retain contributor attribution. A PR describes the resulting behavior, how to use it and which software/platform actually ran. Coordinate shared execution interfaces before changing them in parallel.

开始前查看主分支、现有 PR 与相关分支；在独立分支中完成一项连贯的改进。PR 说明实现后的行为、使用方式与实际运行环境，共同修改执行接口时先衔接设计。发布由维护者统一安排。

| Source / 源文件 | Purpose / 用途 |
| --- | --- |
| `src/optics_photonics/` | Execution, environments, scientific adapters, sampling and MCP / 执行、环境、科学软件接入、采样及 MCP |
| `native/executor/` | Native process execution / 原生进程执行 |
| `clients/typescript/` | Typed host client / 宿主客户端 |
| `skills/` and `data/` | Canonical research instructions and software descriptions / 研究说明与软件资料源文件 |
| `scripts/package_marketplace.py` | Generate the bundled Research OS plugin from source / 从源文件生成内置插件 |

Run the relevant existing workflows for the changed behavior. Changes bundled into the Research OS plugin also require `python scripts/package_marketplace.py`; edit canonical files rather than the generated `connect/agentic-research-os/lib` copies. Keep English and Chinese user-facing instructions aligned.

## Change an entry / 修改条目

1. Edit both `data/catalogue.en.json` and `data/catalogue.zh.json`. Keep the same `id`, `group`, `cats`, `route`, source URLs and MCP / Skill classification in both files.
2. Use primary sources: maintainer documentation, the actual license, vendor APIs, author papers or institutional pages. Attach the precise URL that supports a changed claim.
3. Separate physical capability, licensing and access method. An open client does not make its cloud solver free; a third-party wrapper is not a vendor API; a documentation MCP is not a solver controller.
4. Describe one meaningful limitation and the application basis. Avoid unsupported claims such as “industry standard”, “best”, or “fully validated”.
5. Run `python scripts/build.py` and `python -m unittest discover -s tests`. Commit the generated files with the source change.

中英文保持相同编号与事实字段；用途说明可以按语言自然表达。许可依据应来自许可证或厂商条款，接口依据应来自实际 API 文档或实现。未知的信息明确保留为未知。

## Add a tool / 新增工具

Choose a stable lowercase identifier. Use existing domains where they fit and avoid splitting a product family into numerous modules solely to increase the count. Record the executable interface, compute needs and external dependencies. Follow `data/schema.json`.

新增工具须有清晰用途、可追溯资料和可判断的授权状态；商业、开源、受限免费分别归组。欢迎精确纠错，也欢迎附带小型可运行示例。

## Layout and build / 展示与构建

The two HTML editions must remain independently usable offline. Do not introduce external font, script or analytics dependencies. Preserve keyboard navigation, native readable content without JavaScript, mobile layouts, filtering, comparison and exports.

`src/render.py` contains the shared page renderer. `src/strings.en.json` localizes its static Chinese text at build time; `src/resources.py` builds the bilingual resource index. English output must contain no untranslated Chinese except the language-switch label.

## Attribution / 许可

Contributions of original code and descriptions are provided under this repository's MIT license. Link to third-party manuals instead of copying them into the repository. Preserve notices for any bundled assets.
