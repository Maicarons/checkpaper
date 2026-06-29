import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Typography,
  Card,
  Steps,
  Button,
  Result,
  Spin,
  Progress,
  Tag,
  Space,
  message,
} from 'antd'
import {
  LoadingOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  FileTextOutlined,
} from '@ant-design/icons'
import { validationApi } from '../services/api'

const { Title, Paragraph } = Typography

interface ValidationTask {
  task_id: string
  document_id: string
  status: string
  message: string
  created_at: string
  started_at?: string
  completed_at?: string
}

const ValidationPage: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>()
  const navigate = useNavigate()
  const [task, setTask] = useState<ValidationTask | null>(null)
  const [loading, setLoading] = useState(true)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    if (!taskId) return

    const fetchTask = async () => {
      try {
        const data = await validationApi.getTask(taskId) as unknown as ValidationTask
        setTask(data)

        // 更新进度
        if (data.status === 'completed') {
          setProgress(100)
        } else if (data.status === 'running') {
          setProgress(50)
        } else if (data.status === 'pending') {
          setProgress(10)
        }

        // 如果任务还在进行中，继续轮询
        if (data.status === 'pending' || data.status === 'running') {
          setTimeout(fetchTask, 2000)
        }
      } catch (error) {
        message.error('获取任务状态失败')
      } finally {
        setLoading(false)
      }
    }

    fetchTask()
  }, [taskId])

  const getStatusTag = (status: string) => {
    const statusMap: Record<string, { color: string; text: string }> = {
      pending: { color: 'default', text: '等待中' },
      running: { color: 'processing', text: '验证中' },
      completed: { color: 'success', text: '已完成' },
      failed: { color: 'error', text: '失败' },
      cancelled: { color: 'warning', text: '已取消' },
    }
    const config = statusMap[status] || { color: 'default', text: status }
    return <Tag color={config.color}>{config.text}</Tag>
  }

  const getStepStatus = (currentStatus: string) => {
    if (currentStatus === 'completed') return 'finish'
    if (currentStatus === 'running') return 'process'
    if (currentStatus === 'failed') return 'error'
    return 'wait'
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
        <Paragraph style={{ marginTop: 16 }}>加载中...</Paragraph>
      </div>
    )
  }

  if (!task) {
    return (
      <Result
        status="404"
        title="任务未找到"
        subTitle="请检查任务ID是否正确"
        extra={
          <Button type="primary" onClick={() => navigate('/')}>
            返回首页
          </Button>
        }
      />
    )
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '40px 0' }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: 40 }}>
        验证进度
      </Title>

      <Card>
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          {task.status === 'completed' ? (
            <CheckCircleOutlined style={{ fontSize: 64, color: '#52c41a' }} />
          ) : task.status === 'failed' ? (
            <CloseCircleOutlined style={{ fontSize: 64, color: '#ff4d4f' }} />
          ) : (
            <LoadingOutlined style={{ fontSize: 64, color: '#1890ff' }} />
          )}
        </div>

        <Steps
          current={task.status === 'completed' ? 2 : task.status === 'running' ? 1 : 0}
          status={getStepStatus(task.status)}
          items={[
            {
              title: '任务创建',
              description: task.created_at,
            },
            {
              title: '验证中',
              description: task.started_at || '等待开始',
            },
            {
              title: '完成',
              description: task.completed_at || '等待完成',
            },
          ]}
          style={{ marginBottom: 24 }}
        />

        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <Paragraph>
            任务状态: {getStatusTag(task.status)}
          </Paragraph>
          <Paragraph type="secondary">{task.message}</Paragraph>
        </div>

        {(task.status === 'pending' || task.status === 'running') && (
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <Progress
              percent={progress}
              status="active"
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
            />
            <Paragraph type="secondary" style={{ marginTop: 8 }}>
              AI 正在分析您的论文，请稍候...
            </Paragraph>
          </div>
        )}

        {task.status === 'completed' && (
          <div style={{ textAlign: 'center' }}>
            <Button
              type="primary"
              size="large"
              icon={<FileTextOutlined />}
              onClick={() => navigate(`/report/${task.task_id}`)}
            >
              查看验证报告
            </Button>
          </div>
        )}

        {task.status === 'failed' && (
          <div style={{ textAlign: 'center' }}>
            <Space>
              <Button onClick={() => navigate('/')}>返回首页</Button>
              <Button type="primary" onClick={() => navigate('/upload')}>
                重新上传
              </Button>
            </Space>
          </div>
        )}
      </Card>
    </div>
  )
}

export default ValidationPage
