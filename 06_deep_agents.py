"""Deep Agents with the official E2B backend (langchain-e2b): file tools and shell commands run in the sandbox.

Without ANTHROPIC_API_KEY the script only checks the backend, so you can test the sandbox part on its own.
"""
import os

from e2b import Sandbox
from langchain_e2b import E2BSandbox

sbx = Sandbox.create(timeout=3600)  # template: base (shell, Python, git)
backend = E2BSandbox(sandbox=sbx)
try:
    r = backend.execute("python3 --version && git --version")
    print("backend check:", r.exit_code, r.output.strip())

    if os.environ.get("ANTHROPIC_API_KEY"):
        from deepagents import create_deep_agent

        agent = create_deep_agent(
            model="anthropic:claude-sonnet-5-5",
            backend=backend,
            system_prompt="You are a coding agent. Work in /home/user and test what you write.",
        )
        result = agent.invoke({"messages": [{"role": "user",
                               "content": "Write fib.py with a fib(n) function and a test, then run the test."}]})
        print(result["messages"][-1].content)
    else:
        print("set ANTHROPIC_API_KEY to run the agent as well")
finally:
    sbx.kill()
