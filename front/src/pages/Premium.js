import React, { useEffect, useRef, useState } from "react";
import logo from "../assets/logo.jpg";
import robot from "../assets/mirou.jpg";
const Premium = ()=>{
    return (
    <div>
    <nav className="relative flex items-center justify-between px-8 py-4 border-b border-gray-200">
    <img src={logo} alt="Logo" className="h-10" />
    <ul className="flex items-center space-x-6 text-gray-700 font-medium">
      <li>
        <button className="hover:text-blue-600 transition">History</button>
      </li>
      <li>About Us</li>
      <li className="flex items-center space-x-2">
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-red-400"></div>
        <span className="text-sm font-semibold">Ouahab Islam</span>
      </li>
    </ul>
  </nav>
  <div class="plan">
          <div class="inner">
              <span class="pricing">
                  <span>
                      $49 <small>/ m</small>
                  </span>
              </span>
              <p class="title">Professional</p>
              <p class = "description">for those who want thier mirou to remember them</p>
              <p></p>
              <ul class="features">
                  <li>
                      <span class="icon">
                          <svg height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path d="M0 0h24v24H0z" fill="none"></path>
                              <path fill="currentColor" d="M10 15.172l9.192-9.193 1.415 1.414L10 18l-6.364-6.364 1.414-1.414z"></path>
                          </svg>
                      </span>
                      <span><strong>free images</strong> attatchement</span>
                  </li>
                  <li>
                      <span class="icon">
                          <svg height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path d="M0 0h24v24H0z" fill="none"></path>
                              <path fill="currentColor" d="M10 15.172l9.192-9.193 1.415 1.414L10 18l-6.364-6.364 1.414-1.414z"></path>
                          </svg>
                      </span>
                      <span>Strong recognition<strong>by mirou</strong></span>
                  </li>
                  <li>
                      <span class="icon">
                          <svg height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path d="M0 0h24v24H0z" fill="none"></path>
                              <path fill="currentColor" d="M10 15.172l9.192-9.193 1.415 1.414L10 18l-6.364-6.364 1.414-1.414z"></path>
                          </svg>
                      </span>
                      <span>File sharing</span>
                  </li>
              </ul>
              <div class="action">
              <a class="button" href="#">
                  Choose plan
              </a>
              </div>
          </div>
      </div>
      </div>
);
}
export default Premium;