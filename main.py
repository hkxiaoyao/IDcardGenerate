#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
身份证数据生成器主程序

提供统一的命令行接口来执行：
- 数据生成
- 数据增强
- 数据集创建
- 完整流水线
"""

import argparse
import sys
import os
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils import logger, config, ensure_dir_exists, InteractiveConfig, get_yes_no
from src.core.dataGenerator import main as generate_data
from src.core.dataAugmentation import main as augment_data
from src.core.create_dataset import main as create_lmdb

def setup_directories():
    """创建必要的输出目录"""
    logger.info("创建输出目录...")
    
    # 创建基本输出目录
    ensure_dir_exists(config.get_output_dir())
    ensure_dir_exists(config.get_augmented_dir())
    ensure_dir_exists(config.get_lmdb_dir())
    
    # 创建子目录
    ensure_dir_exists(config.get_output_dir() / "images")
    ensure_dir_exists(config.get_output_dir() / "annotations")
    ensure_dir_exists(config.get_augmented_dir() / "images")
    ensure_dir_exists(Path("output/logs"))
    
    logger.info("目录创建完成")

def cmd_generate(args):
    """执行数据生成"""
    logger.info("开始生成身份证数据...")
    setup_directories()
    
    # 调用数据生成模块
    try:
        generate_data()
        logger.info("数据生成完成")
    except Exception as e:
        logger.error(f"数据生成失败: {e}")
        return False
    return True

def cmd_augment(args):
    """执行数据增强"""
    logger.info("开始数据增强...")
    setup_directories()
    
    try:
        augment_data()
        logger.info("数据增强完成")
    except Exception as e:
        logger.error(f"数据增强失败: {e}")
        return False
    return True

def cmd_create_dataset(args):
    """创建LMDB数据集"""
    logger.info("开始创建LMDB数据集...")
    setup_directories()
    
    try:
        create_lmdb()
        logger.info("LMDB数据集创建完成")
    except Exception as e:
        logger.error(f"LMDB数据集创建失败: {e}")
        return False
    return True

def cmd_pipeline(args):
    """执行完整流水线"""
    logger.info("开始执行完整数据处理流水线...")
    
    # 步骤1：生成数据
    if not cmd_generate(args):
        logger.error("流水线在数据生成步骤失败")
        return
    
    # 步骤2：数据增强
    if not cmd_augment(args):
        logger.error("流水线在数据增强步骤失败")
        return
    
    # 步骤3：创建数据集
    if not cmd_create_dataset(args):
        logger.error("流水线在数据集创建步骤失败")
        return
    
    logger.info("完整流水线执行成功！")

def cmd_interactive(args):
    """交互式模式"""
    print("\n🎉 欢迎使用身份证数据生成器！")
    print("接下来将通过交互式界面配置生成参数...")
    
    # 创建交互式配置收集器
    interactive_config = InteractiveConfig()
    
    # 收集配置
    if not interactive_config.collect_generation_config():
        logger.info("操作已取消")
        return
    
    if not interactive_config.collect_augmentation_config():
        logger.info("操作已取消")
        return
    
    if not interactive_config.collect_pipeline_config():
        logger.info("操作已取消")
        return
    
    # 显示配置摘要并确认
    if not interactive_config.show_summary():
        logger.info("操作已取消")
        return
    
    # 应用配置并执行
    apply_interactive_config(interactive_config.config)
    
    # 执行生成流程
    execute_interactive_pipeline(interactive_config.config)

def apply_interactive_config(user_config):
    """应用交互式配置"""
    # 动态更新配置
    if 'total_samples' in user_config:
        config._config.setdefault('dataset', {})['total_samples'] = user_config['total_samples']
    
    if 'output_dir' in user_config:
        config._config.setdefault('dataset', {})['output_dir'] = user_config['output_dir']
    
    if 'card_width' in user_config:
        config._config.setdefault('id_card', {}).setdefault('card_size', {})['width'] = user_config['card_width']
        config._config.setdefault('id_card', {}).setdefault('card_size', {})['height'] = user_config['card_height']
    
    if 'enable_augmentation' in user_config:
        config._config.setdefault('augmentation', {})['enabled'] = user_config['enable_augmentation']
    
    if 'aug_params' in user_config:
        config._config.setdefault('augmentation', {})['params'] = user_config['aug_params']
    
    if 'train_ratio' in user_config:
        config._config.setdefault('dataset', {})['train_ratio'] = user_config['train_ratio']
        config._config.setdefault('dataset', {})['val_ratio'] = user_config['val_ratio']

def execute_interactive_pipeline(user_config):
    """执行交互式流水线"""
    logger.info("🚀 开始执行数据生成流水线...")
    
    # 步骤1：生成数据
    print("\n" + "="*50)
    print("📝 步骤 1/3: 生成身份证数据")
    print("="*50)
    
    if not cmd_generate_with_config(user_config):
        logger.error("数据生成失败")
        return
    
    # 步骤2：数据增强（如果启用）
    if user_config.get('enable_augmentation', False):
        print("\n" + "="*50)
        print("🔄 步骤 2/3: 数据增强")
        print("="*50)
        
        if not cmd_augment_with_config(user_config):
            logger.error("数据增强失败")
            return
    else:
        print("\n⏭️ 跳过数据增强步骤")
    
    # 步骤3：创建LMDB数据集（如果启用）
    if user_config.get('create_lmdb', False):
        print("\n" + "="*50)
        print("📦 步骤 3/3: 创建LMDB数据集")
        print("="*50)
        
        if not cmd_create_dataset_with_config(user_config):
            logger.error("LMDB数据集创建失败")
            return
    else:
        print("\n⏭️ 跳过LMDB数据集创建步骤")
    
    print("\n🎉 所有步骤完成！")
    logger.info("交互式流水线执行成功！")
    
    # 显示输出位置
    output_dir = user_config.get('output_dir', config.get_output_dir())
    print(f"\n📁 生成的文件位置: {output_dir}")

def cmd_generate_with_config(user_config):
    """使用用户配置生成数据"""
    setup_directories()
    try:
        # 这里可以传递用户配置到生成函数
        generate_data()
        logger.info("数据生成完成")
        return True
    except Exception as e:
        logger.error(f"数据生成失败: {e}")
        return False

def cmd_augment_with_config(user_config):
    """使用用户配置进行数据增强"""
    try:
        augment_data()
        logger.info("数据增强完成")
        return True
    except Exception as e:
        logger.error(f"数据增强失败: {e}")
        return False

def cmd_create_dataset_with_config(user_config):
    """使用用户配置创建数据集"""
    try:
        create_lmdb()
        logger.info("LMDB数据集创建完成")
        return True
    except Exception as e:
        logger.error(f"LMDB数据集创建失败: {e}")
        return False

def cmd_info(args):
    """显示配置信息"""
    logger.info("=== 配置信息 ===")
    logger.info(f"项目根目录: {config.get('', {}).get('project_root', 'N/A')}")
    logger.info(f"输出目录: {config.get_output_dir()}")
    logger.info(f"增强数据目录: {config.get_augmented_dir()}")
    logger.info(f"LMDB目录: {config.get_lmdb_dir()}")
    logger.info(f"字体目录: {config.get_fonts_path()}")
    logger.info(f"总样本数: {config.get('dataset.total_samples', 10000)}")
    logger.info(f"训练集比例: {config.get('dataset.train_ratio', 0.8)}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="身份证数据生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py interactive  # 交互式模式（推荐）
  python main.py generate     # 生成身份证数据
  python main.py augment      # 数据增强
  python main.py dataset      # 创建LMDB数据集
  python main.py pipeline     # 执行完整流水线
  python main.py info         # 显示配置信息
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 交互式命令 (新增)
    parser_interactive = subparsers.add_parser('interactive', help='交互式配置和生成（推荐）')
    parser_interactive.set_defaults(func=cmd_interactive)
    
    # 生成数据命令
    parser_generate = subparsers.add_parser('generate', help='生成身份证数据')
    parser_generate.set_defaults(func=cmd_generate)
    
    # 数据增强命令
    parser_augment = subparsers.add_parser('augment', help='执行数据增强')
    parser_augment.set_defaults(func=cmd_augment)
    
    # 创建数据集命令
    parser_dataset = subparsers.add_parser('dataset', help='创建LMDB数据集')
    parser_dataset.set_defaults(func=cmd_create_dataset)
    
    # 完整流水线命令
    parser_pipeline = subparsers.add_parser('pipeline', help='执行完整流水线')
    parser_pipeline.set_defaults(func=cmd_pipeline)
    
    # 信息命令
    parser_info = subparsers.add_parser('info', help='显示配置信息')
    parser_info.set_defaults(func=cmd_info)
    
    # 解析参数
    args = parser.parse_args()
    
    # 如果没有指定命令，启动交互式模式
    if not args.command:
        print("🎉 欢迎使用身份证数据生成器！")
        print("未指定命令，将启动交互式模式...")
        print("您也可以使用 --help 查看所有可用命令")
        print()
        
        # 询问是否继续交互式模式
        if get_yes_no("是否继续使用交互式模式？", True):
            # 创建一个模拟的args对象
            from types import SimpleNamespace
            interactive_args = SimpleNamespace()
            cmd_interactive(interactive_args)
        else:
            parser.print_help()
        return
    
    # 执行对应命令
    try:
        args.func(args)
    except KeyboardInterrupt:
        logger.info("操作被用户中断")
    except Exception as e:
        logger.error(f"执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 