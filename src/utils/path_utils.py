import os
from pathlib import Path

def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.parent.parent

def get_resources_path():
    """获取资源文件目录"""
    return get_project_root() / "resources"

def get_fonts_path():
    """获取字体文件目录"""
    return get_resources_path() / "fonts_and_images"

def get_mapdata_path():
    """获取地图数据目录"""
    return get_resources_path() / "mapdata"

def get_output_path():
    """获取输出目录"""
    return get_project_root() / "output"

def ensure_dir_exists(path):
    """确保目录存在，如果不存在则创建"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_config_path():
    """获取配置文件目录"""
    return get_project_root() / "config" 