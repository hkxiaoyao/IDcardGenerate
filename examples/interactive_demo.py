#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
交互式功能演示

演示如何使用身份证数据生成器的交互式功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from src.utils import InteractiveConfig, logger

def demo_interactive_config():
    """演示交互式配置收集"""
    print("=" * 60)
    print("🎮 交互式配置演示")
    print("=" * 60)
    print("这是一个演示程序，展示如何使用交互式配置功能")
    print("在实际使用中，您只需要运行: python main.py interactive")
    print()
    
    # 创建交互式配置收集器
    interactive_config = InteractiveConfig()
    
    print("📝 模拟交互式配置收集过程...")
    
    # 这里我们设置一些演示用的配置，而不是真正的交互输入
    interactive_config.config = {
        'total_samples': 50,
        'output_dir': 'output/demo_data',
        'card_width': 526,
        'card_height': 340,
        'enable_augmentation': True,
        'aug_params': {
            'rotation_range': [-2, 2],
            'noise_level': [0.1, 0.2],
            'brightness': [0.9, 1.1]
        },
        'create_lmdb': True,
        'train_ratio': 0.8,
        'val_ratio': 0.2
    }
    
    # 显示收集到的配置
    print("\n✅ 配置收集完成！以下是演示配置:")
    show_demo_config(interactive_config.config)

def show_demo_config(config):
    """显示演示配置"""
    print("\n" + "="*50)
    print("📋 演示配置摘要")
    print("="*50)
    
    print(f"🔢 生成数量: {config.get('total_samples', 'N/A')}")
    print(f"📁 输出目录: {config.get('output_dir', 'N/A')}")
    print(f"📷 图像尺寸: {config.get('card_width', 'N/A')}x{config.get('card_height', 'N/A')}")
    
    if config.get('enable_augmentation'):
        print("🔄 数据增强: 启用")
        aug_params = config.get('aug_params', {})
        print(f"   - 旋转范围: {aug_params.get('rotation_range', 'N/A')}°")
        print(f"   - 噪声级别: {aug_params.get('noise_level', 'N/A')}")
        print(f"   - 亮度范围: {aug_params.get('brightness', 'N/A')}")
    else:
        print("🔄 数据增强: 禁用")
    
    if config.get('create_lmdb'):
        print(f"📦 LMDB数据集: 启用 (训练集比例: {config.get('train_ratio', 'N/A')})")
    else:
        print("📦 LMDB数据集: 禁用")
    
    print("="*50)

def demo_input_validation():
    """演示输入验证功能"""
    print("\n" + "="*60)
    print("🔍 输入验证演示")
    print("="*60)
    
    from src.utils import get_number, get_yes_no
    
    print("以下演示了各种输入验证功能:")
    print()
    
    # 演示数字输入验证
    print("1. 数字输入验证 (范围: 1-100)")
    print("   函数: get_number('请输入数字', default=10, min_val=1, max_val=100)")
    print("   - 输入超出范围会提示重新输入")
    print("   - 输入非数字会提示格式错误")
    print("   - 直接回车使用默认值")
    
    print("\n2. 是/否输入验证")
    print("   函数: get_yes_no('是否启用功能？', default=True)")
    print("   - 支持 y/n、是/否、1/0、true/false")
    print("   - 直接回车使用默认值")
    
    print("\n3. 目录路径验证")
    print("   函数: get_directory_path('请输入目录', create_if_not_exists=True)")
    print("   - 检查目录是否存在")
    print("   - 可选择自动创建不存在的目录")
    print("   - 验证路径是否为有效目录")

def demo_usage_scenarios():
    """演示使用场景"""
    print("\n" + "="*60)
    print("💡 使用场景演示")
    print("="*60)
    
    scenarios = [
        {
            "name": "快速测试场景",
            "description": "小量数据，快速验证功能",
            "config": {
                "samples": 10,
                "quality": "低质量",
                "augmentation": False,
                "lmdb": False
            }
        },
        {
            "name": "开发训练场景",
            "description": "中等数据量，包含数据增强",
            "config": {
                "samples": 1000,
                "quality": "中等质量",
                "augmentation": True,
                "lmdb": True
            }
        },
        {
            "name": "生产环境场景",
            "description": "大量高质量数据，完整流水线",
            "config": {
                "samples": 10000,
                "quality": "高质量",
                "augmentation": True,
                "lmdb": True
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   描述: {scenario['description']}")
        print("   配置:")
        config = scenario['config']
        print(f"   - 生成数量: {config['samples']}")
        print(f"   - 图像质量: {config['quality']}")
        print(f"   - 数据增强: {'启用' if config['augmentation'] else '禁用'}")
        print(f"   - LMDB数据集: {'启用' if config['lmdb'] else '禁用'}")

def main():
    """主函数"""
    print("🎯 身份证数据生成器 - 交互式功能演示")
    print()
    print("本演示程序展示了交互式功能的各个方面:")
    print("- 交互式配置收集")
    print("- 输入验证机制")
    print("- 常见使用场景")
    print()
    
    try:
        demo_interactive_config()
        demo_input_validation()
        demo_usage_scenarios()
        
        print("\n" + "="*60)
        print("✨ 演示完成！")
        print("="*60)
        print("要使用真正的交互式功能，请运行:")
        print("  python main.py interactive")
        print("或直接运行:")
        print("  python main.py")
        print("系统会自动启动交互式模式。")
        
    except Exception as e:
        logger.error(f"演示运行失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 