# getrollouts.dev examples

Runnable examples for [getrollouts.dev](https://getrollouts.dev): hosted, E2B-compatible cloud sandboxes for AI agents,
running as Firecracker microVMs on servers in Switzerland.

The examples use the official E2B SDKs without any changes. The only difference to running them against E2B is one
environment variable, `E2B_DOMAIN=getrollouts.dev`.

## Setup

1. Create an account in the [portal](https://getrollouts.dev/portal). The free trial gives you credit without a card.
2. Install the SDK and set two environment variables:

```bash
pip install -r requirements.txt            # e2b, e2b-code-interpreter
export E2B_API_KEY=e2b_...                 # from the portal
export E2B_DOMAIN=getrollouts.dev
```

For the agent examples (05, 06) also install `requirements-agents.txt` and set `ANTHROPIC_API_KEY`.
Without a model key they still check the sandbox part and skip the agent.

## Examples

| File | What it shows |
|---|---|
| [01_code_interpreter.py](01_code_interpreter.py) | Stateful Python like a notebook, pandas, charts as PNG, errors as data, JavaScript |
| [02_commands_and_files.py](02_commands_and_files.py) | Shell commands, reading and writing files, `pip install`, background jobs |
| [03_public_url.py](03_public_url.py) | A web server inside the sandbox with a public HTTPS URL |
| [04_pause_resume.py](04_pause_resume.py) | Pause keeps memory and files while billing stops; resume brings the same session back |
| [05_langchain_tool.py](05_langchain_tool.py) | A code tool for LangChain and LangGraph agents with one sandbox per conversation |
| [06_deep_agents.py](06_deep_agents.py) | Deep Agents with the official E2B backend (`langchain-e2b`) |
| [07_parallel_rollouts.py](07_parallel_rollouts.py) | Many candidate solutions scored in parallel, one sandbox each, with wall time and cost (evals, RL) |
| [08_network_isolation.py](08_network_isolation.py) | No internet, an outbound allowlist, and public URLs that need a token |
| [09_data_analysis.py](09_data_analysis.py) | Upload a CSV, analyse it with pandas in the sandbox, download chart and results |
| [10_custom_template.py](10_custom_template.py) | Build a template with your packages once, then start ready sandboxes from it |
| [11_run_repo_tests.py](11_run_repo_tests.py) | Clone a repository, install it and run its tests with live output |
| [typescript/](typescript) | The same from TypeScript: code interpreter, commands, parallel sandboxes |

Run any of them with `python 01_code_interpreter.py`. Trial accounts allow 5 sandboxes at a time, so
`07_parallel_rollouts.py` defaults to `CONCURRENCY=5`.

## Good to know

- Sessions last up to 24 hours on paid accounts (1 hour on the trial). Set the length with `Sandbox.create(timeout=...)`
  or extend it with `sbx.set_timeout(...)`.
- Paused sandboxes cost nothing and are kept for 30 days after the last pause.
- Larger ready-made templates: `code-interpreter-8g` (2 vCPU, 8 GiB) and `code-interpreter-16g` (4 vCPU, 16 GiB).
- Billing is per second while a sandbox runs, prepaid, with no monthly fee. See [pricing](https://getrollouts.dev/#pricing)
  and the [comparison with E2B](https://getrollouts.dev/vs-e2b).

More in the [docs](https://getrollouts.dev/docs) and the
[LangChain, LangGraph and Deep Agents guide](https://getrollouts.dev/guides/langchain).

getrollouts.dev is an independent service and is not affiliated with E2B.

## License

MIT, see [LICENSE](LICENSE).
