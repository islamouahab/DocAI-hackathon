
import { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Smile, X } from 'lucide-react';
import axios from "axios";

export default function ChatInput({ chatId, setChatId, chatDisplayRef, appendMessage }) {
    let token = JSON.parse(localStorage.getItem('token'));
  const [message, setMessage] = useState('');
  const [images, setImages] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const [isPremium , setIsPremium] = useState(false);
  useEffect(() => {
    const checkIsPremium = async () => {
      try {
        const response = await axios.get(`http://192.168.221.6:8000/api/is_premium`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
  
        console.log(response.data.is_premium);
  
        if (response.data.is_premium === true) {
          setIsPremium(true);
        } else {
          setIsPremium(false);
        }
      } catch (error) {
        console.error("Error checking premium status:", error);
      }
    };
  
    checkIsPremium();
  }, []);
  
  

  const handleSubmit = async () => {
    const token = JSON.parse(localStorage.getItem('token'));
    if (!message && images.length === 0) return;
  
    appendMessage(message, 'user');
   
    const formData = new FormData();
      if(chatId==null){
    formData.append('chat_id', 0);
      }
      else{
          formData.append('chat_id',chatId);
      }
    formData.append('prompt', message);
    images.forEach((image) => {
        formData.append('image', image);
        appendMessage(`${image.name}`,'user');// same key for all files
      });
      
    
    try {
      setIsSending(true);
      const response = await axios.post(
        'http://192.168.221.6:8000/ai/generate',
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type':'multipart/form-data'
            
          },
        }
      );
  
      const data = response.data;
      console.log(data)
      setChatId(data.chat_id);
      appendMessage(data.generated_text, 'ai');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsSending(false);
      setMessage('');
      setImages([]);
    }
  };
  

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const imageFiles = selectedFiles.filter(file => file.type.startsWith('image/'));
    if (imageFiles.length > 0) {
      setImages(prev => [...prev, ...imageFiles]);
      e.target.value = '';
    }
  };

  const removeImage = (index) => {
    setImages(prevImages => prevImages.filter((_, i) => i !== index));
  };

  return (
    <>
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
      {/* everything below untouched */}
      <div style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'white',
        borderTop: '1px solid #E5E7EB',
        boxShadow: '0 -4px 6px -1px rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{ maxWidth: '56rem', margin: '0 auto', padding: '0.75rem 1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {images.length > 0 && (
              <div style={{
                padding: '0.75rem',
                backgroundColor: '#F9FAFB',
                borderTopLeftRadius: '0.375rem',
                borderTopRightRadius: '0.375rem',
                border: '1px solid #E5E7EB',
                borderBottom: 'none',
                display: 'flex',
                flexWrap: 'wrap',
                gap: '0.5rem'
              }}>
                {images.map((image, index) => (
                  <div key={index} style={{ position: 'relative' }}>
                    <div style={{
                      height: '5rem',
                      width: '5rem',
                      borderRadius: '0.25rem',
                      overflow: 'hidden',
                      backgroundColor: '#F3F4F6'
                    }}>
                      <img 
                        src={URL.createObjectURL(image)} 
                        alt={`Preview ${index + 1}`} 
                        style={{
                          height: '100%',
                          width: '100%',
                          objectFit: 'cover'
                        }}
                      />
                    </div>
                    <button 
                      onClick={() => removeImage(index)}
                      style={{
                        position: 'absolute',
                        top: '-0.5rem',
                        right: '-0.5rem',
                        backgroundColor: '#EF4444',
                        color: 'white',
                        borderRadius: '9999px',
                        padding: '0.25rem',
                        opacity: 0.8,
                        cursor: 'pointer',
                        border: 'none'
                      }}
                      onMouseOver={(e) => e.currentTarget.style.opacity = '1'}
                      onMouseOut={(e) => e.currentTarget.style.opacity = '0.8'}
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '1px solid #E5E7EB',
              borderRadius: images.length > 0 ? '0 0 0.375rem 0.375rem' : '0.375rem',
              overflow: 'hidden',
              backgroundColor: 'white'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', paddingLeft: '0.5rem', gap: '0.25rem' }}>
                <div style={{ position: 'relative' }}>
                {isPremium && (
  <>
    <button 
      onClick={() => document.getElementById('image-upload').click()}
      type="button"
      style={{
        padding: '0.5rem',
        borderRadius: '9999px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#6B7280',
        cursor: 'pointer',
        backgroundColor: 'transparent',
        border: 'none'
      }}
    >
      <Paperclip size={18} />
    </button>
    <input
      type="file"
      id="image-upload"
      accept="image/*"
      multiple
      style={{ display: 'none' }}
      onChange={handleFileChange}
    />
  </>
)}

                </div>

                <button
                  type="button"
                  style={{
                    padding: '0.5rem',
                    borderRadius: '9999px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#6B7280',
                    cursor: 'pointer',
                    backgroundColor: 'transparent',
                    border: 'none'
                  }}
                >
                  <Smile size={18} />
                </button>
              </div>

              <div style={{ flexGrow: 1, position: 'relative' }}>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type a message..."
                  style={{
                    width: '100%',
                    padding: '0.75rem 1rem',
                    backgroundColor: '#F9FAFB',
                    border: 'none',
                    outline: 'none',
                    resize: 'none',
                    overflow: 'auto',
                    minHeight: '20px'
                  }}
                  rows={1}
                  onKeyDown={handleKeyDown}
                />
              </div>

              <div style={{ display: 'flex', alignItems: 'center', paddingRight: '0.5rem' }}>
                <button
                  onClick={handleSubmit}
                  disabled={!message.trim() && images.length === 0}
                  type="button"
                  style={{
                    padding: '0.5rem',
                    borderRadius: '9999px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: (!message.trim() && images.length === 0) ? '#D1D5DB' : '#6B7280',
                    cursor: (!message.trim() && images.length === 0) ? 'not-allowed' : 'pointer',
                    backgroundColor: 'transparent',
                    border: 'none'
                  }}
                >
                  <Send size={18} />
                </button>
              </div>
            </div>
          </div>

          <div style={{
            fontSize: '0.75rem',
            color: '#9CA3AF',
            marginTop: '0.25rem',
            textAlign: 'center'
          }}>
            {images.length > 0 ? `${images.length} image(s) selected · ` : ''}
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </>
  );
}
