import React from 'react'
import AudioPlayer from './AudioPlayer'

const ChatMessage = ({ message, isBot = false }) => {

  return (
    //contains message, changes alignment if bot or user
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4 w-full`} style={{
      marginLeft: isBot ? '0' : '6rem',
      marginRight: isBot ? '8rem' : '0'
    }}>

      {/*inner continer with 80% width*/}
      <div className="flex flex-col" style={{ maxWidth: '80%' }}>

        {/*header row (labels and audio button)*/}
        {/*AudioPlayer button and labels*/}
        <div style={{ 
          display: 'flex',
          alignItems: 'center',
          justifyContent: isBot ? 'flex-start' : 'flex-end',
          //marginBottom: '0.5rem'
        }}>

{/*tú and bot labels*/}
          <p style={{ 
            fontWeight: 'bold',
            textAlign: isBot ? 'left' : 'right',
            paddingLeft: isBot ? '0.8rem' : '0',
            paddingRight: isBot ? '0' : '0.8rem'
          }}>
            {isBot ? 'Bot' : 'Tú'}
          </p>

{/*AudioPlayer button only for the bot*/}
          {isBot && <AudioPlayer isBot={isBot} />}
        </div>

{/*Message bubbles, changes color per bot or user*/}
        <div 
          style={{
            backgroundColor: isBot ? '#3B82F6' : '#10B981',
            padding: '0.5rem',
            borderRadius: '0.8rem',
            color: 'white',
            width: 'fit-content',
            maxWidth: '100%',
            wordBreak: 'break-word'
          }}>
          <p>{message}</p>
        </div>

      </div>

    </div>
  )
}

export default ChatMessage