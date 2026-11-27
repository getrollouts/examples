"""Every port gets a public HTTPS URL: start a web server in the sandbox and open it in your browser."""
import os
import time
import urllib.request

from e2b import Sandbox

sbx = Sandbox.create(timeout=300)
try:
    sbx.files.write("/home/user/site/index.html", "<h1>Hello from a sandbox</h1>")
    sbx.commands.run("cd /home/user/site && python3 -m http.server 8000", background=True)

    url = "https://" + sbx.get_host(8000)
    for _ in range(20):  # the server needs a moment to start
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                print("status", r.status, "body:", r.read().decode().strip())
                break
        except Exception:
            time.sleep(0.5)
    print("open this in your browser for the next minute:", url)
    time.sleep(int(os.environ.get("KEEP_OPEN", "60")))
finally:
    sbx.kill()
