import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Typography,
  Card,
  Table,
  Tag,
  Button,
  Space,
  message,
  Empty,
  Popconfirm,
} from 'antd'
import {
  FileTextOutlined,
  DeleteOutlined,
  EyeOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { documentApi, validationApi } from '../services/api'

const { Title } = Typography

interface DocumentRecord {
  id: string
  filename: string
  file_type: string
  file_size: number
  status: string
  upload_time: string
}

interface ValidationRecord {
  task_id: string
  document_id: string
  status: string
  created_at: string
  completed_at?: string
}

const HistoryPage: React.FC = () => {
  const navigate = useNavigate()
  const [documents, setDocuments] = useState<DocumentRecord[]>([])
  const [validations, setValidations] = useState<ValidationRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'documents' | 'validations'>('validations')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [docsData, tasksData] = await Promise.all([
        documentApi.list(),
        validationApi.listTasks(),
      ]) as unknown as [{ documents: DocumentRecord[] }, ValidationRecord[]]
      setDocuments(docsData.documents || [])
      setValidations(tasksData || [])
    } catch (error) {
      message.error('获取数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteDocument = async (id: string) => {
    try {
      await documentApi.delete(id)
      message.success('删除成功')
      fetchData()
    } catch (error) {
      message.error('删除失败')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
  }

  const getStatusTag = (status: string) => {
    const statusMap: Record<string, { color: string; text: string }> = {
      uploaded: { color: 'default', text: '已上传' },
      parsing: { color: 'processing', text: '解析中' },
      parsed: { color: 'success', text: '已解析' },
      failed: { color: 'error', text: '失败' },
      pending: { color: 'default', text: '等待中' },
      running: { color: 'processing', text: '验证中' },
      completed: { color: 'success', text: '已完成' },
      cancelled: { color: 'warning', text: '已取消' },
    }
    const config = statusMap[status] || { color: 'default', text: status }
    return <Tag color={config.color}>{config.text}</Tag>
  }

  const getFileTypeTag = (type: string) => {
    const typeMap: Record<string, { color: string; text: string }> = {
      pdf: { color: 'red', text: 'PDF' },
      word: { color: 'blue', text: 'Word' },
      latex: { color: 'green', text: 'LaTeX' },
      bibtex: { color: 'orange', text: 'BibTeX' },
    }
    const config = typeMap[type] || { color: 'default', text: type }
    return <Tag color={config.color}>{config.text}</Tag>
  }

  const documentColumns: ColumnsType<DocumentRecord> = [
    {
      title: '文件名',
      dataIndex: 'filename',
      key: 'filename',
      render: (text) => (
        <Space>
          <FileTextOutlined />
          {text}
        </Space>
      ),
    },
    {
      title: '类型',
      dataIndex: 'file_type',
      key: 'file_type',
      render: (type) => getFileTypeTag(type),
    },
    {
      title: '大小',
      dataIndex: 'file_size',
      key: 'file_size',
      render: (size) => formatFileSize(size),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => getStatusTag(status),
    },
    {
      title: '上传时间',
      dataIndex: 'upload_time',
      key: 'upload_time',
      render: (time) => new Date(time).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Popconfirm
            title="确定要删除这个文档吗？"
            onConfirm={() => handleDeleteDocument(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const validationColumns: ColumnsType<ValidationRecord> = [
    {
      title: '任务ID',
      dataIndex: 'task_id',
      key: 'task_id',
      render: (id) => (
        <Button
          type="link"
          onClick={() => navigate(`/validation/${id}`)}
        >
          {id.substring(0, 8)}...
        </Button>
      ),
    },
    {
      title: '文档ID',
      dataIndex: 'document_id',
      key: 'document_id',
      render: (id) => id.substring(0, 8) + '...',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => getStatusTag(status),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (time) => new Date(time).toLocaleString('zh-CN'),
    },
    {
      title: '完成时间',
      dataIndex: 'completed_at',
      key: 'completed_at',
      render: (time) => (time ? new Date(time).toLocaleString('zh-CN') : '-'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/validation/${record.task_id}`)}
          >
            查看
          </Button>
          {record.status === 'completed' && (
            <Button
              type="link"
              icon={<FileTextOutlined />}
              onClick={() => navigate(`/report/${record.task_id}`)}
            >
              报告
            </Button>
          )}
        </Space>
      ),
    },
  ]

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '40px 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <Title level={2}>验证历史</Title>
        <Button icon={<ReloadOutlined />} onClick={fetchData}>
          刷新
        </Button>
      </div>

      <Card
        tabList={[
          { key: 'validations', tab: '验证任务' },
          { key: 'documents', tab: '上传文档' },
        ]}
        activeTabKey={activeTab}
        onTabChange={(key) => setActiveTab(key as 'documents' | 'validations')}
      >
        {activeTab === 'validations' ? (
          <Table
            columns={validationColumns}
            dataSource={validations}
            rowKey="task_id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            locale={{ emptyText: <Empty description="暂无验证记录" /> }}
          />
        ) : (
          <Table
            columns={documentColumns}
            dataSource={documents}
            rowKey="id"
            loading={loading}
            pagination={{ pageSize: 10 }}
            locale={{ emptyText: <Empty description="暂无上传文档" /> }}
          />
        )}
      </Card>
    </div>
  )
}

export default HistoryPage
