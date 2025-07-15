"""
数据模块

包含字典数据和地址数据。
"""

from .dictionary import alphabet, nations, common_surnames, common_name_chars
from .address_set import province_set, city_set, couty_set

__all__ = ["alphabet", "nations", "common_surnames", "common_name_chars", 
           "province_set", "city_set", "couty_set"] 