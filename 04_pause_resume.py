"""Pause keeps memory and files, billing stops. Resume brings the same Python session back."""
import time

from e2b_code_interpreter import Sandbox

sbx = Sandbox.create(timeout=600)
sbx.run_code("counter = 41; import os; open('/home/user/note.txt', 'w').write('still here')")
sandbox_id = sbx.sandbox_id

t = time.time()
sbx.pause()
print("paused in %.1f s, sandbox id %s" % (time.time() - t, sandbox_id))

t = time.time()
sbx = Sandbox.connect(sandbox_id)  # resumes the paused sandbox
print("resumed in %.1f s" % (time.time() - t))

print("variable:", sbx.run_code("counter + 1").text)  # 42: the Python process kept running state
print("file:", sbx.files.read("/home/user/note.txt"))
sbx.kill()
