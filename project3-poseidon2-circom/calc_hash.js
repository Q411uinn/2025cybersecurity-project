const poseidon = require("circomlibjs").poseidon;

function toHex(bigint) {
  return "0x" + bigint.toString(16);
}

async function main() {
  const poseidonLib = await poseidon.buildPoseidon();

  const inputs = [123456789n, 987654321n]; // bigint格式

  const hash = poseidonLib(inputs);

  const hashHex = poseidonLib.F.toString(hash);

  console.log("Calculated Poseidon hash:", hashHex);
}

main();
