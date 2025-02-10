import os
import sys
import psutil
from cpuinfo import get_cpu_info
import GPUtil
import torch
import platform
from datetime import datetime

class SystemCheck:
    def __init__(self):
        self.report = []
        self.score = {
            'cpu': 0,
            'gpu': 0,
            'memory': 0,
            'disk': 0
        }

    def add_to_report(self, section, content):
        self.report.append(f"\n{section}")
        self.report.append("-" * len(section))
        self.report.append(content)

    def check_cpu(self):
        cpu_info = get_cpu_info()
        cpu_count = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1)

        content = f"""
处理器: {cpu_info.get('brand_raw', 'Unknown')}
物理核心数: {cpu_count}
逻辑核心数: {cpu_threads}
基础频率: {cpu_freq.current:.2f} MHz
CPU使用率: {cpu_percent}%
"""
        self.add_to_report("CPU信息", content)
        
        # 评分标准：核心数>=8, 频率>=2GHz
        self.score['cpu'] = min(100, 
            (cpu_count/8) * 50 + 
            (cpu_freq.current/2000) * 50)

    def check_gpu(self):
        content = "未检测到GPU"
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_info = []
                for gpu in gpus:
                    gpu_info.append(f"""
显卡型号: {gpu.name}
显存总量: {gpu.memoryTotal} MB
显存使用: {gpu.memoryUsed} MB
显存空闲: {gpu.memoryFree} MB
GPU使用率: {gpu.load*100:.2f}%
""")
                content = "\n".join(gpu_info)
                
                # 评分标准：显存>=8GB
                self.score['gpu'] = min(100, 
                    (gpus[0].memoryTotal/8000) * 100)
            
            content += f"\nCUDA是否可用: {torch.cuda.is_available()}"
            if torch.cuda.is_available():
                content += f"\nCUDA版本: {torch.version.cuda}"
        except Exception as e:
            content += f"\n检测GPU时发生错误: {str(e)}"
            
        self.add_to_report("GPU信息", content)

    def check_memory(self):
        memory = psutil.virtual_memory()
        content = f"""
内存总量: {memory.total/1024/1024/1024:.2f} GB
已使用: {memory.used/1024/1024/1024:.2f} GB
可用: {memory.available/1024/1024/1024:.2f} GB
使用率: {memory.percent}%
"""
        self.add_to_report("内存信息", content)
        
        # 评分标准：总内存>=16GB
        self.score['memory'] = min(100, 
            (memory.total/1024/1024/1024/16) * 100)

    def check_disk(self):
        disk_info = []
        try:
            for partition in psutil.disk_partitions():
                if os.name == 'nt':
                    if 'cdrom' in partition.opts or partition.fstype == '':
                        continue
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append(f"""
分区: {partition.mountpoint}
文件系统: {partition.fstype}
总空间: {usage.total/1024/1024/1024:.2f} GB
已使用: {usage.used/1024/1024/1024:.2f} GB
可用: {usage.free/1024/1024/1024:.2f} GB
使用率: {usage.percent}%
""")
                except Exception:
                    continue
                
            self.add_to_report("磁盘信息", "\n".join(disk_info))
            
            # 评分标准：系统盘可用空间>=100GB
            system_partition = psutil.disk_usage(os.path.abspath(os.path.sep))
            self.score['disk'] = min(100, 
                (system_partition.free/1024/1024/1024/100) * 100)
        except Exception as e:
            self.add_to_report("磁盘信息", f"检测磁盘时发生错误: {str(e)}")
            self.score['disk'] = 0

    def generate_summary(self):
        total_score = sum(self.score.values()) / len(self.score)
        summary = f"""
系统总评分: {total_score:.2f}/100
- CPU评分: {self.score['cpu']:.2f}/100
- GPU评分: {self.score['gpu']:.2f}/100
- 内存评分: {self.score['memory']:.2f}/100
- 磁盘评分: {self.score['disk']:.2f}/100

AI部署建议:
"""
        if total_score >= 80:
            summary += "✅ 您的系统非常适合部署AI模型"
        elif total_score >= 60:
            summary += "🟡 您的系统基本满足AI部署需求，但某些大型模型可能会受限"
        else:
            summary += "❌ 您的系统可能不适合部署较大的AI模型，建议升级硬件配置"

        self.add_to_report("系统评估总结", summary)

    def run_check(self):
        self.add_to_report("基本信息", f"""
检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
操作系统: {platform.system()} {platform.version()}
Python版本: {sys.version.split()[0]}
""")
        
        self.check_cpu()
        self.check_gpu()
        self.check_memory()
        self.check_disk()
        self.generate_summary()
        
        return "\n".join(self.report)

def main():
    checker = SystemCheck()
    report = checker.run_check()
    
    # 保存报告到文件
    with open("system_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print("\n报告已保存到 system_report.txt")

if __name__ == "__main__":
    main() 