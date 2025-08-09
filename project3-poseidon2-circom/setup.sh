# 1. 编译电路
.\circom.exe circuits/poseidon2.circom --r1cs --wasm --sym -o build

# 2. 下载powersOfTau文件
if (-Not (Test-Path "./powersOfTau28_hez_final_10.ptau")) {
    Invoke-WebRequest -Uri "https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_10.ptau" -OutFile "powersOfTau28_hez_final_10.ptau"
}

# 3. setup
.\snarkjs.exe groth16 setup build/poseidon2.r1cs powersOfTau28_hez_final_10.ptau build/poseidon2_0000.zkey

# 4. 贡献随机数生成最终zkey
.\snarkjs.exe zkey contribute build/poseidon2_0000.zkey build/poseidon2_final.zkey --name="First contribution" -v -e="random entropy"

# 5. 导出验证键
.\snarkjs.exe zkey export verificationkey build/poseidon2_final.zkey build/verification_key.json

Write-Host "Setup 完成"
