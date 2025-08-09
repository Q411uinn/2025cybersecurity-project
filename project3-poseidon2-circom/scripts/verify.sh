#!/bin/bash
set -e
echo "Verify proof using snarkjs:"
# snarkjs groth16 verify verification_key.json build/public.json build/proof.json
echo "Uncomment and provide verification_key.json to run verification."
