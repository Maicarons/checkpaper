import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Typography, Button, Card, Row, Col, Space, Steps } from 'antd'
import {
  UploadOutlined,
  CheckCircleOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons'

const { Title, Paragraph } = Typography

const HomePage: React.FC = () => {
  const navigate = useNavigate()

  const features = [
    {
      icon: <FileTextOutlined style={{ fontSize: 48, color: '#1890ff' }} />,
      title: '多格式支持',
      description: '支持 PDF、Word、LaTeX 等多种论文格式的解析和验证',
    },
    {
      icon: <CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a' }} />,
      title: '全面检查',
      description: '格式规范、引用完整性、数据真实性、参考文献验证等全方位检查',
    },
    {
      icon: <SafetyCertificateOutlined style={{ fontSize: 48, color: '#722ed1' }} />,
      title: 'AI 驱动',
      description: '基于先进的 AI 技术，智能识别论文问题并提供改进建议',
    },
  ]

  const steps = [
    {
      title: '上传论文',
      description: '支持 PDF、Word、LaTeX 格式',
    },
    {
      title: 'AI 分析',
      description: '智能解析和验证论文内容',
    },
    {
      title: '生成报告',
      description: '详细的验证报告和改进建议',
    },
  ]

  return (
    <div style={{ padding: '40px 0' }}>
      {/* Hero Section */}
      <div style={{ textAlign: 'center', marginBottom: 64 }}>
        <Title level={1}>CheckPaper</Title>
        <Title level={3} type="secondary" style={{ fontWeight: 'normal' }}>
          AI论文验证智能体系统
        </Title>
        <Paragraph style={{ fontSize: 18, maxWidth: 600, margin: '24px auto' }}>
          利用人工智能技术，自动检测学术论文中的格式问题、引用错误、数据真实性等，
          帮助研究者提高论文质量。
        </Paragraph>
        <Space size="large">
          <Button
            type="primary"
            size="large"
            icon={<UploadOutlined />}
            onClick={() => navigate('/upload')}
          >
            开始验证
          </Button>
          <Button size="large" onClick={() => navigate('/history')}>
            查看历史
          </Button>
        </Space>
      </div>

      {/* Features Section */}
      <div style={{ marginBottom: 64 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
          核心功能
        </Title>
        <Row gutter={[32, 32]}>
          {features.map((feature, index) => (
            <Col xs={24} sm={8} key={index}>
              <Card
                hoverable
                style={{ textAlign: 'center', height: '100%' }}
                bodyStyle={{ padding: '40px 24px' }}
              >
                <div style={{ marginBottom: 24 }}>{feature.icon}</div>
                <Title level={4}>{feature.title}</Title>
                <Paragraph type="secondary">{feature.description}</Paragraph>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* How it works Section */}
      <div style={{ marginBottom: 64 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
          使用流程
        </Title>
        <Steps
          items={steps}
          style={{ maxWidth: 800, margin: '0 auto' }}
        />
      </div>

      {/* Supported Checks Section */}
      <div>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
          验证内容
        </Title>
        <Row gutter={[16, 16]}>
          {[
            { title: '格式检查', desc: '标题层级、字体字号、页面布局' },
            { title: '图表引用', desc: '图片/表格是否被正确引用' },
            { title: '参考文献', desc: '引用标记与文献列表的一致性' },
            { title: '数据来源', desc: '数据来源的真实性和可访问性' },
            { title: '数据处理', desc: '统计方法的正确性和合理性' },
            { title: '文献验证', desc: '参考文献的真实性和准确性' },
          ].map((item, index) => (
            <Col xs={24} sm={12} md={8} key={index}>
              <Card size="small">
                <Card.Meta
                  title={item.title}
                  description={item.desc}
                />
              </Card>
            </Col>
          ))}
        </Row>
      </div>
    </div>
  )
}

export default HomePage
