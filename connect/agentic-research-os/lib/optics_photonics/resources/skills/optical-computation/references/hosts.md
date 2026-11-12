# Hosts

**Where it runs.** The MCP server and its background workers run on the computer that holds the scientific software. For a remote workstation, start the server there through SSH: `ssh -T USER@HOST /path/to/python -m optics_photonics mcp`. A worker outlives the agent session and the MCP process, but not the removal of its whole container or process group; when the agent's tool environment is disposable, connect to a persistent workstation instead.

**Remote results.** `read_result` and `read_array` return file content through the connection. `download_result` copies a file on the MCP host. The TypeScript client's `download` copies a file to the client's computer.

**Packages.** `optics-photonics connect HOST --output DIR` writes a package for `agentic-research-os`, `codex`, `claude`, `deepseek`, `qiushi`, `mcp` or `portable` (Agent Plugins); follow `DIR/INSTALL.md`. Research OS installs the directory containing `plugin.json` and activates the returned revision; DeepSeek uses the Cordis overlay or bundle; other hosts register the stdio command from `mcp.json`. `--python PATH` selects the interpreter that runs the connector (Python 3.10 or newer); scientific tools keep their own environments.

**Updates.** Install a new version into a new directory. Configuration, scientific environments and research records stay under `OPTICS_HOME` (default `~/.optics-photonics`) and are used by the new version.
