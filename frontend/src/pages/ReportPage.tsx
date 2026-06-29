import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Typography,
  Card,
  Button,
  Result,
  Spin,
  Tag,
  Descriptions,
  Divider,
  List,
  Space,
  message,
  Row,
  Col,
  Statistic,
} from 'antd'
import {
  DownloadOutlined,
  ArrowLeftOutlined,
  WarningOutlined,
  CloseCircleOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons'
import ReactMarkdown from 'react-markdown'
import { validationApi, reportApi } from '../services/api'

const { Title, Paragraph, Text } = Typography

interface ValidationIssue {
  id: string
  severity: string
  category: string
  title: string
  description: string
  location?: string
  suggestion?: string
}

interface ValidationResult {
  id: string
  validation_type: string
  status: string
  issues_count: number
  critical_count: number
  warning_count: number
  info_count: number
  summary?: string
  issues: ValidationIssue[]
}

interface ReportData {
  task_id: string
  document_id: string
  status: string
  total_issues: number
  critical_issues: number
  warning_issues: number
  info_issues: number
  results: ValidationResult[]
  created_at: string
  completed_at?: string
}

const ReportPage: React.FC = () => {
  const { reportId } = useParams<{ reportId: string }>()
  const navigate = useNavigate()
  const [report, setReport] = useState<ReportData | null>(null)
  const [markdownContent, setMarkdownContent] = useState<string>('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!reportId) return

    const fetchReport = async () => {
      try {
        const data = await validationApi.getResults(reportId)
        setReport(data)

        // 生成 Markdown 报告
        const md = generateMarkdown(data)
        setMarkdownContent(md)
      } catch (error) {
        message.error('获取报告失败')
      } finally {
        setLoading(false)
      }
    }

    fetchReport()
  }, [reportId])

  const generateMarkdown = (data: ReportData): string => {
    const lines: string[] = []

    lines.push('# 论文验证报告\n')
    lines.push(`**任务ID**: ${data.task_id}\n`)
    lines.push(`**生成时间**: ${data.completed_at || data.created_at}\n`)
    lines.push('\n---\n\n')

    lines.push('## 验证总结\n\n')
    lines.push(`| 指标 | 数量 |\n`)
    lines.push(`|------|------|\n`)
    lines.push(`| 总问题数 | ${data.total_issues} |\n`)
    lines.push(`| 严重问题 | ${data.critical_issues} |\n`)
    lines.push(`| 警告 | ${data.warning_issues} |\n`)
    lines.push(`| 信息 | ${data.info_issues} |\n`)
    lines.push('\n---\n\n')

    const typeNames: Record<string, string> = {
      format: '格式检查',
      figure_table: '图表引用检查',
      citation: '参考文献引用检查',
      data_source: '数据来源验证',
      data_processing: '数据处理验证',
      reference: '参考文献验证',
    }

    for (const result of data.results) {
      lines.push(`## ${typeNames[result.validation_type] || result.validation_type}\n\n`)
      lines.push(`**状态**: ${result.status === 'completed' ? '✅ 完成' : '❌ 失败'}\n`)
      lines.push(`**问题数量**: ${result.issues_count}\n\n`)

      if (result.summary) {
        lines.push(`**总结**: ${result.summary}\n\n`)
      }

      if (result.issues.length > 0) {
        lines.push('### 发现的问题\n\n')
        for (const issue of result.issues) {
          const icon =
            issue.severity === 'critical' ? '🔴' : issue.severity === 'warning' ? '🟡' : '🔵'
          lines.push(`${icon} **${issue.title}**\n`)
          lines.push(`- ${issue.description}\n`)
          if (issue.location) {
            lines.push(`- **位置**: ${issue.location}\n`)
          }
          if (issue.suggestion) {
            lines.push(`- **建议**: ${issue.suggestion}\n`)
          }
          lines.push('\n')
        }
      } else {
        lines.push('✅ 未发现问题\n\n')
      }

      lines.push('\n---\n\n')
    }

    return lines.join('')
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
      case 'warning':
        return <WarningOutlined style={{ color: '#faad14' }} />
      default:
        return <InfoCircleOutlined style={{ color: '#1890ff' }} />
    }
  }

  const getSeverityTag = (severity: string) => {
    const config: Record<string, { color: string; text: string }> = {
      critical: { color: 'error', text: '严重' },
      warning: { color: 'warning', text: '警告' },
      info: { color: 'processing', text: '信息' },
    }
    const { color, text } = config[severity] || { color: 'default', text: severity }
    return <Tag color={color}>{text}</Tag>
  }

  const handleDownload = async (format: string) => {
    if (!reportId) return
    try {
      const blob = await reportApi.downloadReport(reportId, format)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report_${reportId}.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      message.error('下载失败')
    }
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
        <Paragraph style={{ marginTop: 16 }}>加载报告中...</Paragraph>
      </div>
    )
  }

  if (!report) {
    return (
      <Result
        status="404"
        title="报告未找到"
        subTitle="请检查报告ID是否正确"
        extra={
          <Button type="primary" onClick={() => navigate('/')}>
            返回首页
          </Button>
        }
      />
    )
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '40px 0' }}>
      <div style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)}>
          返回
        </Button>
      </div>

      <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
        验证报告
      </Title>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总问题数"
              value={report.total_issues}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="严重问题"
              value={report.critical_issues}
              valueStyle={{ color: '#ff4d4f' }}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="警告"
              value={report.warning_issues}
              valueStyle={{ color: '#faad14' }}
              prefix={<WarningOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="信息"
              value={report.info_issues}
              valueStyle={{ color: '#1890ff' }}
              prefix={<InfoCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* 下载按钮 */}
      <Card style={{ marginBottom: 24 }}>
        <Space>
          <Text strong>下载报告：</Text>
          <Button icon={<DownloadOutlined />} onClick={() => handleDownload('md')}>
            Markdown
          </Button>
          <Button icon={<DownloadOutlined />} onClick={() => handleDownload('html')}>
            HTML
          </Button>
          <Button icon={<DownloadOutlined />} onClick={() => handleDownload('pdf')}>
            PDF
          </Button>
        </Space>
      </Card>

      {/* 验证结果详情 */}
      {report.results.map((result) => (
        <Card
          key={result.id}
          title={result.validation_type}
          style={{ marginBottom: 16 }}
          extra={
            <Space>
              <Tag>{result.issues_count} 个问题</Tag>
              {result.status === 'completed' ? (
                <Tag color="success">完成</Tag>
              ) : (
                <Tag color="error">失败</Tag>
              )}
            </Space>
          }
        >
          {result.summary && <Paragraph>{result.summary}</Paragraph>}

          {result.issues.length > 0 ? (
            <List
              dataSource={result.issues}
              renderItem={(issue) => (
                <List.Item>
                  <List.Item.Meta
                    avatar={getSeverityIcon(issue.severity)}
                    title={
                      <Space>
                        {getSeverityTag(issue.severity)}
                        {issue.title}
                      </Space>
                    }
                    description={
                      <div>
                        <Paragraph>{issue.description}</Paragraph>
                        {issue.location && (
                          <Text type="secondary">位置: {issue.location}</Text>
                        )}
                        {issue.suggestion && (
                          <Paragraph>
                            <Text strong>建议: </Text>
                            {issue.suggestion}
                          </Paragraph>
                        )}
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          ) : (
            <Paragraph type="success">✅ 未发现问题</Paragraph>
          )}
        </Card>
      ))}

      {/* Markdown 预览 */}
      <Card title="报告预览 (Markdown)" style={{ marginTop: 24 }}>
        <div className="markdown-content">
          <ReactMarkdown>{markdownContent}</ReactMarkdown>
        </div>
      </Card>
    </div>
  )
}

export default ReportPage
