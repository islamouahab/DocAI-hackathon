import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Signup from './pages/SignUp.js';
import Signin from './pages/Signin.js';
import Welcome from './pages/Welcome.js';
import Home from "./pages/Home.js";
import Chat from "./pages/Chat.js";
import Premium from './pages/Premium.js';


function App() {
  return (
    <Router>
      <Routes>
      <Route path="/home" element={<Home />} />
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/chat/:id" element={<Chat />} />
        <Route path="/premium" element={<Premium />} />
      </Routes>
    </Router>
  );
}

export default App;