"""
CheckPaper 提示词模板管理器
实现提示词与代码分离
"""
import os
from typing import Any, Dict, Optional

from jinja2 import BaseLoader, Environment, FileSystemLoader


class PromptManager:
    """提示词管理器"""

    def __init__(self, template_dir: str | None = None):
        """
        初始化提示词管理器

        Args:
            template_dir: 模板目录路径
        """
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), "templates")

        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir) if os.path.exists(template_dir) else BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # 内置提示词
        self._builtin_prompts = self._load_builtin_prompts()

    def _load_builtin_prompts(self) -> dict[str, str]:
        """加载内置提示词"""
        return {
            "format_check": """你是一个专业的学术论文格式检查专家。请检查以下论文内容的格式规范性：

1. 标题层级是否清晰、编号是否正确
2. 字体、字号是否一致
3. 段落格式是否规范
4. 图表编号是否连续
5. 页眉页脚是否符合要求
6. 目录与正文是否对应

请以JSON格式返回检查结果，包含以下字段：
- issues: 问题列表，每个问题包含 severity, category, title, description, suggestion
- summary: 总结

论文内容：
{{ content }}""",

            "figure_table_check": """你是一个学术论文图表引用检查专家。请检查以下论文中的图片和表格引用：

1. 所有图片/表格是否在正文中被显式引用
2. 引用编号是否与实际定义匹配
3. 是否存在"孤儿引用"（引用了不存在的图/表）
4. 是否存在"未引用"的图/表（定义了但正文未提及）

请以JSON格式返回检查结果。

论文内容：
{{ content }}

图片列表：
{{ figures }}

表格列表：
{{ tables }}""",

            "citation_check": """你是一个学术论文引用检查专家。请检查以下论文中的参考文献引用：

1. 正文中的引用标记与参考文献列表是否匹配
2. 是否有重复引用
3. 是否有缺失的引用
4. 引用格式是否规范

请以JSON格式返回检查结果。

论文内容：
{{ content }}

参考文献列表：
{{ references }}

正文引用：
{{ citations }}""",

            "reference_verify": """你是一个学术文献验证专家。请验证以下参考文献的真实性：

对于每条参考文献，请检查：
1. DOI是否存在且有效
2. 标题、作者、期刊信息是否匹配
3. 发表年份是否合理
4. 是否是已知的虚假期刊或掠夺性期刊

请以JSON格式返回验证结果，每条文献包含：
- verified: 是否验证通过
- confidence: 置信度 (0-1)
- issues: 发现的问题

参考文献列表：
{{ references }}""",

            "data_source_verify": """你是一个学术数据验证专家。请验证以下论文中的数据来源：

1. 数据来源是否明确标注
2. 数据集URL是否可访问
3. 数据描述是否与实际内容匹配
4. 是否存在数据造假嫌疑

请以JSON格式返回验证结果。

论文内容：
{{ content }}

数据引用：
{{ data_references }}""",

            "data_processing_verify": """你是一个学术数据处理验证专家。请验证以下论文中的数据处理方法：

1. 统计方法是否正确
2. 样本量是否充足
3. p值、置信区间是否合理
4. 图表数据与正文报告是否一致
5. 是否存在GRIM/SPRITE测试失败

请以JSON格式返回验证结果。

论文内容：
{{ content }}

统计数据：
{{ statistics }}""",

            "report_generation": """你是一个学术论文报告生成专家。请根据以下验证结果生成一份详细的论文验证报告：

报告应包含：
1. 验证总结
2. 各项检查的详细结果
3. 发现的问题及严重程度
4. 改进建议
5. 总体评分

验证结果：
{{ validation_results }}

请以Markdown格式生成报告。"""
        }

    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        获取渲染后的提示词

        Args:
            prompt_name: 提示词名称
            **kwargs: 模板变量

        Returns:
            渲染后的提示词
        """
        # 首先尝试从文件加载
        try:
            template = self.env.get_template(f"{prompt_name}.txt")
            return template.render(**kwargs)
        except Exception:
            pass

        # 然后尝试从文件加载 jinja2 模板
        try:
            template = self.env.get_template(f"{prompt_name}.j2")
            return template.render(**kwargs)
        except Exception:
            pass

        # 最后使用内置提示词
        if prompt_name in self._builtin_prompts:
            from jinja2 import Template
            template = Template(self._builtin_prompts[prompt_name])
            return template.render(**kwargs)

        raise ValueError(f"未找到提示词: {prompt_name}")

    def list_prompts(self) -> list:
        """列出所有可用的提示词"""
        prompts = list(self._builtin_prompts.keys())

        # 添加文件中的提示词
        if os.path.exists(self.template_dir):
            for filename in os.listdir(self.template_dir):
                if filename.endswith(('.txt', '.j2')):
                    name = filename.rsplit('.', 1)[0]
                    if name not in prompts:
                        prompts.append(name)

        return prompts


# 全局提示词管理器实例
prompt_manager = PromptManager()


def get_prompt_manager() -> PromptManager:
    """获取提示词管理器实例"""
    return prompt_manager
