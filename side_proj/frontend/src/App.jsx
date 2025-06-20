import { useState } from 'react'
import './App.css'
import ChatMessage from './components/Message'
import RecordingInterface from './components/RecordingInterface'

function App() {
  const [messages, setMessages] = useState([]);

  // This function will be called by RecordingInterface
  const handleNewMessage = (newMessage) => {
    // Add user message to the chat
    setMessages(prev => [...prev, { text: newMessage.user, isBot: false }]);
    
    // Add bot response to the chat
    setMessages(prev => [...prev, { text: newMessage.bot, isBot: true }]);
  };

  //main container that is whole screen, gray bg
  return (
    <div className="min-h-screen bg-gray-100">
      {/*center container with padding, with extra bottom padding to avoid overlap with fixed recorder */}
      <div className="container mx-auto p-4 pb-40">
        {/*white chat card, takes remaining space, max width*/}
        <div className="bg-white rounded-lg shadow-lg p-6 max-w-xl mx-auto">
          <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">
          {/*Title*/}
            Contigo
          </h1>
          {/*Message area - scrollable, takes remaining space*/}
          <div className="space-y-4">
            {/*Messages rendered here*/}
            {messages.map((msg, index) => (
              <ChatMessage 
                key={index}
                message={msg.text}
                isBot={msg.isBot}
              />
            ))}
          </div>
          {/*recording interface (margin top for separaton)*/}
          <div className="mt-6">
            <RecordingInterface onNewMessage={handleNewMessage} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
