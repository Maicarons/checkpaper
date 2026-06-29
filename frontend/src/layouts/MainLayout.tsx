import React from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, theme } from 'antd'
import {
  HomeOutlined,
  UploadOutlined,
  HistoryOutlined,
  FileTextOutlined,
} from '@ant-design/icons'

const { Header, Content, Footer } = Layout

const MainLayout: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken()

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
    <Layout>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div className="logo" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          CheckPaper
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: '0 48px' }}>
        <div
          className="site-layout-content"
          style={{
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
            marginTop: 24,
          }}
        >
          <Outlet />
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        CheckPaper ©{new Date().getFullYear()} - AI论文验证智能体系统
      </Footer>
    </Layout>
  )
}

export default MainLayout
