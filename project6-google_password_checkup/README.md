# Google密码核查 DDH私有交集求和协议

本项目实现了论文（Section 3.1）中描述的 DDH-based Private Intersection-Sum 协议的教学性 Python demo。  
实现要点：使用乘法群 (Z_p^*) + 自实现 Paillier 同态加密，模拟三轮交互并返回交集对应值的和（由 P2 得到）。


## 使用说明
1. 安装依赖库：
```bash
pip install -r requirement.txt
```
2. 运行示例演示：
```bash
python demo.py

```
本演示模拟了两方在各自拥有的标识符集合上，私下计算交集中对应值的加和，且不泄露额外信息。

## 文件
-paillier.py - Paillier 密码学实现（密钥生成/加密/解密/同态加法/随机化）
-protocol.py - 协议主要逻辑（P1/P2 的三轮流程）
-demo.py - 演示脚本，直接运行显示交集求和结果