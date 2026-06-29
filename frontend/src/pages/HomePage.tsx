import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Typography, Button, Card, Row, Col, Space, Steps, Tag } from 'antd'
import {
  UploadOutlined,
  CheckCircleOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
  SearchOutlined,
  BarChartOutlined,
  GithubOutlined,
  BookOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons'

const { Title, Paragraph, Text } = Typography

const HomePage: React.FC = () => {
  const navigate = useNavigate()

  const features = [
    {
      icon: <FileTextOutlined style={{ fontSize: 40, color: '#4F46E5' }} />,
      title: '多格式支持',
      description: '支持 PDF、Word、LaTeX 等多种论文格式的解析和验证',
      color: '#EEF2FF',
      borderColor: '#C7D2FE',
    },
    {
      icon: <CheckCircleOutlined style={{ fontSize: 40, color: '#059669' }} />,
      title: '全面检查',
      description: '格式规范、引用完整性、数据真实性、参考文献验证等全方位检查',
      color: '#ECFDF5',
      borderColor: '#A7F3D0',
    },
    {
      icon: <SafetyCertificateOutlined style={{ fontSize: 40, color: '#7C3AED' }} />,
      title: 'AI 驱动',
      description: '基于先进的 AI 技术，智能识别论文问题并提供改进建议',
      color: '#F5F3FF',
      borderColor: '#DDD6FE',
    },
    {
      icon: <SearchOutlined style={{ fontSize: 40, color: '#DC2626' }} />,
      title: '联网验证',
      description: '通过 Crossref、Semantic Scholar 等数据库验证参考文献真实性',
      color: '#FEF2F2',
      borderColor: '#FECACA',
    },
    {
      icon: <BarChartOutlined style={{ fontSize: 40, color: '#D97706' }} />,
      title: '数据验证',
      description: 'GRIM/SPRITE 测试验证统计数据一致性，检测数据造假',
      color: '#FFFBEB',
      borderColor: '#FDE68A',
    },
    {
      icon: <FileTextOutlined style={{ fontSize: 40, color: '#0891B2' }} />,
      title: '详细报告',
      description: '生成结构化的验证报告，包含问题清单和改进建议',
      color: '#ECFEFF',
      borderColor: '#A5F3FC',
    },
  ]

  const steps = [
    {
      title: '上传论文',
      description: '支持 PDF、Word、LaTeX 格式',
      icon: <UploadOutlined />,
    },
    {
      title: 'AI 分析',
      description: '智能解析和验证论文内容',
      icon: <SearchOutlined />,
    },
    {
      title: '生成报告',
      description: '详细的验证报告和改进建议',
      icon: <FileTextOutlined />,
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section with Gradient Background */}
      <div
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '80px 0 100px',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Background Pattern */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundImage: `radial-gradient(circle at 25% 25%, rgba(255,255,255,0.15) 1px, transparent 1px),
                             radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 1px, transparent 1px)`,
            backgroundSize: '50px 50px',
          }}
        />

        <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px', position: 'relative', zIndex: 1 }}>
          <div style={{ textAlign: 'center' }}>
            <Tag
              color="rgba(255,255,255,0.2)"
              style={{
                color: '#fff',
                padding: '4px 16px',
                borderRadius: 20,
                fontSize: 14,
                marginBottom: 24,
                border: '1px solid rgba(255,255,255,0.3)',
              }}
            >
              AI 驱动的学术论文验证系统
            </Tag>

            <Title
              level={1}
              style={{
                color: '#fff',
                fontSize: 56,
                fontWeight: 800,
                marginBottom: 24,
                lineHeight: 1.2,
                textShadow: '0 2px 10px rgba(0,0,0,0.2)',
              }}
            >
              CheckPaper
            </Title>

            <Paragraph
              style={{
                color: 'rgba(255,255,255,0.9)',
                fontSize: 20,
                maxWidth: 600,
                margin: '0 auto 40px',
                lineHeight: 1.6,
              }}
            >
              利用人工智能技术，自动检测学术论文中的格式问题、引用错误、数据真实性等，
              帮助研究者提高论文质量
            </Paragraph>

            <Space size="large">
              <Button
                type="primary"
                size="large"
                icon={<UploadOutlined />}
                onClick={() => navigate('/upload')}
                style={{
                  height: 56,
                  padding: '0 40px',
                  fontSize: 18,
                  fontWeight: 600,
                  borderRadius: 12,
                  background: '#fff',
                  borderColor: '#fff',
                  color: '#4F46E5',
                  boxShadow: '0 4px 14px rgba(0,0,0,0.15)',
                }}
              >
                开始验证
              </Button>
              <Button
                size="large"
                icon={<GithubOutlined />}
                href="https://github.com/Maicarons/checkpaper"
                target="_blank"
                style={{
                  height: 56,
                  padding: '0 40px',
                  fontSize: 18,
                  fontWeight: 600,
                  borderRadius: 12,
                  background: 'rgba(255,255,255,0.15)',
                  borderColor: 'rgba(255,255,255,0.4)',
                  color: '#fff',
                  backdropFilter: 'blur(10px)',
                }}
              >
                GitHub
              </Button>
            </Space>

            {/* Stats */}
            <Row gutter={48} style={{ marginTop: 64 }}>
              {[
                { value: '6+', label: '验证类型' },
                { value: '3', label: '支持格式' },
                { value: '100%', label: '自动化' },
              ].map((stat, index) => (
                <Col key={index} xs={8}>
                  <div style={{ textAlign: 'center' }}>
                    <div
                      style={{
                        fontSize: 36,
                        fontWeight: 800,
                        color: '#fff',
                        marginBottom: 8,
                      }}
                    >
                      {stat.value}
                    </div>
                    <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: 16 }}>
                      {stat.label}
                    </div>
                  </div>
                </Col>
              ))}
            </Row>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '80px 24px' }}>
        <div style={{ textAlign: 'center', marginBottom: 64 }}>
          <Title level={2} style={{ fontSize: 36, fontWeight: 700, marginBottom: 16 }}>
            核心功能
          </Title>
          <Paragraph style={{ fontSize: 18, color: '#6B7280', maxWidth: 600, margin: '0 auto' }}>
            全方位的论文验证能力，确保您的学术论文质量
          </Paragraph>
        </div>

        <Row gutter={[24, 24]}>
          {features.map((feature, index) => (
            <Col xs={24} sm={12} lg={8} key={index}>
              <Card
                hoverable
                style={{
                  height: '100%',
                  borderRadius: 16,
                  border: `1px solid ${feature.borderColor}`,
                  background: feature.color,
                  transition: 'all 0.3s ease',
                }}
                bodyStyle={{ padding: 32 }}
                className="feature-card"
              >
                <div
                  style={{
                    width: 64,
                    height: 64,
                    borderRadius: 16,
                    background: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: 20,
                    boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                  }}
                >
                  {feature.icon}
                </div>
                <Title level={4} style={{ marginBottom: 12, fontWeight: 600 }}>
                  {feature.title}
                </Title>
                <Paragraph style={{ color: '#4B5563', marginBottom: 0, lineHeight: 1.6 }}>
                  {feature.description}
                </Paragraph>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* How it works Section */}
      <div
        style={{
          background: '#F9FAFB',
          padding: '80px 0',
        }}
      >
        <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px' }}>
          <div style={{ textAlign: 'center', marginBottom: 64 }}>
            <Title level={2} style={{ fontSize: 36, fontWeight: 700, marginBottom: 16 }}>
              使用流程
            </Title>
            <Paragraph style={{ fontSize: 18, color: '#6B7280' }}>
              简单三步，完成论文验证
            </Paragraph>
          </div>

          <Row gutter={48} justify="center">
            {steps.map((step, index) => (
              <Col xs={24} sm={8} key={index}>
                <div
                  style={{
                    textAlign: 'center',
                    padding: 32,
                    background: '#fff',
                    borderRadius: 16,
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                    height: '100%',
                  }}
                >
                  <div
                    style={{
                      width: 80,
                      height: 80,
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 24px',
                      fontSize: 32,
                      color: '#fff',
                    }}
                  >
                    {step.icon}
                  </div>
                  <div
                    style={{
                      width: 32,
                      height: 32,
                      borderRadius: '50%',
                      background: '#4F46E5',
                      color: '#fff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '-40px auto 16px',
                      fontSize: 14,
                      fontWeight: 700,
                      position: 'relative',
                      zIndex: 1,
                      border: '3px solid #fff',
                    }}
                  >
                    {index + 1}
                  </div>
                  <Title level={4} style={{ marginBottom: 8 }}>
                    {step.title}
                  </Title>
                  <Paragraph style={{ color: '#6B7280', marginBottom: 0 }}>
                    {step.description}
                  </Paragraph>
                </div>
              </Col>
            ))}
          </Row>
        </div>
      </div>

      {/* CTA Section */}
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '80px 24px' }}>
        <Card
          style={{
            borderRadius: 24,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            overflow: 'hidden',
          }}
          bodyStyle={{ padding: '64px 48px' }}
        >
          <Row gutter={48} align="middle">
            <Col xs={24} lg={16}>
              <Title level={2} style={{ color: '#fff', marginBottom: 16, fontSize: 32 }}>
                准备好验证您的论文了吗？
              </Title>
              <Paragraph style={{ color: 'rgba(255,255,255,0.9)', fontSize: 18, marginBottom: 0 }}>
                立即上传您的论文，获取详细的验证报告和改进建议
              </Paragraph>
            </Col>
            <Col xs={24} lg={8} style={{ textAlign: 'center' }}>
              <Button
                type="primary"
                size="large"
                icon={<ArrowRightOutlined />}
                onClick={() => navigate('/upload')}
                style={{
                  height: 56,
                  padding: '0 48px',
                  fontSize: 18,
                  fontWeight: 600,
                  borderRadius: 12,
                  background: '#fff',
                  borderColor: '#fff',
                  color: '#4F46E5',
                }}
              >
                开始验证
              </Button>
            </Col>
          </Row>
        </Card>
      </div>

      {/* Footer Links */}
      <div style={{ background: '#111827', padding: '48px 24px' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <Row gutter={48}>
            <Col xs={24} sm={8}>
              <Title level={4} style={{ color: '#fff', marginBottom: 16 }}>
                CheckPaper
              </Title>
              <Paragraph style={{ color: '#9CA3AF', marginBottom: 24 }}>
                AI 驱动的论文验证智能体系统
              </Paragraph>
              <Space>
                <Button
                  type="text"
                  icon={<GithubOutlined />}
                  href="https://github.com/Maicarons/checkpaper"
                  target="_blank"
                  style={{ color: '#9CA3AF' }}
                >
                  GitHub
                </Button>
                <Button
                  type="text"
                  icon={<BookOutlined />}
                  href="https://github.com/Maicarons/checkpaper#readme"
                  target="_blank"
                  style={{ color: '#9CA3AF' }}
                >
                  文档
                </Button>
              </Space>
            </Col>
            <Col xs={24} sm={8}>
              <Title level={5} style={{ color: '#fff', marginBottom: 16 }}>
                快速链接
              </Title>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                <Button type="link" style={{ color: '#9CA3AF', padding: 0, textAlign: 'left' }} onClick={() => navigate('/upload')}>
                  上传论文
                </Button>
                <Button type="link" style={{ color: '#9CA3AF', padding: 0, textAlign: 'left' }} onClick={() => navigate('/history')}>
                  验证历史
                </Button>
                <Button type="link" href="/docs" style={{ color: '#9CA3AF', padding: 0, textAlign: 'left' }}>
                  API 文档
                </Button>
              </div>
            </Col>
            <Col xs={24} sm={8}>
              <Title level={5} style={{ color: '#fff', marginBottom: 16 }}>
                资源
              </Title>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                <Button type="link" href="https://github.com/Maicarons/checkpaper/issues" target="_blank" style={{ color: '#9CA3AF', padding: 0, textAlign: 'left' }}>
                  问题反馈
                </Button>
                <Button type="link" href="https://github.com/Maicarons/checkpaper/blob/main/CONTRIBUTING.md" target="_blank" style={{ color: '#9CA3AF', padding: 0, textAlign: 'left' }}>
                  贡献指南
                </Button>
                <Button type="link" href="https://github.com/Maicarons/checkpaper/blob/main/LICENSE" target="_blank" style={{ color: '#9CA3AF', padding: 0, textAlign: 'left' }}>
                  MIT 许可证
                </Button>
              </div>
            </Col>
          </Row>

          <div
            style={{
              borderTop: '1px solid #374151',
              marginTop: 48,
              paddingTop: 24,
              textAlign: 'center',
            }}
          >
            <Text style={{ color: '#6B7280' }}>
              © {new Date().getFullYear()} CheckPaper. 基于 MIT 许可证开源.
            </Text>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage
