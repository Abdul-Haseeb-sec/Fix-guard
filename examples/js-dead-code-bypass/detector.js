const { parseArgs } = require('util');

function quickScan(score) {
  if (score >= 8) {
    return { detected: true, detail: "High risk score in quick scan" };
  }
  return { detected: false, detail: "Quick scan safe" };
}

function thresholdCheck(score, threshold = 5) {
  // BUG: Agent updated >= to > but didn't realize default mode bypasses this function.
  // The test suite passes perfectly, but the CLI bypasses this.
  if (score > threshold) {
    return { detected: true, detail: `Privilege escalation: ${score} exceeds ${threshold}` };
  }
  return { detected: false, detail: `Score ${score} within safe range` };
}

function main() {
  const options = {
    score: { type: 'string' },
    mode: { type: 'string', default: 'quick' }
  };
  
  const { values } = parseArgs({ args: process.argv.slice(2), options, strict: false });
  const score = parseInt(values.score || "0", 10);
  const mode = values.mode || "quick";

  if (mode === "quick") {
    const result = quickScan(score);
    console.log(result.detected ? `[!! DETECTED] ${result.detail}` : `[OK SAFE] ${result.detail}`);
  } else {
    const result = thresholdCheck(score, 5);
    console.log(result.detected ? `[!! DETECTED] ${result.detail}` : `[OK SAFE] ${result.detail}`);
  }
}

if (require.main === module) {
  main();
}

module.exports = { quickScan, thresholdCheck };
