import React from 'react'
import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import ValidationPage from './pages/ValidationPage'
import ReportPage from './pages/ReportPage'
import HistoryPage from './pages/HistoryPage'

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="upload" element={<UploadPage />} />
        <Route path="validation/:taskId" element={<ValidationPage />} />
        <Route path="report/:reportId" element={<ReportPage />} />
        <Route path="history" element={<HistoryPage />} />
      </Route>
    </Routes>
  )
}

export default App
