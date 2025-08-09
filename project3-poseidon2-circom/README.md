# project3: Poseidon2 Zero-Knowledge Proof Circuit
## 使用说明

本项目基于Poseidon2哈希函数，构建了适用于零知识证明（zk-SNARKs）的Circom电路。
支持t=2和t=3两种状态大小，灵活适配多种应用场景。
包含完整的电路实现、辅助模块、构建与证明脚本，助你快速上手零知识证明。

## 目录结构

circuits/              # Circom电路源代码
  ├─ poseidon2.circom      # 主电路：Poseidon2完整置换与哈希
  └─ utils/
       ├─ poseidon2_constants.circom  # 常量定义
       └─ poseidon2_round.circom      # 单轮置换逻辑
build/                 # 编译输出目录（生成的wasm、r1cs等）
input.json             # 示例输入数据
generate_witness.js    # witness生成脚本
setup.sh               # 一键构建与初始化脚本
README.md              # 项目说明文档


## 使用说明

1. 安装依赖:
```bash
npm install -g circom snarkjs
snarkjs --version
```

2. 编译电路:

```bash
circom poseidon2.circom --r1cs --wasm --sym -o build
```

3. 生成 zkey 文件（可信设置）：

```bash
snarkjs groth16 setup build/poseidon2.r1cs build/powersOfTau28_hez_final_10.ptau build/poseidon2_0000.zkey
```
4. 进行“贡献”阶段

```bash
snarkjs zkey contribute build/poseidon2_0000.zkey build/poseidon2_final.zkey --name="First contribution" -v
```
5.导出验证密钥（Verifier Key）：

```bash
snarkjs zkey export verificationkey build/poseidon2_final.zkey build/verification_key.json
```

6. 生成 witness:

```bash
node generate_witness.js
```

7. 生成证明:

```bash
snarkjs groth16 prove build/poseidon2_final.zkey witness.wtns proof.json public.json
```

8. 验证证明:
```bash
snarkjs groth16 verify build/verification_key.json public.json proof.json
```

## 使用说明
- 高性能：基于Poseidon2设计，优化哈希性能与证明效率
- 模块化：电路拆分合理，方便扩展与维护
- 一键化构建：自动下载所需参数，免去繁琐配置

## 关键成果：
- 解决了witness生成中接口变更的问题，适配最新witness-calculator。
-顺利完成了Windows环境下的setup与证明流程。
-生成了有效证明文件，实现了电路功能验证。