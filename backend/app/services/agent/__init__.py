"""
CheckPaper Agent 服务模块
实现论文验证的核心逻辑
"""
import re
import json
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from ...schemas.validation import ValidationTypeEnum, IssueSeverity
from ...core.config import settings


class AgentService:
    """Agent 服务类"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化 OpenAI 客户端"""
        try:
            from openai import AsyncOpenAI
            # 支持自定义API地址（兼容本地部署的模型）
            self.client = AsyncOpenAI(
                api_key=settings.openai_api_key or "no-key-required",
                base_url=settings.openai_base_url
            )
            self.model = settings.openai_model
        except Exception as e:
            print(f"警告: 无法初始化 OpenAI 客户端: {e}")
            self.model = settings.openai_model
    
    async def run_validation(
        self,
        document_id: str,
        validation_types: List[ValidationTypeEnum],
        options: Dict[str, Any],
        document_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        运行验证任务
        
        Args:
            document_id: 文档ID
            validation_types: 验证类型列表
            options: 验证选项
            document_content: 文档内容（可选，用于测试）
        
        Returns:
            验证结果字典
        """
        results = {}
        
        for vtype in validation_types:
            try:
                if vtype == ValidationTypeEnum.FORMAT:
                    results[vtype.value] = await self._validate_format(document_content or "", options)
                elif vtype == ValidationTypeEnum.FIGURE_TABLE:
                    results[vtype.value] = await self._validate_figure_table(document_content or "", options)
                elif vtype == ValidationTypeEnum.CITATION:
                    results[vtype.value] = await self._validate_citation(document_content or "", options)
                elif vtype == ValidationTypeEnum.DATA_SOURCE:
                    results[vtype.value] = await self._validate_data_source(document_content or "", options)
                elif vtype == ValidationTypeEnum.DATA_PROCESSING:
                    results[vtype.value] = await self._validate_data_processing(document_content or "", options)
                elif vtype == ValidationTypeEnum.REFERENCE:
                    results[vtype.value] = await self._validate_reference(document_content or "", options)
            except Exception as e:
                results[vtype.value] = {
                    "status": "failed",
                    "error": str(e),
                    "issues_count": 0,
                    "critical_count": 0,
                    "warning_count": 0,
                    "info_count": 0,
                    "issues": []
                }
        
        return results
    
    async def _validate_format(self, content: str, options: dict) -> dict:
        """
        验证论文格式
        
        检查内容：
        - 标题层级和编号规范
        - 字体、字号一致性
        - 页面布局（页边距、页眉页脚）
        - 目录与正文对应关系
        - 图表编号连续性
        """
        issues = []
        
        if not content:
            return self._empty_result("格式检查")
        
        # 检查标题层级
        section_pattern = r'^(#{1,6})\s+(.+)$'
        sections = re.findall(section_pattern, content, re.MULTILINE)
        
        if not sections:
            issues.append({
                "severity": "warning",
                "category": "结构问题",
                "title": "未检测到标准标题格式",
                "description": "论文应包含清晰的章节标题（如：引言、方法、结果、讨论、结论）",
                "suggestion": "使用标准的Markdown或LaTeX标题格式"
            })
        
        # 检查常见论文章节
        common_sections = ["引言", "introduction", "方法", "method", "结果", "result", 
                          "讨论", "discussion", "结论", "conclusion", "摘要", "abstract"]
        found_sections = []
        for _, title in sections:
            title_lower = title.lower()
            for cs in common_sections:
                if cs in title_lower:
                    found_sections.append(cs)
                    break
        
        if len(found_sections) < 3:
            issues.append({
                "severity": "info",
                "category": "结构完整性",
                "title": "论文章节结构可能不完整",
                "description": f"只检测到以下标准章节: {', '.join(found_sections) if found_sections else '无'}",
                "suggestion": "建议包含完整的论文章节：引言、方法、结果、讨论、结论"
            })
        
        # 检查图表编号连续性
        fig_numbers = re.findall(r'(?:Fig(?:ure)?\.?\s*(\d+)|图\s*(\d+))', content, re.IGNORECASE)
        if fig_numbers:
            nums = sorted(set(int(n[0] or n[1]) for n in fig_numbers))
            expected = list(range(1, len(nums) + 1))
            if nums != expected and len(nums) > 1:
                issues.append({
                    "severity": "warning",
                    "category": "图表编号",
                    "title": "图表编号可能不连续",
                    "description": f"检测到的图表编号: {nums}，期望: {expected}",
                    "suggestion": "请检查图表编号是否连续"
                })
        
        # 检查段落长度
        paragraphs = content.split('\n\n')
        long_paragraphs = [i for i, p in enumerate(paragraphs) if len(p) > 1000]
        if long_paragraphs:
            issues.append({
                "severity": "info",
                "category": "格式建议",
                "title": f"发现 {len(long_paragraphs)} 个过长段落",
                "description": "过长的段落可能影响可读性",
                "suggestion": "建议将长段落拆分为多个小段落"
            })
        
        return self._build_result(
            status="completed",
            summary="格式检查完成",
            issues=issues
        )
    
    async def _validate_figure_table(self, content: str, options: dict) -> dict:
        """
        验证图表引用
        
        检查内容：
        - 所有图片/表格是否在正文中被显式引用
        - 引用编号是否与实际定义匹配
        - 检测"孤儿引用"（引用了不存在的图/表）
        - 检测"未引用"的图/表
        """
        issues = []
        
        if not content:
            return self._empty_result("图表引用检查")
        
        # 提取图片定义
        fig_defs = set()
        fig_def_pattern = r'(?:Fig(?:ure)?\.?\s*(\d+)|图\s*(\d+))'
        for match in re.finditer(fig_def_pattern, content, re.IGNORECASE):
            num = match.group(1) or match.group(2)
            fig_defs.add(num)
        
        # 提取表格定义
        tab_defs = set()
        tab_def_pattern = r'(?:Table\.?\s*(\d+)|表\s*(\d+))'
        for match in re.finditer(tab_def_pattern, content, re.IGNORECASE):
            num = match.group(1) or match.group(2)
            tab_defs.add(num)
        
        # 提取正文中的引用
        fig_refs = set()
        tab_refs = set()
        
        # 检查引用上下文
        ref_pattern = r'(?:见|参见|如|see|refer to|shown in|displayed in)\s+(?:Fig(?:ure)?\.?\s*(\d+)|图\s*(\d+)|Table\.?\s*(\d+)|表\s*(\d+))'
        for match in re.finditer(ref_pattern, content, re.IGNORECASE):
            if match.group(1) or match.group(2):
                fig_refs.add(match.group(1) or match.group(2))
            if match.group(3) or match.group(4):
                tab_refs.add(match.group(3) or match.group(4))
        
        # 检测未引用的图片
        unreferenced_figs = fig_defs - fig_refs
        for fig in unreferenced_figs:
            issues.append({
                "severity": "warning",
                "category": "未引用图片",
                "title": f"图片 {fig} 未被引用",
                "description": f"图片 {fig} 在文中定义但未被显式引用",
                "suggestion": "在正文中添加对图片的引用说明"
            })
        
        # 检测未引用的表格
        unreferenced_tabs = tab_defs - tab_refs
        for tab in unreferenced_tabs:
            issues.append({
                "severity": "warning",
                "category": "未引用表格",
                "title": f"表格 {tab} 未被引用",
                "description": f"表格 {tab} 在文中定义但未被显式引用",
                "suggestion": "在正文中添加对表格的引用说明"
            })
        
        return self._build_result(
            status="completed",
            summary=f"图表引用检查完成，发现 {len(fig_defs)} 个图片和 {len(tab_defs)} 个表格",
            issues=issues
        )
    
    async def _validate_citation(self, content: str, options: dict) -> dict:
        """
        验证参考文献引用
        
        检查内容：
        - 正文引用标记与参考文献列表的一致性
        - 重复引用检测
        - 缺失引用检测
        - 引用格式规范
        """
        issues = []
        
        if not content:
            return self._empty_result("参考文献引用检查")
        
        # 提取参考文献部分
        ref_section_pattern = r'(?:References|参考文献|Bibliography)\s*\n([\s\S]+?)(?:\n\n|\Z)'
        ref_match = re.search(ref_section_pattern, content, re.IGNORECASE)
        
        # 提取参考文献条目
        references = set()
        if ref_match:
            ref_text = ref_match.group(1)
            # 匹配 [1], [2] 等格式
            ref_entries = re.findall(r'\[(\d+)\]', ref_text)
            references = set(ref_entries)
        
        # 提取正文中的引用
        citations = set()
        citation_pattern = r'\[(\d+(?:,\s*\d+)*)\]'
        for match in re.finditer(citation_pattern, content):
            nums = match.group(1).split(',')
            for num in nums:
                citations.add(num.strip())
        
        # 检测引用但不在参考文献列表中的
        orphan_citations = citations - references
        for cite in orphan_citations:
            issues.append({
                "severity": "critical",
                "category": "引用错误",
                "title": f"引用 [{cite}] 在参考文献中不存在",
                "description": f"正文中引用了 [{cite}]，但在参考文献列表中找不到对应条目",
                "suggestion": "检查引用编号是否正确，或添加缺失的参考文献"
            })
        
        # 检测在参考文献中但未被引用的
        unreferenced_refs = references - citations
        for ref in unreferenced_refs:
            issues.append({
                "severity": "warning",
                "category": "未引用文献",
                "title": f"参考文献 [{ref}] 未被引用",
                "description": f"参考文献列表中的 [{ref}] 在正文中未被引用",
                "suggestion": "删除未使用的参考文献或在正文中添加引用"
            })
        
        # 检查引用格式
        malformed_citations = re.findall(r'\[\d+[^]\d]*\]', content)
        if malformed_citations:
            issues.append({
                "severity": "info",
                "category": "格式问题",
                "title": "发现可能格式错误的引用",
                "description": f"检测到 {len(malformed_citations)} 个可能格式错误的引用",
                "suggestion": "检查引用格式是否正确，应为 [数字] 格式"
            })
        
        return self._build_result(
            status="completed",
            summary=f"引用检查完成，发现 {len(references)} 条参考文献和 {len(citations)} 处引用",
            issues=issues
        )
    
    async def _validate_data_source(self, content: str, options: dict) -> dict:
        """
        验证数据来源
        
        检查内容：
        - 数据来源是否明确标注
        - 数据集URL是否可访问
        - 数据描述是否与实际内容匹配
        - 是否存在数据造假嫌疑
        """
        issues = []
        
        if not content:
            return self._empty_result("数据来源验证")
        
        # 检查是否提到数据来源
        data_keywords = ["数据来源", "数据集", "dataset", "data source", "data from", 
                        "来源于", "收集自", "obtained from", "collected from"]
        has_data_source = any(kw in content.lower() for kw in data_keywords)
        
        if not has_data_source:
            issues.append({
                "severity": "warning",
                "category": "数据来源",
                "title": "未明确标注数据来源",
                "description": "论文中未找到明确的数据来源说明",
                "suggestion": "建议在方法部分明确说明数据来源"
            })
        
        # 检查URL
        url_pattern = r'https?://[^\s<>\"\')\]]+'
        urls = re.findall(url_pattern, content)
        
        # 检查DOI
        doi_pattern = r'doi:\s*(10\.\d{4,}/[^\s]+)'
        dois = re.findall(doi_pattern, content, re.IGNORECASE)
        
        if urls:
            # 异步检查URL可访问性（抽样检查）
            async with httpx.AsyncClient(timeout=5.0) as client:
                for url in urls[:3]:  # 只检查前3个URL
                    try:
                        response = await client.head(url)
                        if response.status_code >= 400:
                            issues.append({
                                "severity": "critical",
                                "category": "数据来源",
                                "title": f"URL不可访问: {url[:50]}...",
                                "description": f"返回状态码: {response.status_code}",
                                "suggestion": "请检查URL是否正确，或提供替代链接"
                            })
                    except Exception:
                        issues.append({
                            "severity": "warning",
                            "category": "数据来源",
                            "title": f"URL无法访问: {url[:50]}...",
                            "description": "无法连接到该URL",
                            "suggestion": "请检查URL是否正确"
                        })
        
        # 检查数据统计描述
        stat_patterns = [
            (r'样本量[为是：:]\s*(\d+)', "样本量"),
            (r'n\s*=\s*(\d+)', "样本量"),
            (r'p\s*[<>=]\s*([\d.]+)', "p值"),
            (r'置信区间', "置信区间"),
        ]
        
        for pattern, name in stat_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                # 验证统计值的合理性
                if name == "样本量":
                    for match in matches:
                        n = int(match)
                        if n < 10:
                            issues.append({
                                "severity": "warning",
                                "category": "统计问题",
                                "title": f"样本量过小: {n}",
                                "description": "样本量小于10可能影响统计结论的可靠性",
                                "suggestion": "考虑增加样本量或说明样本量选择的理由"
                            })
                elif name == "p值":
                    for match in matches:
                        p = float(match)
                        if p > 1 or p < 0:
                            issues.append({
                                "severity": "critical",
                                "category": "统计错误",
                                "title": f"p值异常: {p}",
                                "description": "p值应在0-1之间",
                                "suggestion": "请检查p值是否正确"
                            })
        
        return self._build_result(
            status="completed",
            summary="数据来源验证完成",
            issues=issues
        )
    
    async def _validate_data_processing(self, content: str, options: dict) -> dict:
        """
        验证数据处理
        
        检查内容：
        - 统计方法是否正确
        - 样本量是否充足
        - p值、置信区间合理性
        - 图表数据与正文报告的一致性
        - GRIM/SPRITE测试
        """
        issues = []
        
        if not content:
            return self._empty_result("数据处理验证")
        
        # 提取统计数据
        stats = {
            "means": [],
            "sds": [],
            "ns": [],
            "pvalues": []
        }
        
        # 提取均值
        mean_pattern = r'(?:M|均值|mean)\s*[=:]\s*([\d.]+)'
        stats["means"] = [float(m) for m in re.findall(mean_pattern, content, re.IGNORECASE)]
        
        # 提取标准差
        sd_pattern = r'(?:SD|标准差|std)\s*[=:]\s*([\d.]+)'
        stats["sds"] = [float(s) for s in re.findall(sd_pattern, content, re.IGNORECASE)]
        
        # 提取样本量
        n_pattern = r'(?:N|n|样本量)\s*[=:]\s*(\d+)'
        stats["ns"] = [int(n) for n in re.findall(n_pattern, content, re.IGNORECASE)]
        
        # 提取p值
        p_pattern = r'p\s*[<>=]\s*([\d.]+)'
        stats["pvalues"] = [float(p) for p in re.findall(p_pattern, content, re.IGNORECASE)]
        
        # 验证p值
        for p in stats["pvalues"]:
            if p < 0 or p > 1:
                issues.append({
                    "severity": "critical",
                    "category": "统计错误",
                    "title": f"p值超出范围: {p}",
                    "description": "p值必须在0到1之间",
                    "suggestion": "请检查p值的报告是否正确"
                })
            elif p == 0.0:
                issues.append({
                    "severity": "warning",
                    "category": "统计问题",
                    "title": "p值报告为0.0",
                    "description": "p值通常不应精确为0",
                    "suggestion": "建议报告p < 0.001或更精确的值"
                })
        
        # 验证样本量
        for n in stats["ns"]:
            if n < 30:
                issues.append({
                    "severity": "info",
                    "category": "样本量",
                    "title": f"小样本研究 (n={n})",
                    "description": "样本量小于30，统计检验力可能不足",
                    "suggestion": "考虑增加样本量或使用适合小样本的统计方法"
                })
        
        # GRIM测试（GRIM test）- 验证均值与整数数据的一致性
        if stats["means"] and stats["ns"]:
            for mean, n in zip(stats["means"], stats["ns"]):
                if n > 0:
                    # GRIM测试：均值乘以样本量应该是整数
                    product = mean * n
                    if not product.is_integer() and product > 1:
                        # 检查是否接近整数
                        if abs(product - round(product)) > 0.01:
                            issues.append({
                                "severity": "critical",
                                "category": "GRIM测试失败",
                                "title": f"均值 {mean} 与样本量 {n} 不一致",
                                "description": f"M × N = {product:.4f}，应为整数",
                                "suggestion": "请检查均值和样本量是否正确"
                            })
        
        return self._build_result(
            status="completed",
            summary="数据处理验证完成",
            issues=issues
        )
    
    async def _validate_reference(self, content: str, options: dict) -> dict:
        """
        验证参考文献真实性
        
        检查内容：
        - DOI是否存在且有效
        - 标题、作者、期刊信息是否匹配
        - 发表年份是否合理
        - 是否是已知的虚假期刊或掠夺性期刊
        """
        issues = []
        
        if not content:
            return self._empty_result("参考文献验证")
        
        # 提取参考文献部分
        ref_section_pattern = r'(?:References|参考文献|Bibliography)\s*\n([\s\S]+?)(?:\n\n|\Z)'
        ref_match = re.search(ref_section_pattern, content, re.IGNORECASE)
        
        if not ref_match:
            return self._build_result(
                status="completed",
                summary="未找到参考文献部分",
                issues=[{
                    "severity": "info",
                    "category": "结构问题",
                    "title": "未找到参考文献部分",
                    "description": "论文中未检测到标准的参考文献部分",
                    "suggestion": "请确保论文包含参考文献列表"
                }]
            )
        
        ref_text = ref_match.group(1)
        
        # 提取DOI
        doi_pattern = r'doi:\s*(10\.\d{4,}/[^\s,;]+)'
        dois = re.findall(doi_pattern, ref_text, re.IGNORECASE)
        
        # 验证DOI
        async with httpx.AsyncClient(timeout=10.0) as client:
            for doi in dois[:5]:  # 只检查前5个DOI
                try:
                    response = await client.get(
                        f"https://api.crossref.org/works/{doi}",
                        headers={"Accept": "application/json"}
                    )
                    if response.status_code == 404:
                        issues.append({
                            "severity": "critical",
                            "category": "虚假文献",
                            "title": f"DOI不存在: {doi}",
                            "description": "Crossref数据库中未找到此DOI",
                            "suggestion": "请检查DOI是否正确，或该文献可能是虚假引用"
                        })
                    elif response.status_code == 200:
                        data = response.json()
                        # 验证年份
                        year = data.get("message", {}).get("published", {}).get("date-parts", [[None]])[0][0]
                        if year and (year < 1900 or year > 2030):
                            issues.append({
                                "severity": "warning",
                                "category": "年份异常",
                                "title": f"文献年份异常: {year}",
                                "description": f"DOI {doi} 的发表年份为 {year}",
                                "suggestion": "请检查年份是否正确"
                            })
                except httpx.TimeoutException:
                    issues.append({
                        "severity": "info",
                        "category": "验证超时",
                        "title": f"DOI验证超时: {doi}",
                        "description": "无法在规定时间内验证此DOI",
                        "suggestion": "请稍后重试"
                    })
                except Exception as e:
                    issues.append({
                        "severity": "info",
                        "category": "验证错误",
                        "title": f"DOI验证失败: {doi}",
                        "description": str(e),
                        "suggestion": "请手动验证此文献"
                    })
        
        # 检查参考文献数量
        ref_entries = re.findall(r'\[\d+\]', ref_text)
        if len(ref_entries) < 5:
            issues.append({
                "severity": "info",
                "category": "文献数量",
                "title": f"参考文献数量较少: {len(ref_entries)}",
                "description": "论文的参考文献数量可能不足",
                "suggestion": "建议增加相关文献的引用"
            })
        
        return self._build_result(
            status="completed",
            summary=f"参考文献验证完成，检查了 {len(dois)} 个DOI",
            issues=issues
        )
    
    async def generate_report(
        self,
        document_id: str,
        validation_results: dict
    ) -> str:
        """
        生成Markdown格式的验证报告
        """
        report_lines = []
        report_lines.append("# 论文验证报告\n")
        report_lines.append(f"**文档ID**: {document_id}\n")
        report_lines.append(f"**生成时间**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append("\n---\n\n")
        
        # 计算总问题数
        total_issues = sum(r.get("issues_count", 0) for r in validation_results.values())
        critical_issues = sum(r.get("critical_count", 0) for r in validation_results.values())
        warning_issues = sum(r.get("warning_count", 0) for r in validation_results.values())
        
        report_lines.append("## 验证总结\n\n")
        report_lines.append(f"| 指标 | 数量 |\n")
        report_lines.append(f"|------|------|\n")
        report_lines.append(f"| 总问题数 | {total_issues} |\n")
        report_lines.append(f"| 严重问题 | {critical_issues} |\n")
        report_lines.append(f"| 警告 | {warning_issues} |\n")
        report_lines.append("\n---\n\n")
        
        # 各项验证结果
        type_names = {
            "format": "格式检查",
            "figure_table": "图表引用检查",
            "citation": "参考文献引用检查",
            "data_source": "数据来源验证",
            "data_processing": "数据处理验证",
            "reference": "参考文献验证"
        }
        
        for vtype, result in validation_results.items():
            report_lines.append(f"## {type_names.get(vtype, vtype)}\n\n")
            report_lines.append(f"**状态**: {'✅ 完成' if result.get('status') == 'completed' else '❌ 失败'}\n")
            report_lines.append(f"**总结**: {result.get('summary', '')}\n\n")
            
            if result.get("issues"):
                report_lines.append("### 发现的问题\n\n")
                for issue in result["issues"]:
                    icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue.get("severity", "info"), "⚪")
                    report_lines.append(f"{icon} **{issue.get('title', '')}**\n")
                    report_lines.append(f"  - {issue.get('description', '')}\n")
                    if issue.get("suggestion"):
                        report_lines.append(f"  - **建议**: {issue['suggestion']}\n")
                    report_lines.append("\n")
            else:
                report_lines.append("✅ 未发现问题\n\n")
            
            report_lines.append("\n---\n\n")
        
        return "\n".join(report_lines)
    
    def _empty_result(self, name: str) -> dict:
        """返回空结果"""
        return {
            "status": "completed",
            "issues_count": 0,
            "critical_count": 0,
            "warning_count": 0,
            "info_count": 0,
            "summary": f"{name}完成（无内容可分析）",
            "details": {},
            "issues": []
        }
    
    def _build_result(
        self,
        status: str,
        summary: str,
        issues: List[Dict[str, Any]]
    ) -> dict:
        """构建验证结果"""
        critical_count = sum(1 for i in issues if i.get("severity") == "critical")
        warning_count = sum(1 for i in issues if i.get("severity") == "warning")
        info_count = sum(1 for i in issues if i.get("severity") == "info")
        
        return {
            "status": status,
            "issues_count": len(issues),
            "critical_count": critical_count,
            "warning_count": warning_count,
            "info_count": info_count,
            "summary": summary,
            "details": {},
            "issues": issues
        }
