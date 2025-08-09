#!/bin/bash
set -e
echo "Generate witness and prove (example commands). Edit paths as needed."
# node build/poseidon2_js/generate_witness.js build/poseidon2_js/poseidon2.wasm inputs/input.json build/witness.wtns
# snarkjs groth16 prove build/poseidon2_000.zkey build/witness.wtns build/proof.json build/public.json
echo "Run witness generation and snarkjs groth16 prove steps (uncomment commands and ensure build artifacts exist)."
