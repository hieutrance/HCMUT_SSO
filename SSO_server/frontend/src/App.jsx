import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Login from "./pages/Login";
import Register from "./pages/Register";
import './index.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen min-w-full flex items-center justify-center">
        <Routes>
          <Route path="/authorize" element={<Login />} />
          <Route path="/register" element={<Register />} />
          {/* ... (các Route khác) */}
        </Routes>
      </div>
    </Router>
  );
}


export default App
