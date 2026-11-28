// Stateful code execution and shell commands from TypeScript.
// Run: npm install && npm run code-interpreter   (with E2B_API_KEY and E2B_DOMAIN=getrollouts.dev set)
import { Sandbox } from '@e2b/code-interpreter'

const sbx = await Sandbox.create()
try {
  await sbx.runCode('import pandas as pd; df = pd.DataFrame({"x": range(5)})')
  const sum = await sbx.runCode('int(df.x.sum())')
  console.log('sum computed in Python:', sum.text)

  const js = await sbx.runCode('const xs = [1, 2, 3]; xs.map(x => x * 2)', { language: 'js' })
  console.log('JavaScript in the sandbox:', js.text)

  await sbx.files.write('/home/user/hello.txt', 'hello from TypeScript\n')
  const cmd = await sbx.commands.run('cat /home/user/hello.txt && uname -sr')
  console.log(cmd.stdout.trim())
} finally {
  await sbx.kill()
}
