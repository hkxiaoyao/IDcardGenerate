#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基础使用示例

演示如何使用身份证数据生成器的基本功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from src.utils import logger, config, ensure_dir_exists

def example_basic_generation():
    """基础数据生成示例"""
    logger.info("=== 基础数据生成示例 ===")
    
    # 确保输出目录存在
    output_dir = config.get_output_dir()
    ensure_dir_exists(output_dir / "images")
    ensure_dir_exists(output_dir / "annotations")
    
    logger.info(f"输出目录: {output_dir}")
    logger.info(f"将生成 {config.get('dataset.total_samples', 100)} 个样本")
    
    # 这里可以调用生成函数
    # from src.core.dataGenerator import main as generate_data
    # generate_data()
    
    logger.info("生成完成（示例模式，未实际生成）")

def example_config_usage():
    """配置使用示例"""
    logger.info("=== 配置使用示例 ===")
    
    # 显示配置信息
    logger.info(f"项目根目录: {config.get_project_root()}")
    logger.info(f"输出目录: {config.get_output_dir()}")
    logger.info(f"字体目录: {config.get_fonts_path()}")
    
    # 获取身份证配置
    id_config = config.get_id_card_config()
    logger.info(f"身份证尺寸: {id_config.get('card_size', {})}")
    logger.info(f"年份范围: {id_config.get('year_range', {})}")
    
    # 获取数据增强配置
    aug_config = config.get_augmentation_config()
    logger.info(f"数据增强启用: {aug_config.get('enabled', False)}")

def example_custom_paths():
    """自定义路径示例"""
    logger.info("=== 自定义路径示例 ===")
    
    # 获取资源文件路径
    font_path = config.get_font_path("hei.ttf")
    bg_path = config.get_background_image_path("fore.png")
    
    logger.info(f"字体文件路径: {font_path}")
    logger.info(f"背景图片路径: {bg_path}")
    
    # 检查文件是否存在
    if font_path.exists():
        logger.info("✓ 字体文件存在")
    else:
        logger.warning("✗ 字体文件不存在")
    
    if bg_path.exists():
        logger.info("✓ 背景图片存在")
    else:
        logger.warning("✗ 背景图片不存在")

def main():
    """主函数"""
    logger.info("开始运行身份证数据生成器使用示例")
    
    try:
        example_basic_generation()
        print()
        example_config_usage()
        print()
        example_custom_paths()
        
    except Exception as e:
        logger.error(f"示例运行失败: {e}")
        return 1
    
    logger.info("示例运行完成")
    return 0

if __name__ == "__main__":
    exit(main()) 