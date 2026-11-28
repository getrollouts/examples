"""Upload a data file, analyse it with pandas in the sandbox, download the results.

Your own data never has to be pasted into a prompt: upload the file, let the (model-written)
code work on it inside the sandbox, and take back only what you need.
"""
import base64
import csv
import io
import random

from e2b_code_interpreter import Sandbox

# Some sample data: daily sales per region
random.seed(1)
buf = io.StringIO()
w = csv.writer(buf)
w.writerow(["date", "region", "units", "price"])
for day in range(1, 91):
    for region in ("north", "south", "east", "west"):
        w.writerow([f"2026-{(day - 1) // 30 + 9:02d}-{(day - 1) % 30 + 1:02d}", region,
                    random.randint(20, 120), round(random.uniform(8, 12), 2)])

with Sandbox.create() as sbx:
    sbx.files.write("/home/user/sales.csv", buf.getvalue())

    summary = sbx.run_code("""
import pandas as pd
df = pd.read_csv('/home/user/sales.csv', parse_dates=['date'])
df['revenue'] = df.units * df.price
by_region = df.groupby('region').revenue.sum().sort_values(ascending=False).round(0)
by_region.to_csv('/home/user/revenue_by_region.csv')
by_region
""")
    print("revenue by region:\n" + summary.text)

    chart = sbx.run_code("""
import matplotlib.pyplot as plt
monthly = df.set_index('date').groupby('region').resample('MS').revenue.sum().unstack(0)
monthly.plot(kind='bar', figsize=(8, 4), title='Monthly revenue per region')
plt.tight_layout(); plt.show()
""")
    png = next(r.png for r in chart.results if r.png)
    with open("revenue.png", "wb") as f:
        f.write(base64.b64decode(png))

    table = sbx.files.read("/home/user/revenue_by_region.csv")
    with open("revenue_by_region.csv", "w") as f:
        f.write(table)
    print("saved revenue.png and revenue_by_region.csv")
