"""A small Linux VM: run shell commands, write and read files, start background jobs."""
from e2b import Sandbox

sbx = Sandbox.create(timeout=600)  # template: base; killed automatically after 10 minutes
try:
    print(sbx.commands.run("uname -sr && nproc && free -m | head -2").stdout)

    sbx.files.write("/home/user/data.csv", "name,score\nada,92\nlinus,87\n")
    print(sbx.files.read("/home/user/data.csv"))

    sbx.commands.run("pip install --quiet cowsay")
    print(sbx.commands.run("python3 -c \"import cowsay; cowsay.cow('hello from the sandbox')\"").stdout)

    job = sbx.commands.run("sleep 2 && echo done > /home/user/job.txt", background=True)
    job.wait()
    print("background job wrote:", sbx.files.read("/home/user/job.txt").strip())
finally:
    sbx.kill()
