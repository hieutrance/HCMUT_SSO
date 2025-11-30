import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Login from "./pages/Login";
import Register from "./pages/Register";
import LogoutPage from './pages/Logout';
import './index.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen min-w-full flex items-center justify-center">
        <Routes>
          <Route path="/authorize" element={<Register />} />
          <Route path="/logout" element={<LogoutPage />} />
        </Routes>
      </div>
    </Router>
  );
}


export default App
