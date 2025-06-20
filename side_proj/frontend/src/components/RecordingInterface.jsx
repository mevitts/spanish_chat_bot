import React, { useState, useEffect } from 'react';

const RecordingInterface = ({ onNewMessage }) => {
    const [audioData, setAudioData] = useState(null);
    const [currentTranscription, setCurrentTranscription] = useState('');
    const [transcribedText, setTranscribedText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false); //when audio is processing 
    const [isGenerating, setIsGenerating] = useState(false);
    
    useEffect(() => {
        const processAudio = async () => {
            if (audioData && !isRecording) {  // Only process if we have audioData and recording is stopped
                setIsProcessing(true);
                try {
                    const transcription = await transcribeAudio(audioData);
                    await generateResponse(transcription);
                } catch (error) {
                    console.error('Error processing audio:', error);
                } finally {
                    setIsProcessing(false);
                }
            }
        };
        
        processAudio();
    }, [audioData, isRecording]); //runs when one of these changes

    const recordAudio = async() => {
        try {
            const response = await fetch('/api/start-recording', {
                method: 'POST'
            });
            const { audioData } = await response.json();
            setAudioData(audioData);
            setIsRecording(false);
            return audioData;
        } catch (error) {
            console.error('Error during recording:', error);
        }
    }

    const transcribeAudio = async(audioData) => {
        if (!audioData) {
            console.error('No audio data available for transcription');
            return;
        }
        try {
             // Handle the transcription...'
            const transcriptionResponse = await fetch('/api/transcribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ audioData })
            });
            const { transcription } = await transcriptionResponse.json();
            setCurrentTranscription(transcription);
            return transcription;
        } catch (error) {
            console.error('Error during recording:', error);
        }
    }

    const generateResponse = async(transcription) => {
        try {          
            if (!transcription) {
                console.error('No transcription available for response generation');
                return;
            }
            //get bot response
            setIsGenerating(true);
            const botResponse = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: transcription }) //send transcription to backend
            });
            const { response, audioUrl } = await botResponse.json();//parse json response

            // Send new message up to the parent component
            if (onNewMessage) {
                onNewMessage({
                    user: transcription,
                    bot: response,
                    audioUrl: audioUrl
                });
            }

            //play audio
            const audio = new Audio(audioUrl);
            await audio.play();
            } catch (error) {
                console.error('Error:', error);
            } finally {
                setIsGenerating(false);
            }
    }

    const handleRecordClick = async () => {
        try {
            if(isRecording) {
                //if currently recording and button pressed, stop rec and start processing
                setIsRecording(false);
            } else { 
                //if not recording
                setAudioData(null) //resets audiodata
                setIsRecording(true);
                await recordAudio();
            }
        } catch (error) {
            console.error('Error in recording process:', error);
        } finally {
            setIsProcessing(false);
        }
    }

    return (
        <div className="flex flex-col items-center space-y-3">
            {/* Visualizer Area (status display) - smaller height for bottom layout*/}
            <div className="w-full h-16 bg-gray-100 rounded-lg flex items-center justify-center">
                {/*shows different message depending on stage of process.*/}
                {isRecording ? (
                     <div className="flex flex-col items-center">
                        <p className="text-gray-700 mb-1 text-sm">Grabando...</p>
                        <div className="flex space-x-2">
                            {[...Array(5)].map((_, i) => (
                            <div
                                key={i}
                                className="w-6 bg-blue-500 rounded-full animate-pulse"
                                style={{
                                    height: `${Math.random() * 30 + 15}px`,
                                    animationDelay: `${i * 0.1}s`
                                }}
                            />
                            ))}
                        </div>
                    </div>
                ) : isProcessing ? (
                    <p className="text-gray-700 text-sm">Procesando audio...</p>
                ) : isGenerating ? (
                    <p className="text-gray-700 text-sm">Generando respuesta...</p>
                ) : currentTranscription ? (
                    <p className="text-gray-700 text-sm">{currentTranscription}</p>
                ) : (
                    <p className="text-gray-700 text-sm">Click the record button to start speaking</p>
                )
            }
            </div>

            {/* Record Button */}
            <button
                type="button"
                onClick={handleRecordClick}
                style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '50%',
                    backgroundColor: isRecording ? '#f3f4f6' : '#f3f4f6',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.3s',
                    position: 'relative'
                }}
            >
                {isRecording ? (
                    <div style={{ 
                        width: '20px', 
                        height: '20px', 
                        backgroundColor: 'black', 
                        borderRadius: '30%',
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)'
                    }} />
                ) : (
                    <div style={{ 
                        width: '20px', 
                        height: '20px', 
                        backgroundColor: 'red', 
                        borderRadius: '80%',
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)'
                    }} />
                )}
            </button>
        </div>
    );
};

export default RecordingInterface; 