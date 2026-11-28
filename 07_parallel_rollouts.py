"""Many rollouts in parallel: run candidate solutions against tests, one sandbox each.

This is the core loop of code evals and RL training: a model proposes solutions, every
solution runs in its own isolated sandbox, and only the score comes back. Here the
candidates are hard-coded; in a real setup they come from your model.

    CONCURRENCY=5 python 07_parallel_rollouts.py      # trial accounts allow 5 at a time
    CONCURRENCY=50 python 07_parallel_rollouts.py     # paid accounts allow 50
"""
import asyncio
import os
import time

from e2b import AsyncSandbox, CommandExitException

CONCURRENCY = int(os.getenv("CONCURRENCY", "5"))

# Candidate implementations of "return the n-th Fibonacci number (fib(0) = 0)".
# Some are right, some are subtly wrong, one never terminates.
CANDIDATES = [
    "def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n",
    "def fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n",
    "def fib(n):\n    a, b = 1, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n",
    "def fib(n):\n    a, b = 0, 1\n    for _ in range(n - 1):\n        a, b = b, a + b\n    return b\n",
    "def fib(n):\n    while True:\n        pass\n",
    "import functools\n@functools.cache\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n",
    "def fib(n):\n    return round(((1 + 5 ** 0.5) / 2) ** n / 5 ** 0.5)\n",
    "def fib(n):\n    return [0, 1, 1, 2, 3, 5, 8][n]\n",
] * 3  # 24 rollouts

TESTS = """
from solution import fib
cases = {0: 0, 1: 1, 2: 1, 7: 13, 20: 6765, 30: 832040}
passed = 0
for n, want in cases.items():
    try:
        passed += fib(n) == want
    except Exception:
        pass
print(f"{passed}/{len(cases)}")
"""

# Price of the 'base' template (2 vCPU, 512 MiB), see https://getrollouts.dev/#pricing
PRICE_PER_SECOND = (2 * 0.040 + 0.5 * 0.013) / 3600


async def rollout(i: int, code: str, gate: asyncio.Semaphore) -> dict:
    async with gate:
        start = time.monotonic()
        sbx = await AsyncSandbox.create(timeout=120)
        try:
            await sbx.files.write("/home/user/solution.py", code)
            await sbx.files.write("/home/user/test_solution.py", TESTS)
            try:
                r = await sbx.commands.run("cd /home/user && timeout 10 python3 test_solution.py", timeout=30)
                score = r.stdout.strip()
            except CommandExitException as e:  # non-zero exit: crash or timeout
                score = "timeout" if e.exit_code == 124 else "error"
        finally:
            await sbx.kill()
        return {"i": i, "score": score, "seconds": time.monotonic() - start}


async def main() -> None:
    gate = asyncio.Semaphore(CONCURRENCY)
    t0 = time.monotonic()
    results = await asyncio.gather(*(rollout(i, c, gate) for i, c in enumerate(CANDIDATES)))
    wall = time.monotonic() - t0

    for r in results:
        print(f"rollout {r['i']:2d}: {r['score']:>8}  ({r['seconds']:.1f} s)")
    full = sum(1 for r in results if r["score"] == "6/6")
    sandbox_seconds = sum(r["seconds"] for r in results)
    print(f"\n{full}/{len(results)} candidates pass all tests")
    print(f"wall time {wall:.1f} s with {CONCURRENCY} in parallel, {sandbox_seconds:.0f} sandbox-seconds")
    print(f"approx. cost: ${sandbox_seconds * PRICE_PER_SECOND:.4f}")


asyncio.run(main())
