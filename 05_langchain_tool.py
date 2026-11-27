"""A code tool for LangChain / LangGraph agents. One sandbox per conversation keeps state between tool calls.

Without ANTHROPIC_API_KEY the script only calls the tool directly, so you can check the sandbox part on its own.
"""
import os

from e2b_code_interpreter import Sandbox
from langchain_core.tools import tool

sbx = Sandbox.create(timeout=3600)


@tool
def run_python(code: str) -> str:
    """Run Python code in a persistent sandbox. Returns stdout, results and errors."""
    ex = sbx.run_code(code)
    if ex.error:
        return f"{ex.error.name}: {ex.error.value}\n{ex.error.traceback}"
    out = "".join(ex.logs.stdout)
    res = "\n".join(r.text for r in ex.results if r.text)
    return (out + res) or "(no output)"


try:
    print("tool check:", run_python.invoke({"code": "import sys; print(sys.version.split()[0]); 6 * 7"}))

    if os.environ.get("ANTHROPIC_API_KEY"):
        from langchain.agents import create_agent

        agent = create_agent("anthropic:claude-sonnet-5-5", tools=[run_python])
        reply = agent.invoke({"messages": [{"role": "user",
                              "content": "Compute the 30th Fibonacci number and the mean of the first 30."}]})
        print(reply["messages"][-1].content)
    else:
        print("set ANTHROPIC_API_KEY to run the agent as well")
finally:
    sbx.kill()
