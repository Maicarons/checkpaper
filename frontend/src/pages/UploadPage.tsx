import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Typography,
  Upload,
  Button,
  Card,
  message,
  Checkbox,
  Space,
  Row,
  Col,
  Steps,
  Tag,
} from 'antd'
import {
  InboxOutlined,
  UploadOutlined,
  CheckCircleOutlined,
  FileTextOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons'
import type { UploadFile, UploadProps } from 'antd'
import { documentApi, validationApi } from '../services/api'

const { Title, Paragraph, Text } = Typography
const { Dragger } = Upload

const validationTypes = [
  {
    label: '格式检查',
    value: 'format',
    description: '检查论文格式、结构、目录对应关系',
    icon: <FileTextOutlined style={{ color: '#4F46E5' }} />,
    color: '#EEF2FF',
  },
  {
    label: '图表引用检查',
    value: 'figure_table',
    description: '检查图片/表格是否在文中被显式引用',
    icon: <FileTextOutlined style={{ color: '#059669' }} />,
    color: '#ECFDF5',
  },
  {
    label: '参考文献引用检查',
    value: 'citation',
    description: '检查引用标记与文献列表的一致性',
    icon: <FileTextOutlined style={{ color: '#D97706' }} />,
    color: '#FFFBEB',
  },
  {
    label: '数据来源验证',
    value: 'data_source',
    description: '验证论文中数据来源的真实性',
    icon: <SafetyCertificateOutlined style={{ color: '#DC2626' }} />,
    color: '#FEF2F2',
  },
  {
    label: '数据处理验证',
    value: 'data_processing',
    description: '验证数据处理方法的正确性',
    icon: <CheckCircleOutlined style={{ color: '#7C3AED' }} />,
    color: '#F5F3FF',
  },
  {
    label: '参考文献验证',
    value: 'reference',
    description: '联网搜索验证参考文献的真实性',
    icon: <FileTextOutlined style={{ color: '#0891B2' }} />,
    color: '#ECFEFF',
  },
]

const UploadPage: React.FC = () => {
  const navigate = useNavigate()
  const [fileList, setFileList] = useState<UploadFile[]>([])
  const [uploading, setUploading] = useState(false)
  const [selectedTypes, setSelectedTypes] = useState<string[]>(validationTypes.map((t) => t.value))

  const handleUpload = async () => {
    if (fileList.length === 0) {
      message.warning('请先选择要上传的论文文件')
      return
    }

    const file = fileList[0]
    const formData = new FormData()
    formData.append('file', file.originFileObj as Blob)

    setUploading(true)

    try {
      // 上传文件
      const uploadResult = await documentApi.upload(formData) as unknown as { id: string }
      message.success('文件上传成功')

      // 开始验证
      const validationResult = await validationApi.startValidation({
        document_id: uploadResult.id,
        validation_types: selectedTypes,
      }) as unknown as { task_id: string }

      message.success('验证任务已创建')
      navigate(`/validation/${validationResult.task_id}`)
    } catch (error: any) {
      message.error(error.response?.data?.detail || '上传失败，请重试')
    } finally {
      setUploading(false)
    }
  }

  const uploadProps: UploadProps = {
    onRemove: () => {
      setFileList([])
    },
    beforeUpload: (file) => {
      // 验证文件类型
      const allowedExtensions = ['.pdf', '.docx', '.doc', '.tex', '.latex']
      const extension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'))

      if (!allowedExtensions.includes(extension)) {
        message.error('只支持 PDF、Word、LaTeX 格式的文件')
        return false
      }

      // 验证文件大小 (50MB)
      if (file.size > 50 * 1024 * 1024) {
        message.error('文件大小不能超过 50MB')
        return false
      }

      setFileList([file])
      return false
    },
    fileList,
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(180deg, #F9FAFB 0%, #fff 100%)',
        padding: '48px 24px',
      }}
    >
      <div style={{ maxWidth: 1000, margin: '0 auto' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <Tag
            color="blue"
            style={{
              padding: '4px 16px',
              borderRadius: 20,
              fontSize: 14,
              marginBottom: 16,
            }}
          >
            第 1 步
          </Tag>
          <Title level={2} style={{ fontSize: 36, fontWeight: 700, marginBottom: 12 }}>
            上传论文
          </Title>
          <Paragraph style={{ fontSize: 18, color: '#6B7280', maxWidth: 500, margin: '0 auto' }}>
            选择您要验证的论文文件，支持多种格式
          </Paragraph>
        </div>

        {/* Steps */}
        <Steps
          current={0}
          items={[
            { title: '上传论文', description: '选择文件' },
            { title: '选择验证项', description: '配置检查' },
            { title: 'AI 分析', description: '自动验证' },
            { title: '查看报告', description: '获取结果' },
          ]}
          style={{ marginBottom: 48 }}
        />

        <Row gutter={32}>
          {/* Upload Area */}
          <Col xs={24} lg={14}>
            <Card
              style={{
                borderRadius: 16,
                boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                border: 'none',
              }}
              bodyStyle={{ padding: 32 }}
            >
              <Dragger
                {...uploadProps}
                style={{
                  borderRadius: 12,
                  border: '2px dashed #D1D5DB',
                  background: '#F9FAFB',
                  padding: '40px 20px',
                }}
              >
                <p className="ant-upload-drag-icon">
                  <InboxOutlined style={{ fontSize: 64, color: '#9CA3AF' }} />
                </p>
                <p className="ant-upload-text" style={{ fontSize: 18, fontWeight: 600, color: '#374151' }}>
                  点击或拖拽文件到此区域上传
                </p>
                <p className="ant-upload-hint" style={{ fontSize: 14, color: '#6B7280' }}>
                  支持 PDF、Word (.docx)、LaTeX 格式的论文文件，最大 50MB
                </p>
              </Dragger>

              {/* File Info */}
              {fileList.length > 0 && (
                <div
                  style={{
                    marginTop: 16,
                    padding: 16,
                    background: '#F0FDF4',
                    borderRadius: 12,
                    border: '1px solid #BBF7D0',
                  }}
                >
                  <Space>
                    <CheckCircleOutlined style={{ color: '#059669', fontSize: 20 }} />
                    <Text strong style={{ color: '#059669' }}>
                      已选择: {fileList[0].name}
                    </Text>
                  </Space>
                </div>
              )}
            </Card>
          </Col>

          {/* Validation Options */}
          <Col xs={24} lg={10}>
            <Card
              style={{
                borderRadius: 16,
                boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                border: 'none',
              }}
              bodyStyle={{ padding: 32 }}
            >
              <Title level={4} style={{ marginBottom: 8, fontWeight: 600 }}>
                选择验证项目
              </Title>
              <Paragraph style={{ color: '#6B7280', marginBottom: 24 }}>
                请选择需要进行的验证项目，可以多选：
              </Paragraph>

              <Checkbox.Group
                value={selectedTypes}
                onChange={setSelectedTypes}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }} size={12}>
                  {validationTypes.map((type) => (
                    <Card
                      key={type.value}
                      size="small"
                      style={{
                        borderRadius: 12,
                        border: selectedTypes.includes(type.value) ? '2px solid #4F46E5' : '1px solid #E5E7EB',
                        background: selectedTypes.includes(type.value) ? type.color : '#fff',
                        transition: 'all 0.2s ease',
                        cursor: 'pointer',
                      }}
                      bodyStyle={{ padding: 16 }}
                      hoverable
                    >
                      <Checkbox value={type.value}>
                        <Space>
                          {type.icon}
                          <div>
                            <Text strong>{type.label}</Text>
                            <br />
                            <Text type="secondary" style={{ fontSize: 12 }}>
                              {type.description}
                            </Text>
                          </div>
                        </Space>
                      </Checkbox>
                    </Card>
                  ))}
                </Space>
              </Checkbox.Group>
            </Card>
          </Col>
        </Row>

        {/* Submit Button */}
        <div style={{ textAlign: 'center', marginTop: 48 }}>
          <Button
            type="primary"
            size="large"
            icon={<UploadOutlined />}
            onClick={handleUpload}
            disabled={fileList.length === 0}
            loading={uploading}
            style={{
              height: 56,
              padding: '0 64px',
              fontSize: 18,
              fontWeight: 600,
              borderRadius: 12,
              background: fileList.length === 0 ? '#D1D5DB' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderColor: 'transparent',
              boxShadow: fileList.length > 0 ? '0 4px 14px rgba(102, 126, 234, 0.4)' : 'none',
            }}
          >
            {uploading ? '上传中...' : '开始验证'}
          </Button>
        </div>
      </div>
    </div>
  )
}

export default UploadPage
