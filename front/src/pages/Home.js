import React, { useEffect, useRef, useState } from "react";
import logo from "../assets/logo.jpg";
import robot from "../assets/mirou.jpg";
import ChatInput from "../components/ChatInput.js";
import { useNavigate } from "react-router-dom";
import { Link } from "lucide-react";
import axios from "axios";

let token = JSON.parse(localStorage.getItem('token'));

const HomeScreen = () => {
  let nav = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      nav('/login');
    }
  }, []);

  const [showHistory, setShowHistory] = useState(false);
  const [historyItems, setHistoryItems] = useState([]);
  const [chatId, setChatId] = useState(null);

  const chatDisplayRef = useRef(null);

  const handleAppendMessage = (text, sender = 'user') => {
    if (!chatDisplayRef.current) return;
  
    const msgDiv = document.createElement('div');
    msgDiv.className = `max-w-xs px-4 py-2 rounded-xl text-sm my-1 ${
      sender === 'user'
        ? 'self-end bg-cyan-400 text-white'
        : 'self-start bg-gray-200 text-gray-800'
    }`;
    msgDiv.innerText = text;
  
    chatDisplayRef.current.appendChild(msgDiv);
  
    setTimeout(() => {
      chatDisplayRef.current.scrollTop = chatDisplayRef.current.scrollHeight;
    }, 0);
  };
  

  const fetchHistory = async () => {
    try {
      const response = await axios.get('http://localhost:8000/ai/chats', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log(response.data[0].id);
      setHistoryItems(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const fetchChats = async (id) => {
    try {
      setChatId(id);
      console.log(id);
      if (chatDisplayRef.current) {
        chatDisplayRef.current.innerHTML = ''; // Clear existing messages
      }

      const response = await axios.get(`http://localhost:8000/ai/chats/${id}`,{
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log(response.data);
      for (let msg of response.data) {
        handleAppendMessage(msg.content, msg.sender);
      }
    } catch (error) {
      console.error('Error fetching chat:', error);
    }
  };

  const toggleHistory = () => {
    setShowHistory(prev => !prev);
    fetchHistory();
  };

  return (
    <div className="min-h-screen bg-white">
      <nav className="relative flex items-center justify-between px-8 py-4 border-b border-gray-200">
        <img src={logo} alt="Logo" className="h-10" />
        <ul className="flex items-center space-x-6 text-gray-700 font-medium relative">
          <li className="relative">
            <button onClick={toggleHistory} className="hover:text-blue-600 transition">
              History
            </button>
            {showHistory && (
              <div className="absolute top-full left-0 mt-2 w-64 bg-white border border-gray-200 rounded shadow-lg z-10">
                <ul className="divide-y divide-gray-100 max-h-60 overflow-y-auto">
                  {historyItems.length === 0 ? (
                    <li className="px-4 py-2 text-sm text-gray-500">No history found.</li>
                  ) : (
                    historyItems.map((item) => (
                      <li
                        key={item.id}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-sm"
                        onClick={() => fetchChats(item.id)}
                      >
                        {`Chat #${item.id}`}
                      </li>
                    ))
                  )}
                </ul>
              </div>
            )}
          </li>
          
          <li>become premium</li>
          <li>About Us</li>
          <li className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-red-400"></div>
            <span className="text-sm font-semibold">Ouahab Islam</span>
          </li>
        </ul>
      </nav>

      <div className="flex flex-col md:flex-row items-center justify-between px-10 py-16">
        <img src={robot} alt="Robot" className="w-96 mb-10 md:mb-0" />
        <div className="w-full max-w-xl">
  <div
    ref={chatDisplayRef}
    style={{
      maxWidth: '56rem',
      margin: '0 auto',
      padding: '1rem',
      paddingBottom: '6rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem',
      maxHeight: 'calc(100vh - 6rem)',
      overflowY: 'auto'
    }}
  />
  <ChatInput
    chatDisplayRef={chatDisplayRef}
    chatId={chatId}
    setChatId={setChatId}
    appendMessage={handleAppendMessage}
  />
</div>

      </div>

      <div className="flex justify-center py-6">
        <button className="flex items-center gap-2 px-6 py-2 text-sm font-semibold text-gray-600 border border-gray-300 rounded-full hover:shadow-md">
          ✦ Upgrade To Premium
        </button>
      </div>
    </div>
  );
};

export default HomeScreen;
