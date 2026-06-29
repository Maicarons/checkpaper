"""
CheckPaper 报告服务模块
"""
import uuid
import os
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, func

from ...schemas.report import Report, ReportStatus
from ...schemas.document import Document
from ...core.config import settings


class ReportService:
    """报告服务类"""
    
    def create_report(
        self,
        session: Session,
        document_id: str,
        title: str,
        validation_task_id: Optional[str] = None
    ) -> Report:
        """
        创建报告
        
        Args:
            session: 数据库会话
            document_id: 文档ID
            title: 报告标题
            validation_task_id: 验证任务ID
        
        Returns:
            创建的报告
        """
        report = Report(
            id=str(uuid.uuid4()),
            document_id=document_id,
            validation_task_id=validation_task_id,
            title=title,
            status=ReportStatus.GENERATING,
            created_at=datetime.utcnow()
        )
        session.add(report)
        session.commit()
        session.refresh(report)
        return report
    
    def get_report(self, session: Session, report_id: str) -> Optional[Report]:
        """获取报告"""
        statement = select(Report).where(Report.id == report_id)
        return session.exec(statement).first()
    
    def get_reports(
        self,
        session: Session,
        offset: int = 0,
        limit: int = 20,
        document_id: Optional[str] = None
    ) -> List[Report]:
        """获取报告列表"""
        statement = select(Report)
        
        if document_id:
            statement = statement.where(Report.document_id == document_id)
        
        statement = statement.offset(offset).limit(limit).order_by(Report.created_at.desc())
        return list(session.exec(statement).all())
    
    def get_reports_count(
        self,
        session: Session,
        document_id: Optional[str] = None
    ) -> int:
        """获取报告总数"""
        statement = select(func.count()).select_from(Report)
        
        if document_id:
            statement = statement.where(Report.document_id == document_id)
        
        return session.exec(statement).one()
    
    def update_report(
        self,
        session: Session,
        report_id: str,
        content: str,
        total_issues: int = 0,
        critical_issues: int = 0,
        warning_issues: int = 0,
        info_issues: int = 0,
        score: Optional[float] = None
    ) -> Optional[Report]:
        """
        更新报告
        
        Args:
            session: 数据库会话
            report_id: 报告ID
            content: 报告内容
            total_issues: 总问题数
            critical_issues: 严重问题数
            warning_issues: 警告数
            info_issues: 信息数
            score: 评分
        
        Returns:
            更新后的报告
        """
        report = self.get_report(session, report_id)
        if not report:
            return None
        
        report.content = content
        report.total_issues = total_issues
        report.critical_issues = critical_issues
        report.warning_issues = warning_issues
        report.info_issues = info_issues
        report.score = score
        report.status = ReportStatus.COMPLETED
        report.completed_at = datetime.utcnow()
        
        # 保存到文件
        file_path = self._save_report_to_file(report_id, content)
        report.file_path = file_path
        
        session.add(report)
        session.commit()
        session.refresh(report)
        return report
    
    def delete_report(self, session: Session, report_id: str) -> bool:
        """删除报告"""
        report = self.get_report(session, report_id)
        if not report:
            return False
        
        # 删除文件
        if report.file_path and os.path.exists(report.file_path):
            os.remove(report.file_path)
        
        session.delete(report)
        session.commit()
        return True
    
    def export_report(
        self,
        session: Session,
        report_id: str,
        format: str = "md"
    ) -> str:
        """
        导出报告
        
        Args:
            session: 数据库会话
            report_id: 报告ID
            format: 导出格式
        
        Returns:
            文件路径
        """
        report = self.get_report(session, report_id)
        if not report:
            raise ValueError("报告不存在")
        
        if format == "md":
            return report.file_path
        elif format == "html":
            return self._convert_to_html(report)
        elif format == "pdf":
            return self._convert_to_pdf(report)
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def _save_report_to_file(self, report_id: str, content: str) -> str:
        """保存报告到文件"""
        os.makedirs(settings.report_output_dir, exist_ok=True)
        file_path = os.path.join(settings.report_output_dir, f"report_{report_id}.md")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def _convert_to_html(self, report: Report) -> str:
        """转换为 HTML"""
        import markdown
        
        html_content = markdown.markdown(report.content, extensions=['tables', 'fenced_code'])
        
        # 包装成完整 HTML
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{report.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        # 保存 HTML 文件
        html_path = os.path.join(settings.report_output_dir, f"report_{report.id}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return html_path
    
    def _convert_to_pdf(self, report: Report) -> str:
        """转换为 PDF"""
        # 先转换为 HTML
        html_path = self._convert_to_html(report)
        
        # 使用 weasyprint 转换为 PDF
        try:
            from weasyprint import HTML
            pdf_path = os.path.join(settings.report_output_dir, f"report_{report.id}.pdf")
            HTML(filename=html_path).write_pdf(pdf_path)
            return pdf_path
        except ImportError:
            raise ValueError("PDF 导出需要安装 weasyprint 库")
