// Run the same job in several sandboxes at once.
// Run: npm run parallel   (CONCURRENCY=5 on trial accounts)
import { Sandbox } from 'e2b'

const n = Number(process.env.CONCURRENCY ?? 5)
const t0 = Date.now()

const results = await Promise.all(
  Array.from({ length: n }, async (_, i) => {
    const sbx = await Sandbox.create()
    try {
      const r = await sbx.commands.run(`python3 -c "import random; random.seed(${i}); print(sum(random.random() for _ in range(10**6)))"`)
      return `sandbox ${i}: ${r.stdout.trim()}`
    } finally {
      await sbx.kill()
    }
  }),
)

results.forEach((line) => console.log(line))
console.log(`${n} sandboxes in ${((Date.now() - t0) / 1000).toFixed(1)} s`)
