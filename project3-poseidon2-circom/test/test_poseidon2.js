const { execSync } = require('child_process');

try {
  execSync('node build/poseidon2_js/generate_witness.js build/poseidon2_js/poseidon2.wasm inputs/input.json build/witness.wtns', { stdio: 'inherit' });
  console.log('witness generated');
} catch(e) {
  console.error('generate witness failed', e);
}