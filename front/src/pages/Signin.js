import React, { useEffect, useState } from "react";
import logo from '../assets/logo.jpg';
import robot from '../assets/miroExcited.jpg';
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Signin = () => {
  let nav = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  useEffect(()=>{
    if (localStorage.getItem('token')){
        nav('/home')
    }
  });
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/auth/login', {
        email,
        password,
      });
      console.log("Signup successful:", response.data.access_token);
      localStorage.setItem('token',JSON.stringify(response.data.access_token));
      nav('/home');
    } catch (error) {
      console.error("Signup error:", error);
    }
  };
  return (
    <div className="min-h-screen bg-white">
     
      <nav className="flex items-center justify-between px-8 py-4 border-b border-gray-200">
        <img src={logo} alt="Logo" className="h-10" />
        <ul className="flex items-center space-x-6 text-gray-700 font-medium">
         
          <li>About Us</li>
          <li>Home</li>
          <li>
            <Link to="/signup" className="px-4 py-1 rounded-full border border-cyan-400 text-cyan-400 hover:bg-cyan-50">
              Sign up
            </Link>
          </li>
          <li>
            <Link to="/signin" className="px-4 py-1 bg-cyan-400 text-white rounded-full hover:bg-cyan-500">
              Login
            </Link>
          </li>
        </ul>
      </nav>

    
      <div className="flex flex-col md:flex-row items-center justify-between px-10 py-16">
        
        <img src={robot} alt="Robot" className="w-96 mb-10 md:mb-0" />

       
        <div className="max-w-md w-full space-y-4">
          
          <div className="flex justify-center space-x-4">
            <button className="px-6 py-2 font-bold text-cyan-500 border-2 border-cyan-300 rounded-full shadow-md bg-white">
            <Link to="/login"> Login
            </Link>
            </button>
            <button className="px-6 py-2 font-bold text-gray-400 border border-gray-300 rounded-full shadow-inner">
              <Link to="/signup">Sign Up</Link>
            </button>
          </div>

        
          <div className="space-y-4">
            <div className="flex items-center border border-cyan-300 rounded-full px-4 py-2 shadow-sm">
              
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1 outline-none bg-transparent"
              />
            </div>

            <div className="flex items-center border border-cyan-300 rounded-full px-4 py-2 shadow-sm">
              
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="flex-1 outline-none bg-transparent"
              />
            </div>
          </div>

          
          <p className="text-sm text-gray-400 text-center">Forgot your password ?</p>

          <button className="w-full px-6 py-2 text-white font-bold bg-gradient-to-r from-cyan-400 to-cyan-600 rounded-full shadow-md hover:scale-105 transition" onClick = {handleSubmit}>
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default Signin;
