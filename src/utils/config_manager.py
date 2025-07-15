import yaml
import os
from pathlib import Path
from .path_utils import get_config_path, get_project_root

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file="default.yaml"):
        """初始化配置管理器
        
        Args:
            config_file: 配置文件名，默认为default.yaml
        """
        self.config_file = config_file
        self.config_path = get_config_path() / config_file
        self._config = None
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            print(f"配置文件加载成功: {self.config_path}")
        except FileNotFoundError:
            print(f"配置文件未找到: {self.config_path}")
            self._config = {}
        except yaml.YAMLError as e:
            print(f"配置文件格式错误: {e}")
            self._config = {}
    
    def get(self, key_path, default=None):
        """获取配置值
        
        Args:
            key_path: 配置键路径，使用点号分隔，如 'dataset.output_dir'
            default: 默认值
        
        Returns:
            配置值或默认值
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_output_dir(self):
        """获取输出目录路径"""
        output_dir = self.get('dataset.output_dir', 'output/data')
        return get_project_root() / output_dir
    
    def get_augmented_dir(self):
        """获取数据增强输出目录路径"""
        augmented_dir = self.get('dataset.augmented_dir', 'output/augmented_data')
        return get_project_root() / augmented_dir
    
    def get_lmdb_dir(self):
        """获取LMDB数据库目录路径"""
        lmdb_dir = self.get('dataset.lmdb_dir', 'output/lmdb')
        return get_project_root() / lmdb_dir
    
    def get_fonts_path(self):
        """获取字体文件目录路径"""
        fonts_dir = self.get('resources.fonts_dir', 'resources/fonts_and_images')
        return get_project_root() / fonts_dir
    
    def get_font_path(self, font_name):
        """获取特定字体文件路径"""
        return self.get_fonts_path() / font_name
    
    def get_background_image_path(self, image_name):
        """获取背景图片路径"""
        images_dir = self.get('resources.images_dir', 'resources/fonts_and_images')
        return get_project_root() / images_dir / image_name
    
    def get_id_card_config(self):
        """获取身份证配置"""
        return self.get('id_card', {})
    
    def get_augmentation_config(self):
        """获取数据增强配置"""
        return self.get('augmentation', {})

# 创建全局配置实例
config = ConfigManager() 