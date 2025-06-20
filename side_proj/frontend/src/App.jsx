import { useState } from 'react'
import './App.css'
import ChatMessage from './components/Message'
import RecordingInterface from './components/RecordingInterface'

function App() {
  const [messages, setMessages] = useState([]);

  // update messages when conversation history changes
  //needed because Message has text and isBot
  const updateMessages = (newHistory) => {
    setMessages(newHistory.map(item => ({
      text: item.user,
      isBot: false
    })).concat(newHistory.map(item => ({//convert messages from bot
      text: item.bot,
      isBot: true
    }))));
  };

  //main container that is whole screen, gray bg
  return (
    <div className="min-h-screen bg-gray-100">
      {/*center container with padding*/}
      <div className="container mx-auto p-4">
        {/*white chat card*/}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">
          {/*Title*/}
            Chat en Español
          </h1>
          {/*Message area (verticl space between messages)*/}
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
            <RecordingInterface />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
