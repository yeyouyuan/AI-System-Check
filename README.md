# AI System Check (AI系统检测工具)

[English](#english) | [中文](#中文)

<a name="english"></a>
## English

### Introduction
AI System Check is a tool designed to evaluate whether your local system is suitable for deploying AI models. It assesses your hardware configuration and provides targeted recommendations.

### Features
- Comprehensive Hardware Detection
  - CPU information (model, cores, frequency, usage)
  - GPU information (model, memory, CUDA support)
  - Memory information (total, available, usage)
  - Disk information (partition space usage)
- Smart Scoring System
  - CPU score (based on core count and frequency)
  - GPU score (based on VRAM size)
  - Memory score (based on total capacity)
  - Disk score (based on available space)
- Detailed Reports
  - Saved as text file
  - Complete system information
  - AI deployment recommendations

### Requirements
- Python 3.8+
- Windows/Linux/MacOS

### Dependencies
```
psutil>=5.9.0
py-cpuinfo>=9.0.0
GPUtil>=1.4.0
torch>=2.0.0
```

### Installation
1. Clone or download this project
2. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Using Tsinghua mirror (for users in China)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Usage
Run the main program:
```bash
python system_check.py
```
The program will automatically detect system configuration and generate a report, which will be displayed in the console and saved as `system_report.txt`.

### Scoring Criteria
1. CPU Score (max 100 points)
   - Physical cores >= 8 (50 points)
   - Base frequency >= 2GHz (50 points)

2. GPU Score (max 100 points)
   - VRAM >= 8GB (100 points)
   - Proportional scoring for less VRAM

3. Memory Score (max 100 points)
   - Total memory >= 16GB (100 points)
   - Proportional scoring for less memory

4. Disk Score (max 100 points)
   - System drive free space >= 100GB (100 points)
   - Proportional scoring for less space

### System Recommendations
- Total score >= 80: Excellent for AI model deployment
- Total score >= 60: Suitable for AI deployment with some limitations
- Total score < 60: Hardware upgrade recommended

### Notes
1. GPU detection requires NVIDIA graphics card with proper drivers
2. Some systems may require administrator privileges
3. Scoring criteria are based on common AI model requirements
4. Actual performance depends on specific model requirements

---

<a name="中文"></a>
## 中文

### 简介
AI System Check 是一个用于评估本地系统是否适合部署AI模型的工具。它可以帮助您评估系统的硬件配置，并给出针对性的建议。

### 功能特点
- 全面的硬件检测
  - CPU信息（型号、核心数、频率、使用率）
  - GPU信息（型号、显存、CUDA支持）
  - 内存信息（总量、可用量、使用率）
  - 磁盘信息（各分区空间使用情况）
- 智能评分系统
  - CPU评分（基于核心数和频率）
  - GPU评分（基于显存大小）
  - 内存评分（基于总容量）
  - 磁盘评分（基于可用空间）
- 生成详细报告
  - 保存为文本文件
  - 包含完整的系统信息
  - 提供AI部署建议

### 系统要求
- Python 3.8+
- Windows/Linux/MacOS

### 依赖包
```
psutil>=5.9.0
py-cpuinfo>=9.0.0
GPUtil>=1.4.0
torch>=2.0.0
```

### 安装步骤
1. 克隆或下载本项目
2. 安装依赖包：
```bash
# 使用pip安装
pip install -r requirements.txt

# 如果下载速度慢，可以使用清华镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 使用方法
运行主程序：
```bash
python system_check.py
```
程序会自动检测系统配置并生成报告。报告将同时显示在控制台中，并保存为`system_report.txt`文件。

### 评分标准
1. CPU评分（满分100分）
   - 物理核心数 >= 8核（50分）
   - 基础频率 >= 2GHz（50分）

2. GPU评分（满分100分）
   - 显存 >= 8GB（100分）
   - 显存不足则按比例得分

3. 内存评分（满分100分）
   - 总内存 >= 16GB（100分）
   - 不足则按比例得分

4. 磁盘评分（满分100分）
   - 系统盘可用空间 >= 100GB（100分）
   - 不足则按比例得分

### 系统建议
- 总分 >= 80分：系统非常适合部署AI模型
- 总分 >= 60分：系统基本满足AI部署需求，但某些大型模型可能会受限
- 总分 < 60分：系统可能不适合部署较大的AI模型，建议升级硬件配置

### 注意事项
1. GPU检测需要NVIDIA显卡并安装正确的驱动
2. 某些系统可能需要管理员权限才能获取完整信息
3. 评分标准是基于常见AI模型的最低要求设定的
4. 实际AI模型的运行效果还需要考虑具体模型的要求

## License
MIT License

## Contributing
Feel free to submit issues and pull requests.

## 作者
由[夜游猿]创建

## Acknowledgments
- psutil team
- py-cpuinfo team
- GPUtil team
- PyTorch team 