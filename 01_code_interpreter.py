"""Stateful Python in a sandbox: variables survive between calls, charts come back as PNG."""
import base64

from e2b_code_interpreter import Sandbox

with Sandbox.create() as sbx:  # template: code-interpreter-v1 (2 vCPU, 2 GiB)
    sbx.run_code("import pandas as pd; df = pd.DataFrame({'x': range(10), 'y': [v * v for v in range(10)]})")
    print("sum of y:", sbx.run_code("int(df['y'].sum())").text)

    ex = sbx.run_code("import matplotlib.pyplot as plt; plt.plot(df['x'], df['y']); plt.title('y = x^2'); plt.show()")
    png = next(r.png for r in ex.results if r.png)
    with open("chart.png", "wb") as f:
        f.write(base64.b64decode(png))
    print("chart saved to chart.png")

    ex = sbx.run_code("1 / 0")
    print("errors come back as data:", ex.error.name, ex.error.value)

    js = sbx.run_code("const xs = [1, 2, 3]; xs.map(x => x * 2)", language="js")
    print("JavaScript works too:", js.text)
