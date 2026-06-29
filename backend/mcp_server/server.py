"""
CheckPaper MCP 服务器
基于 Model Context Protocol 的验证工具服务器
"""
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import (
    parse_pdf,
    parse_docx,
    parse_latex,
    check_citations,
    verify_references,
    check_figures,
    check_format,
    web_search_reference
)


# 创建 MCP 服务器实例
server = Server("checkpaper-validation")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="parse_pdf",
            description="解析PDF论文，返回结构化数据（标题、正文、参考文献、图表）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "PDF文件路径"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="parse_docx",
            description="解析Word文档，返回结构化数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Word文件路径"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="parse_latex",
            description="解析LaTeX文档，返回结构化数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "LaTeX文件路径"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="check_citations",
            description="检查参考文献引用的一致性",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "论文正文内容"
                    },
                    "references": {
                        "type": "array",
                        "description": "参考文献列表",
                        "items": {"type": "object"}
                    },
                    "citations": {
                        "type": "array",
                        "description": "正文引用列表",
                        "items": {"type": "object"}
                    }
                },
                "required": ["content", "references", "citations"]
            }
        ),
        Tool(
            name="verify_references",
            description="验证参考文献的真实性（DOI查询、Crossref匹配）",
            inputSchema={
                "type": "object",
                "properties": {
                    "references": {
                        "type": "array",
                        "description": "参考文献列表",
                        "items": {
                            "type": "object",
                            "properties": {
                                "doi": {"type": "string"},
                                "title": {"type": "string"},
                                "authors": {"type": "string"},
                                "year": {"type": "integer"}
                            }
                        }
                    }
                },
                "required": ["references"]
            }
        ),
        Tool(
            name="check_figures",
            description="检查图片/表格引用的完整性",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "论文正文内容"
                    },
                    "figures": {
                        "type": "array",
                        "description": "图片列表",
                        "items": {"type": "object"}
                    },
                    "tables": {
                        "type": "array",
                        "description": "表格列表",
                        "items": {"type": "object"}
                    }
                },
                "required": ["content", "figures", "tables"]
            }
        ),
        Tool(
            name="check_format",
            description="检查论文格式规范性",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "论文内容"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "文档元数据"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="web_search_reference",
            description="联网搜索验证参考文献",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "文献标题"
                    },
                    "authors": {
                        "type": "string",
                        "description": "作者"
                    },
                    "doi": {
                        "type": "string",
                        "description": "DOI号"
                    }
                },
                "required": ["title"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
    try:
        if name == "parse_pdf":
            result = await parse_pdf(arguments["file_path"])
        elif name == "parse_docx":
            result = await parse_docx(arguments["file_path"])
        elif name == "parse_latex":
            result = await parse_latex(arguments["file_path"])
        elif name == "check_citations":
            result = await check_citations(
                arguments["content"],
                arguments["references"],
                arguments["citations"]
            )
        elif name == "verify_references":
            result = await verify_references(arguments["references"])
        elif name == "check_figures":
            result = await check_figures(
                arguments["content"],
                arguments["figures"],
                arguments["tables"]
            )
        elif name == "check_format":
            result = await check_format(
                arguments["content"],
                arguments.get("metadata", {})
            )
        elif name == "web_search_reference":
            result = await web_search_reference(
                arguments["title"],
                arguments.get("authors", ""),
                arguments.get("doi", "")
            )
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=str(result))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"工具执行错误: {str(e)}")]


async def run_server():
    """运行 MCP 服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """主入口函数"""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
