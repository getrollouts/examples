"""Build your own template once, then start ready-to-work sandboxes from it in about a second.

Installing packages in every new sandbox costs time and money on each start. A template
bakes them in. The build runs on getrollouts.dev and takes a minute or two; you only
rebuild when your dependencies change.

    TEMPLATE_ALIAS=my-analyst python 10_custom_template.py
"""
import os
import time

from e2b import Template, default_build_logger
from e2b_code_interpreter import Sandbox

ALIAS = os.getenv("TEMPLATE_ALIAS", "my-analyst")

template = (
    Template()
    .from_template("code-interpreter-v1")
    .pip_install(["yfinance", "scikit-learn"])
)

print(f"building template '{ALIAS}' ...")
Template.build(template, alias=ALIAS, cpu_count=2, memory_mb=4096, on_build_logs=default_build_logger())

t0 = time.monotonic()
with Sandbox.create(ALIAS) as sbx:
    started = time.monotonic() - t0
    ex = sbx.run_code("import sklearn, yfinance; sklearn.__version__, yfinance.__version__")
    print(f"sandbox from '{ALIAS}' started in {started:.1f} s, packages ready: {ex.text}")
