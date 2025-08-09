const circomlibjs = require("circomlibjs");

async function main() {
  const poseidon = await circomlibjs.buildPoseidon();

  const F = poseidon.F;

  // 输入转换成BigInt
  const inputs = [123456789n, 987654321n];

  // 计算hash
  const hash = poseidon(inputs);

  const hashStr = F.toString(hash);

  console.log("Calculated Poseidon hash:", hashStr);
}

main().catch(console.error);
