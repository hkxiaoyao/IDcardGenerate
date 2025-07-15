#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
交互式输入模块

提供用户友好的交互式参数收集功能
"""

import os
from pathlib import Path
from .logger import logger

def get_user_input(prompt, default=None, input_type=str, choices=None):
    """获取用户输入
    
    Args:
        prompt: 提示信息
        default: 默认值
        input_type: 输入类型 (str, int, float, bool)
        choices: 可选值列表
    
    Returns:
        用户输入的值
    """
    while True:
        try:
            # 构建提示信息
            full_prompt = prompt
            if default is not None:
                full_prompt += f" (默认: {default})"
            if choices:
                full_prompt += f" {choices}"
            full_prompt += ": "
            
            # 获取用户输入
            user_input = input(full_prompt).strip()
            
            # 如果用户直接回车且有默认值，使用默认值
            if not user_input and default is not None:
                return default
            
            # 如果没有输入且没有默认值，继续询问
            if not user_input:
                print("请输入有效值")
                continue
            
            # 处理布尔类型
            if input_type == bool:
                if user_input.lower() in ['y', 'yes', '是', '1', 'true']:
                    return True
                elif user_input.lower() in ['n', 'no', '否', '0', 'false']:
                    return False
                else:
                    print("请输入 y/n、是/否、1/0 或 true/false")
                    continue
            
            # 处理数字类型
            if input_type in [int, float]:
                value = input_type(user_input)
                return value
            
            # 处理选择类型
            if choices:
                if user_input in choices:
                    return user_input
                else:
                    print(f"请从以下选项中选择: {choices}")
                    continue
            
            # 默认返回字符串
            return user_input
            
        except ValueError as e:
            print(f"输入格式错误: {e}")
        except KeyboardInterrupt:
            print("\n操作已取消")
            return None

def get_yes_no(prompt, default=None):
    """获取是/否输入"""
    return get_user_input(prompt, default, bool)

def get_number(prompt, default=None, min_val=None, max_val=None, input_type=int):
    """获取数字输入并验证范围"""
    while True:
        value = get_user_input(prompt, default, input_type)
        if value is None:  # 用户取消
            return None
        
        # 验证范围
        if min_val is not None and value < min_val:
            print(f"值不能小于 {min_val}")
            continue
        if max_val is not None and value > max_val:
            print(f"值不能大于 {max_val}")
            continue
        
        return value

def get_directory_path(prompt, default=None, create_if_not_exists=True):
    """获取目录路径输入"""
    while True:
        path_str = get_user_input(prompt, default, str)
        if path_str is None:  # 用户取消
            return None
        
        path = Path(path_str)
        
        # 检查路径是否存在
        if not path.exists():
            if create_if_not_exists:
                create = get_yes_no(f"目录 '{path}' 不存在，是否创建？", True)
                if create:
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        logger.info(f"已创建目录: {path}")
                        return path
                    except Exception as e:
                        print(f"创建目录失败: {e}")
                        continue
                else:
                    continue
            else:
                print(f"目录 '{path}' 不存在")
                continue
        
        if not path.is_dir():
            print(f"'{path}' 不是一个目录")
            continue
        
        return path

class InteractiveConfig:
    """交互式配置收集器"""
    
    def __init__(self):
        self.config = {}
    
    def collect_generation_config(self):
        """收集数据生成配置"""
        print("\n" + "="*50)
        print("🎯 身份证数据生成配置")
        print("="*50)
        
        # 生成数量
        self.config['total_samples'] = get_number(
            "请输入要生成的身份证数量", 
            default=10, 
            min_val=1, 
            max_val=100000
        )
        
        if self.config['total_samples'] is None:
            return False
        
        # 是否使用自定义目录
        use_custom_dir = get_yes_no("是否自定义输出目录？", False)
        
        if use_custom_dir:
            custom_dir = get_directory_path("请输入输出目录路径", "output/custom_data")
            if custom_dir:
                self.config['output_dir'] = str(custom_dir)
        
        # 图像质量设置
        print("\n📷 图像质量设置:")
        quality_choices = ['高质量(1052x680)', '中等质量(526x340)', '低质量(263x170)']
        quality_map = {
            '高质量(1052x680)': (1052, 680),
            '中等质量(526x340)': (526, 340), 
            '低质量(263x170)': (263, 170)
        }
        
        for i, choice in enumerate(quality_choices, 1):
            print(f"  {i}. {choice}")
        
        quality_choice = get_user_input("请选择图像质量", "1", str, ['1', '2', '3'])
        if quality_choice:
            selected_quality = quality_choices[int(quality_choice) - 1]
            width, height = quality_map[selected_quality]
            self.config['card_width'] = width
            self.config['card_height'] = height
        
        return True
    
    def collect_augmentation_config(self):
        """收集数据增强配置"""
        print("\n" + "="*50)
        print("🔄 数据增强配置")
        print("="*50)
        
        # 是否启用数据增强
        enable_aug = get_yes_no("是否启用数据增强？", True)
        self.config['enable_augmentation'] = enable_aug
        
        if not enable_aug:
            return True
        
        print("\n📊 增强强度设置:")
        intensity_choices = ['轻微', '中等', '强烈', '自定义']
        for i, choice in enumerate(intensity_choices, 1):
            print(f"  {i}. {choice}")
        
        intensity = get_user_input("请选择增强强度", "2", str, ['1', '2', '3', '4'])
        
        if intensity == '1':  # 轻微
            self.config['aug_params'] = {
                'rotation_range': [-1, 1],
                'noise_level': [0.05, 0.1],
                'brightness': [0.95, 1.05]
            }
        elif intensity == '2':  # 中等
            self.config['aug_params'] = {
                'rotation_range': [-2, 2],
                'noise_level': [0.1, 0.2],
                'brightness': [0.9, 1.1]
            }
        elif intensity == '3':  # 强烈
            self.config['aug_params'] = {
                'rotation_range': [-5, 5],
                'noise_level': [0.2, 0.4],
                'brightness': [0.8, 1.2]
            }
        elif intensity == '4':  # 自定义
            print("\n⚙️ 自定义增强参数:")
            rotation = get_number("旋转角度范围 (度)", 2, 0, 10)
            noise = get_number("噪声强度 (0.0-1.0)", 0.2, 0.0, 1.0, float)
            brightness = get_number("亮度变化范围 (0.0-2.0)", 0.2, 0.0, 2.0, float)
            
            self.config['aug_params'] = {
                'rotation_range': [-rotation, rotation],
                'noise_level': [max(0, 0.1-noise/2), min(1, 0.1+noise/2)],
                'brightness': [max(0.1, 1-brightness), min(2, 1+brightness)]
            }
        
        return True
    
    def collect_pipeline_config(self):
        """收集完整流水线配置"""
        print("\n" + "="*50)
        print("🔧 流水线配置")
        print("="*50)
        
        # 是否创建LMDB数据集
        create_lmdb = get_yes_no("是否创建LMDB数据集？", True)
        self.config['create_lmdb'] = create_lmdb
        
        if create_lmdb:
            # 数据集分割比例
            train_ratio = get_number("训练集比例 (0.0-1.0)", 0.8, 0.1, 0.9, float)
            self.config['train_ratio'] = train_ratio
            self.config['val_ratio'] = 1.0 - train_ratio
        
        return True
    
    def show_summary(self):
        """显示配置摘要"""
        print("\n" + "="*50)
        print("📋 配置摘要")
        print("="*50)
        
        print(f"生成数量: {self.config.get('total_samples', 'N/A')}")
        
        if 'output_dir' in self.config:
            print(f"输出目录: {self.config['output_dir']}")
        
        if 'card_width' in self.config:
            print(f"图像尺寸: {self.config['card_width']}x{self.config['card_height']}")
        
        print(f"数据增强: {'启用' if self.config.get('enable_augmentation') else '禁用'}")
        
        if self.config.get('create_lmdb'):
            print(f"LMDB数据集: 启用 (训练集比例: {self.config.get('train_ratio', 0.8)})")
        
        print("="*50)
        
        # 确认配置
        confirm = get_yes_no("\n确认以上配置并开始生成？", True)
        return confirm 