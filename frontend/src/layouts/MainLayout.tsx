import React from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, Button, Space, Tooltip } from 'antd'
import {
  HomeOutlined,
  UploadOutlined,
  HistoryOutlined,
  GithubOutlined,
  BookOutlined,
} from '@ant-design/icons'

const { Header, Content, Footer } = Layout

const MainLayout: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
    },
    {
      key: '/upload',
      icon: <UploadOutlined />,
      label: '上传论文',
    },
    {
      key: '/history',
      icon: <HistoryOutlined />,
      label: '验证历史',
    },
  ]

  const handleMenuClick = (info: { key: string }) => {
    navigate(info.key)
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          background: '#fff',
          borderBottom: '1px solid #E5E7EB',
          padding: '0 24px',
          position: 'sticky',
          top: 0,
          zIndex: 50,
          boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        }}
      >
        {/* Logo */}
        <div
          onClick={() => navigate('/')}
          style={{
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            marginRight: 48,
          }}
        >
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 8,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              fontWeight: 700,
              fontSize: 16,
            }}
          >
            CP
          </div>
          <span
            style={{
              fontSize: 20,
              fontWeight: 700,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            CheckPaper
          </span>
        </div>

        {/* Navigation Menu */}
        <Menu
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          style={{
            flex: 1,
            minWidth: 0,
            border: 'none',
            background: 'transparent',
          }}
        />

        {/* Right Actions */}
        <Space size={8}>
          <Tooltip title="GitHub 仓库">
            <Button
              type="text"
              icon={<GithubOutlined />}
              href="https://github.com/Maicarons/checkpaper"
              target="_blank"
              style={{ color: '#6B7280' }}
            />
          </Tooltip>
          <Tooltip title="文档">
            <Button
              type="text"
              icon={<BookOutlined />}
              href="https://github.com/Maicarons/checkpaper#readme"
              target="_blank"
              style={{ color: '#6B7280' }}
            />
          </Tooltip>
        </Space>
      </Header>

      <Content
        style={{
          flex: 1,
          background: location.pathname === '/' ? '#fff' : '#F9FAFB',
        }}
      >
        <Outlet />
      </Content>

      <Footer
        style={{
          textAlign: 'center',
          background: '#111827',
          color: '#9CA3AF',
          padding: '24px 50px',
        }}
      >
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <Space split={<span style={{ color: '#374151' }}>|</span>}>
            <a
              href="https://github.com/Maicarons/checkpaper"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#9CA3AF' }}
            >
              GitHub
            </a>
            <a
              href="https://github.com/Maicarons/checkpaper#readme"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#9CA3AF' }}
            >
              文档
            </a>
            <a
              href="https://github.com/Maicarons/checkpaper/issues"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#9CA3AF' }}
            >
              问题反馈
            </a>
            <a
              href="https://github.com/Maicarons/checkpaper/blob/main/LICENSE"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#9CA3AF' }}
            >
              MIT 许可证
            </a>
          </Space>
          <div style={{ marginTop: 12 }}>
            © {new Date().getFullYear()} CheckPaper - AI论文验证智能体系统
          </div>
        </div>
      </Footer>
    </Layout>
  )
}

export default MainLayout
