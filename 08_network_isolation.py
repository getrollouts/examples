"""Lock a sandbox down: no internet, an allowlist, and a private public URL.

Every sandbox is its own Firecracker microVM. Sandboxes cannot reach each other or any
internal address. Outbound internet is open by default and you can restrict it per sandbox.
See https://getrollouts.dev/docs#security
"""
import time
import urllib.error
import urllib.request

from e2b import Sandbox

CHECK = (
    "for u in https://example.com https://pypi.org/simple/; do "
    "printf '%s ' $u; curl -s -m 8 -o /dev/null -w '%{http_code}\\n' $u || echo blocked; done"
)


def show(title: str, sbx: Sandbox) -> None:
    out = sbx.commands.run(CHECK, timeout=30).stdout.replace(" 000", " blocked")
    print(f"--- {title}\n{out}")


# 1. Default: outbound internet is open
with Sandbox.create() as sbx:
    show("default", sbx)

# 2. No outbound internet at all, e.g. for untrusted code that should only compute
with Sandbox.create(allow_internet_access=False) as sbx:
    show("allow_internet_access=False", sbx)

# 3. Allowlist: only the hosts you name, everything else is denied
with Sandbox.create(network={"allow_out": ["example.com"], "deny_out": ["0.0.0.0/0"]}) as sbx:
    show("allowlist example.com", sbx)

# 4. Private public URL: ports are only reachable with the sandbox's traffic token
with Sandbox.create(network={"allow_public_traffic": False}) as sbx:
    sbx.commands.run("python3 -m http.server 8000", background=True)
    time.sleep(2)
    url = "https://" + sbx.get_host(8000)
    for label, headers in (
        ("without token", {}),
        ("with token", {"e2b-traffic-access-token": sbx.traffic_access_token}),
    ):
        try:
            status = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=10).status
        except urllib.error.HTTPError as e:
            status = e.code
        print(f"--- allow_public_traffic=False, {label}: HTTP {status}")
