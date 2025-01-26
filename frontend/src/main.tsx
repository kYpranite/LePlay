import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Home from './Home'
import Clips from './Clips'
import Highlights from './Highlights'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/clips" element={<Clips />} />
        <Route path="/highlights" element={<Highlights />} />

      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
