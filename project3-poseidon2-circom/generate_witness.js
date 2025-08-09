const fs = require('fs');
const path = require('path');
const wcModule = require('./build/poseidon2_js/witness_calculator.js');

async function main() {
  console.log("开始读取wasm和输入...");
  const wasmBuffer = fs.readFileSync(path.join(__dirname, 'build/poseidon2_js/poseidon2.wasm'));
  const input = JSON.parse(fs.readFileSync(path.join(__dirname, 'input.json'), 'utf8'));

  console.log("初始化WitnessCalculator...");
  const witnessCalculator = await wcModule(wasmBuffer);

  console.log("计算witness并生成wtns文件...");
  const wtnsBuffer = await witnessCalculator.calculateWTNSBin(input, 0);
  fs.writeFileSync(path.join(__dirname, 'witness.wtns'), wtnsBuffer);

  console.log("witness.wtns生成完成");
}

main().catch(err => {
  console.error("运行出错:", err);
});
