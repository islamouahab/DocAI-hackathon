import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.jpg";
import robot from "../assets/mirou.jpg";
const Welcome = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-4 border-b border-gray-200">
        <img src={logo} alt="Logo" className="h-10" />
        <ul className="flex items-center space-x-6 text-gray-700 font-medium">
          <li>Home</li>
          <li>About Us</li>
          <li>Service</li>
          <li>
            <Link to="/signin" className="px-4 py-1 border border-cyan-400 rounded-full text-cyan-400 hover:bg-cyan-50">
              LogIn
            </Link>
          </li>
          <li>
            <Link to="/signup" className="px-4 py-1 bg-cyan-400 text-white rounded-full hover:bg-cyan-500">
              SignUp
            </Link>
          </li>
        </ul>
      </nav>

      {/* Hero */}
      <div className="flex flex-col md:flex-row items-center justify-between px-8 py-16">
        <img src={robot} alt="Robot Assistant" className="w-80 mb-8 md:mb-0" />
        <div className="max-w-md text-center md:text-left">
          <p className="text-xl font-medium mb-2">Hi there!</p>
          <p className="text-2xl font-semibold">
            I'm <span className="text-cyan-600">Dr. Miro</span>, your health care assistant at your service . . .
          </p>
          <button className="mt-6 px-6 py-2 text-white bg-gradient-to-r from-cyan-400 to-cyan-600 rounded-full shadow-lg hover:scale-105 transition">
            <Link to="/home">Get Started</Link>
            
          </button>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
