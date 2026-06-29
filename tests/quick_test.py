#!/usr/bin/env python3
"""
CheckPaper 快速测试脚本
用于验证项目功能是否正常
"""
import sys
import os
import asyncio

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    try:
        from backend.app.core.config import settings
        print(f"  ✅ 配置模块导入成功")
        print(f"     - API地址: {settings.openai_base_url}")
        print(f"     - 模型: {settings.openai_model}")
    except Exception as e:
        print(f"  ❌ 配置模块导入失败: {e}")
        return False
    
    try:
        from backend.app.services.agent import AgentService
        print(f"  ✅ Agent服务导入成功")
    except Exception as e:
        print(f"  ❌ Agent服务导入失败: {e}")
        return False
    
    try:
        from backend.app.services.document import DocumentService
        print(f"  ✅ 文档服务导入成功")
    except Exception as e:
        print(f"  ❌ 文档服务导入失败: {e}")
        return False
    
    return True


def test_validation():
    """测试验证功能"""
    print("\n🔍 测试验证功能...")
    
    from backend.app.services.agent import AgentService
    
    service = AgentService()
    
    # 测试内容
    test_content = """
    # 测试论文
    
    ## 摘要
    这是一篇测试论文。
    
    ## 引言
    研究背景[1]，相关工作[2,3]。
    
    ## 方法
    如图1所示，表1展示了结果。
    
    ## 参考文献
    [1] Author A. (2020). Paper 1. Journal.
    [2] Author B. (2021). Paper 2. Journal.
    [3] Author C. (2022). Paper 3. Journal.
    """
    
    # 测试格式检查
    try:
        result = asyncio.run(service._validate_format(test_content, {}))
        print(f"  ✅ 格式检查: {result['summary']}")
        print(f"     - 发现 {result['issues_count']} 个问题")
    except Exception as e:
        print(f"  ❌ 格式检查失败: {e}")
    
    # 测试引用检查
    try:
        result = asyncio.run(service._validate_citation(test_content, {}))
        print(f"  ✅ 引用检查: {result['summary']}")
        print(f"     - 发现 {result['issues_count']} 个问题")
    except Exception as e:
        print(f"  ❌ 引用检查失败: {e}")
    
    return True


def test_api():
    """测试API端点"""
    print("\n🔍 测试API端点...")
    
    try:
        from fastapi.testclient import TestClient
        from backend.app.main import app
        
        client = TestClient(app)
        
        # 测试根路由
        response = client.get("/")
        if response.status_code == 200:
            print(f"  ✅ 根路由正常")
        else:
            print(f"  ❌ 根路由异常: {response.status_code}")
        
        # 测试健康检查
        response = client.get("/health")
        if response.status_code == 200:
            print(f"  ✅ 健康检查正常")
        else:
            print(f"  ❌ 健康检查异常: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"  ❌ API测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 50)
    print("CheckPaper 快速测试")
    print("=" * 50)
    
    # 测试导入
    if not test_imports():
        print("\n❌ 导入测试失败，请检查依赖安装")
        sys.exit(1)
    
    # 测试验证功能
    test_validation()
    
    # 测试API
    test_api()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)
    print("\n下一步：")
    print("1. 配置 .env 文件（可选，本地模型无需修改）")
    print("2. 运行后端: uvicorn backend.app.main:app --reload")
    print("3. 运行前端: cd frontend && npm start")


if __name__ == "__main__":
    main()
