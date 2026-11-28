"""Clone a repository, install it and run its test suite, with output streamed live.

The typical job of a coding agent or a SWE-bench style eval: check out code, apply a
change, run the tests, read the result. The output arrives line by line while it runs.

    REPO=https://github.com/pallets/itsdangerous python 11_run_repo_tests.py
"""
import os

from e2b import CommandExitException, Sandbox

REPO = os.getenv("REPO", "https://github.com/pallets/itsdangerous")

with Sandbox.create(timeout=900) as sbx:
    stream = dict(on_stdout=lambda line: print(line, end=""), on_stderr=lambda line: print(line, end=""))

    sbx.commands.run(f"git clone --depth 1 {REPO} /home/user/repo", timeout=120, **stream)
    sbx.commands.run("cd /home/user/repo && pip install -q . pytest freezegun", timeout=300, **stream)

    try:
        r = sbx.commands.run("cd /home/user/repo && python -m pytest -q", timeout=600, **stream)
        print(f"\ntests passed (exit {r.exit_code})")
    except CommandExitException as e:
        print(f"\ntests failed (exit {e.exit_code})")
