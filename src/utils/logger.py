import logging
import os
from pathlib import Path
from .config_manager import config
from .path_utils import ensure_dir_exists, get_project_root

class Logger:
    """日志管理器"""
    
    def __init__(self, name="IDCardGenerator"):
        """初始化日志器
        
        Args:
            name: 日志器名称
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志器配置"""
        # 获取日志配置
        log_level = config.get('logging.level', 'INFO')
        log_format = config.get('logging.format', 
                               '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = config.get('logging.file', 'output/logs/id_card_generator.log')
        
        # 设置日志级别
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # 避免重复添加处理器
        if self.logger.handlers:
            return
        
        # 创建格式器
        formatter = logging.Formatter(log_format)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 创建文件处理器
        log_file_path = get_project_root() / log_file
        ensure_dir_exists(log_file_path.parent)
        
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)
    
    def info(self, message):
        """记录一般信息"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录错误信息"""
        self.logger.error(message)
    
    def critical(self, message):
        """记录严重错误信息"""
        self.logger.critical(message)
    
    def log_progress(self, current, total, operation="处理"):
        """记录进度信息"""
        percentage = (current / total) * 100
        self.info(f"{operation}进度: {current}/{total} ({percentage:.1f}%)")

# 创建全局日志器实例
logger = Logger() 