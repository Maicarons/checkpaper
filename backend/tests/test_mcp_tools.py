"""
MCP 工具测试
"""

import pytest

from backend.mcp_server.tools import (
    _extract_citations,
    _extract_references,
    check_citations,
    check_figures,
    check_format,
)


@pytest.mark.asyncio
async def test_check_citations():
    """测试引用检查"""
    content = "This is a test paper [1]. Another reference [2,3]."
    references = [
        {"id": "1", "text": "Reference 1"},
        {"id": "2", "text": "Reference 2"},
        {"id": "3", "text": "Reference 3"},
        {"id": "4", "text": "Reference 4"},
    ]
    citations = [
        {"key": "1"},
        {"key": "2"},
        {"key": "3"},
    ]

    result = await check_citations(content, references, citations)

    assert "issues" in result
    assert "total_references" in result
    assert "total_citations" in result
    assert result["total_references"] == 4
    assert result["total_citations"] == 3


@pytest.mark.asyncio
async def test_check_citations_missing_reference():
    """测试缺失引用检查"""
    content = "This is a test paper [1] and [5]."
    references = [
        {"id": "1", "text": "Reference 1"},
    ]
    citations = [
        {"key": "1"},
        {"key": "5"},
    ]

    result = await check_citations(content, references, citations)

    # 应该有警告：引用5在参考文献中不存在
    assert len(result["issues"]) > 0
    assert any("5" in issue["title"] for issue in result["issues"])


@pytest.mark.asyncio
async def test_check_figures():
    """测试图表引用检查"""
    content = "See Figure 1 and Table 1."
    figures = [
        {"id": "1", "page": 1},
        {"id": "2", "page": 2},
    ]
    tables = [
        {"id": "1"},
    ]

    result = await check_figures(content, figures, tables)

    assert "issues" in result
    assert "figures_count" in result
    assert "tables_count" in result
    assert result["figures_count"] == 2
    assert result["tables_count"] == 1


@pytest.mark.asyncio
async def test_check_format():
    """测试格式检查"""
    content = """
    摘要
    这是一篇测试论文的摘要。

    引言
    这是引言部分。

    方法
    这是方法部分。

    结果
    这是结果部分。

    讨论
    这是讨论部分。

    结论
    这是结论部分。
    """

    result = await check_format(content)

    assert "issues" in result
    assert "sections_found" in result
    assert "content_length" in result


def test_extract_references():
    """测试提取参考文献"""
    text = """
    References
    [1] Smith, J. (2020). Test Paper 1. Journal of Testing.
    [2] Johnson, A. (2021). Test Paper 2. Another Journal.
    [3] Williams, B. (2022). Test Paper 3. doi: 10.1234/test
    """

    references = _extract_references(text)

    assert len(references) == 3
    assert references[0]["id"] == "1"
    assert references[2]["doi"] == "10.1234/test"


def test_extract_citations():
    """测试提取引用"""
    text = "This paper [1] cites [2,3] and also [4-6]."

    citations = _extract_citations(text)

    # 应该提取出 1, 2, 3, 4, 5, 6
    keys = [c["key"] for c in citations]
    assert "1" in keys
    assert "2" in keys
    assert "3" in keys
