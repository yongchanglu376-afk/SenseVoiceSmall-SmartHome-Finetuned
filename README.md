# SenseVoiceSmall-SmartHome-Finetuned

基于 **SenseVoiceSmall** 全参数微调得到的中文智能家居语音识别模型。

本项目主要用于识别智能家居语音指令，例如：

- 打开空调
- 把温度调到二十五度
- 把灯光亮度调到百分之三十
- 洗碗机暂停工作
- 调整风量
- 控制家电开关

> 本项目不是从零训练的基础模型，而是在官方 **SenseVoiceSmall** 基础上进行全参数微调得到的衍生模型。

---

## 模型效果

在本项目固定的 **122 条独立智能家居测试集** 上：

| 模型 | CER | 完全正确 |
|---|---:|---:|
| 原始 SenseVoiceSmall | 24.2424% | 67 / 122（54.92%） |
| **微调后模型** | **5.1282%** | **102 / 122（83.61%）** |

CER 从 **24.2424%** 降到 **5.1282%**，相对下降约 **78.85%**。

> **注意：** 这个结果只代表本项目的智能家居语音测试集，不代表模型在所有中文语音识别场景中都能达到 5.1282% CER。

---

## 模型信息

| 项目 | 信息 |
|---|---|
| 基础模型 | `iic/SenseVoiceSmall` |
| 框架 | FunASR |
| 微调方式 | 全参数微调（Full-parameter Fine-tuning） |
| 参数量 | 约 234M |
| 发布精度 | FP32 |
| 模型文件大小 | 约 893 MiB |
| 当前版本 | v1.0.0 |

当前 v1.0 只发布经过完整验证的 **FP32 模型**，暂不提供 FP16 模型。

---

## 下载模型

模型权重不会直接放进 Git 仓库。

请前往本项目的 **Releases** 页面下载 `v1.0.0` 模型文件，并将模型解压到项目目录下。

建议目录结构：

```text
SenseVoiceSmall-SmartHome-Finetuned/
├── README.md
├── inference.py
├── requirements.txt
└── SenseVoiceSmall/
    ├── model.pt
    ├── config.yaml
    ├── configuration.json
    ├── am.mvn
    ├── tokens.json
    └── chn_jpn_yue_eng_ko_spectok.bpe.model
```

---

## 安装依赖

建议使用 **Python 3.11**。

```bash
pip install -r requirements.txt
```

本项目依赖基本与官方 SenseVoice 项目保持一致。

---

## 使用方法

准备一个 WAV 音频，例如：

```text
test.wav
```

如果模型目录为默认的 `./SenseVoiceSmall`，直接运行：

```bash
python inference.py test.wav
```

程序会自动选择设备：

- 检测到 CUDA 时默认使用 `cuda:0`
- 没有 CUDA 时使用 CPU

### 指定模型位置

如果模型不在默认目录：

```bash
python inference.py test.wav --model /path/to/SenseVoiceSmall
```

### 指定运行设备

使用 NVIDIA GPU：

```bash
python inference.py test.wav --device cuda:0
```

使用 CPU：

```bash
python inference.py test.wav --device cpu
```

### 运行示例

```bash
python inference.py cmd_0.wav
```

输出示例：

```text
Recognition result:
空调开到制热调到二十五度风量调到百分之三十
```

---

## 推理速度

测试环境：

| 项目 | 信息 |
|---|---|
| GPU | NVIDIA GeForce RTX 5090 D |
| 精度 | FP32 |
| batch size | 1 |

在全部 **1204 条语音** 上进行额外测试：

| 指标 | 结果 |
|---|---:|
| 音频总时长 | 3101.355 秒 |
| 总推理时间 | 43.037 秒 |
| 平均延迟 | 35.745 ms / 条 |
| P50 延迟 | 35.334 ms |
| P95 延迟 | 38.697 ms |
| RTF | 0.013877 |
| 实时倍速 | 约 72.06× |
| 峰值显存 | 952.52 MiB |

这 1204 条数据包含训练数据，因此这组结果主要用于 **完整语料回归检查和推理速度测试**。

用于模型效果对比的正式结果仍然是前面的：

**122 条独立测试集，CER = 5.1282%。**

---

## 数据集

清洗后的数据总量为 **1204 条**，固定划分如下：

| 数据集 | 数量 |
|---|---:|
| Train | 962 |
| Val | 120 |
| Test | 122 |
| **总计** | **1204** |

目前本项目 **不公开完整训练音频数据集**。

仓库主要提供：

- 微调后的模型
- 推理代码
- 使用方法

真实训练语音不会默认上传。

---

## 关于 FP16

本项目曾尝试把 FP32 模型转换为 FP16：

```text
约 893 MiB
↓
约 447 MiB
```

但当前 FunASR / SenseVoiceSmall 的 PyTorch 推理过程中存在部分 FP32 / FP16 类型混用问题。

为了保证下载后可以稳定使用，**v1.0 只发布经过完整验证的 FP32 模型。**

---

## 项目来源

本项目基于以下开源项目进行开发和微调：

- FunASR
- SenseVoice
- SenseVoiceSmall

**SenseVoiceSmall 是本项目的基础模型。**

本项目只针对智能家居语音场景对 SenseVoiceSmall 进行了微调，并不是从零训练一个新的基础语音模型。

感谢 FunASR、SenseVoice 以及相关项目作者的开源工作。

---

## 许可证

项目中的自编写代码和模型权重不是同一种许可。

模型权重属于 SenseVoiceSmall 的微调衍生模型，使用模型时请同时遵守 SenseVoiceSmall / FunASR 对应的模型许可证。

详细内容请查看：

```text
LICENSE
MODEL_LICENSE
```

---

## 快速开始

如果只是想直接使用模型，只需要：

```text
下载模型
↓
安装依赖
↓
准备 WAV 音频
↓
运行 inference.py
↓
得到识别文本
```

也就是：

```bash
pip install -r requirements.txt
python inference.py test.wav
```
