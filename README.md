# 身份证数据生成器

一个专业的身份证OCR训练数据生成工具，支持批量生成真实的中国身份证图像数据，用于OCR模型训练和测试。

## ✨ 功能特性

- 🎯 **真实数据生成**：生成符合真实规律的身份证信息（姓名、身份证号、地址等）
- 🎨 **高质量图像**：生成高分辨率的身份证正面图像
- 🔄 **数据增强**：支持多种数据增强技术（旋转、噪声、模糊、亮度调整等）
- 📊 **多种格式**：支持输出标注文件和LMDB数据集格式
- ⚙️ **模块化设计**：清晰的模块化架构，易于扩展和维护
- 📝 **配置化管理**：YAML配置文件，灵活调整参数
- 📋 **日志系统**：完整的日志记录和进度追踪
- 🖥️ **命令行工具**：统一的CLI接口，支持完整流水线

## 🏗️ 项目架构

```
IDcardGenerate/
├── src/                          # 源代码目录
│   ├── core/                     # 核心功能模块
│   │   ├── dataGenerator.py      # 数据生成器
│   │   ├── dataAugmentation.py   # 数据增强
│   │   └── create_dataset.py     # 数据集创建
│   ├── data/                     # 数据模块
│   │   ├── dictionary.py         # 字典数据
│   │   ├── address_set.py        # 地址数据
│   │   └── dataAugmentateion_LookUpTable.py
│   └── utils/                    # 工具模块
│       ├── config_manager.py     # 配置管理
│       ├── logger.py            # 日志系统
│       └── path_utils.py        # 路径工具
├── config/                       # 配置文件
│   └── default.yaml             # 默认配置
├── resources/                    # 资源文件
│   ├── fonts_and_images/        # 字体和图像
│   └── mapdata/                 # 地图数据
├── output/                      # 输出目录
│   ├── data/                    # 生成的原始数据
│   ├── augmented_data/          # 增强后的数据
│   ├── lmdb/                    # LMDB数据集
│   └── logs/                    # 日志文件
├── examples/                    # 使用示例
├── main.py                      # 主程序入口
└── README.md                    # 项目文档
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 系统支持：Windows / Linux / macOS

### 安装依赖

```bash
# 克隆项目
git clone <your-repo-url>
cd IDcardGenerate

# 安装依赖包
pip install -r requirements.txt
```

### 立即开始

```bash
# 🚀 一键启动交互式模式
python main.py

# 系统将引导您：
# 1. 设置生成数量（默认10张）
# 2. 选择图像质量
# 3. 配置数据增强
# 4. 设置输出目录
# 5. 自动执行完整流水线
```

### 基本使用

#### 🎯 交互式模式（推荐）
```bash
# 启动交互式配置界面
python main.py interactive

# 或者直接运行（会自动进入交互式模式）
python main.py
```

交互式模式特点：
- 🎮 **用户友好**：图形化界面引导，无需记忆命令参数
- ⚙️ **灵活配置**：实时配置生成数量、图像质量、增强参数等
- 🔍 **输入验证**：自动验证输入范围和格式
- 📋 **配置预览**：执行前显示完整配置摘要
- 🛡️ **错误处理**：友好的错误提示和重试机制

#### 传统命令行模式

#### 1. 查看配置信息
```bash
python main.py info
```

#### 2. 生成身份证数据
```bash
python main.py generate
```

#### 3. 数据增强
```bash
python main.py augment
```

#### 4. 创建LMDB数据集
```bash
python main.py dataset
```

#### 5. 执行完整流水线
```bash
python main.py pipeline
```

## ⚙️ 配置说明

配置文件位于 `config/default.yaml`，主要配置项：

### 数据集配置
```yaml
dataset:
  output_dir: "output/data"        # 输出目录
  total_samples: 10000             # 生成样本总数
  train_ratio: 0.8                 # 训练集比例
```

### 身份证配置
```yaml
id_card:
  year_range:                      # 出生年份范围
    min: 1950
    max: 2010
  card_size:                       # 身份证尺寸
    width: 1052
    height: 680
```

### 数据增强配置
```yaml
augmentation:
  enabled: true
  params:
    rotation_range: [-2, 2]        # 旋转角度范围
    noise_level: [0.1, 0.3]        # 噪声级别
    brightness: [0.8, 1.2]         # 亮度范围
```

## 📁 输出格式

### 原始数据
```
output/data/
├── images/           # 身份证图像
│   ├── 001.jpg
│   ├── 002.jpg
│   └── ...
└── annotations/      # 标注文件
    └── data.txt     # 图像路径和对应文本
```

### 标注格式
```
images/001.jpg    张三,110101199001011234,北京市东城区,汉,1990,01,01,男
images/002.jpg    李四,120102199202022345,天津市河东区,汉,1992,02,02,女
```

### LMDB数据集
生成的LMDB数据集可直接用于PaddleOCR、TrOCR等OCR框架训练。

## 🔧 高级用法

### 交互式编程接口
```python
from src.utils import InteractiveConfig, logger

# 创建交互式配置收集器
interactive_config = InteractiveConfig()

# 收集用户配置
if interactive_config.collect_generation_config():
    if interactive_config.collect_augmentation_config():
        # 显示配置摘要
        if interactive_config.show_summary():
            logger.info("用户确认配置，开始生成...")
            # 使用收集到的配置
            user_config = interactive_config.config
```

### 自定义配置
```python
from src.utils import ConfigManager

# 使用自定义配置文件
config = ConfigManager("my_config.yaml")
```

### 编程接口
```python
from src.core.dataGenerator import IDCardGenerator
from src.utils import logger, config

# 创建生成器
generator = IDCardGenerator(config)

# 生成单张身份证
card_info = generator.generate_single_card()
logger.info(f"生成身份证: {card_info}")
```

### 输入验证工具
```python
from src.utils import get_number, get_yes_no, get_directory_path

# 获取数字输入（带范围验证）
count = get_number("生成数量", default=10, min_val=1, max_val=1000)

# 获取是/否输入
enable_aug = get_yes_no("是否启用数据增强？", default=True)

# 获取目录路径（自动创建）
output_dir = get_directory_path("输出目录", "output/data")
```

## 🎯 数据质量

### 生成的数据特点
- **真实性**：姓名使用常见姓氏和名字组合
- **合法性**：身份证号码符合校验规则
- **地理准确性**：地址信息基于真实行政区划
- **时间合理性**：出生日期在合理范围内
- **多样性**：支持各省市地区、多种民族

### 质量保证
- 身份证号码通过校验位算法验证
- 地址数据基于国家标准行政区划
- 日期信息考虑月份天数限制
- 字体和布局符合真实身份证规范

## 🛠️ 开发指南

### 项目结构说明
- `src/core/`：核心算法实现
- `src/data/`：数据定义和管理
- `src/utils/`：通用工具函数
- `config/`：配置文件管理
- `resources/`：字体、图像等资源

### 扩展功能
1. 添加新的数据增强算法到 `src/core/dataAugmentation.py`
2. 修改身份证模板到 `resources/fonts_and_images/`
3. 调整配置参数到 `config/default.yaml`

## 🐛 常见问题

### Q: 生成的图像质量不理想？
A: 检查字体文件是否完整，调整 `config/default.yaml` 中的字体大小配置。

### Q: 生成速度慢？
A: 可以减少 `dataset.total_samples` 或调整 `dataset.batch_size`。

### Q: 地址信息不准确？
A: 更新 `resources/mapdata/` 中的地理数据文件。

### Q: 依赖包安装失败？
A: 建议使用虚拟环境，确保Python版本兼容。

## 📊 性能指标

- **生成速度**：约100-200张/分钟（取决于硬件配置）
- **图像质量**：1052×680高分辨率
- **数据准确性**：99%+的身份证号码格式正确率
- **地址覆盖**：支持全国31个省市自治区

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

本工具仅用于学术研究和技术测试，生成的身份证数据均为虚构，请勿用于任何非法用途。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/your-repo/issues)
- 发送邮件至：your-email@example.com

---

⭐ 如果这个项目对您有帮助，请给个星标支持！

