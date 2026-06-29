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
} from 'antd'
import { InboxOutlined, UploadOutlined } from '@ant-design/icons'
import type { UploadFile, UploadProps } from 'antd'
import { documentApi, validationApi } from '../services/api'

const { Title, Paragraph } = Typography
const { Dragger } = Upload

const validationTypes = [
  { label: '格式检查', value: 'format', description: '检查论文格式、结构、目录' },
  { label: '图表引用检查', value: 'figure_table', description: '检查图片/表格引用完整性' },
  { label: '参考文献引用检查', value: 'citation', description: '检查引用标记与文献列表' },
  { label: '数据来源验证', value: 'data_source', description: '验证数据来源真实性' },
  { label: '数据处理验证', value: 'data_processing', description: '验证数据处理正确性' },
  { label: '参考文献验证', value: 'reference', description: '验证参考文献真实性' },
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
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '40px 0' }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
        上传论文
      </Title>

      <Card>
        <Dragger {...uploadProps} style={{ marginBottom: 24 }}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
          <p className="ant-upload-hint">
            支持 PDF、Word (.docx)、LaTeX 格式的论文文件，最大 50MB
          </p>
        </Dragger>

        <Title level={4} style={{ marginBottom: 16 }}>
          选择验证项目
        </Title>
        <Paragraph type="secondary" style={{ marginBottom: 16 }}>
          请选择需要进行的验证项目，可以多选：
        </Paragraph>

        <Checkbox.Group
          value={selectedTypes}
          onChange={setSelectedTypes}
          style={{ width: '100%' }}
        >
          <Space direction="vertical" style={{ width: '100%' }}>
            {validationTypes.map((type) => (
              <Card key={type.value} size="small" style={{ marginBottom: 8 }}>
                <Checkbox value={type.value}>
                  <strong>{type.label}</strong>
                  <br />
                  <span style={{ color: '#666' }}>{type.description}</span>
                </Checkbox>
              </Card>
            ))}
          </Space>
        </Checkbox.Group>

        <div style={{ textAlign: 'center', marginTop: 24 }}>
          <Button
            type="primary"
            size="large"
            icon={<UploadOutlined />}
            onClick={handleUpload}
            disabled={fileList.length === 0}
            loading={uploading}
          >
            {uploading ? '上传中...' : '开始验证'}
          </Button>
        </div>
      </Card>
    </div>
  )
}

export default UploadPage
