import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Home from "./Home"
import Clips from "./Clips"

export default function App() {
    return (
        <>
            <Router>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/clips" element={<Clips />} />
                </Routes>
            </Router>
        </>
    )
}