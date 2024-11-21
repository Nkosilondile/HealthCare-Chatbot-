// src/Chatbot.js
import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css'; // Import your CSS file

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [buttons, setButtons] = useState([]);
    const [options, setOptions] = useState([]); // State for options list
    const [previousMessage, setPreviousMessage] = useState(''); // Track previous message
    const chatWindowRef = useRef(null); // Create a ref for the chat window

    useEffect(() => {
        // Automatically greet the user when the component mounts
        sendMessage("Hey");
    }, []);

    useEffect(() => {
        // Scroll to the bottom of the chat window whenever messages update
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages]); // Run this effect whenever messages change

    const sendMessage = async (message) => {
        if (!message.trim()) return; // Prevent sending empty messages

        const newMessages = [...messages, { sender: 'user', text: message }];
        setMessages(newMessages);
        setPreviousMessage(message); // Track the message to provide context

        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, previous_message: previousMessage }),
        });

        const data = await response.json();
        setMessages(prevMessages => [
            ...prevMessages,
            { sender: 'bot', text: data.response }
        ]);

        // Set buttons if they exist in the response
        if (data.buttons) {
            setButtons(data.buttons);
        } else {
            setButtons([]);
        }

        // Set options if they exist in the response
        if (data.options) {
            setOptions(data.options);
        } else {
            setOptions([]);
        }

        // Clear the input field after sending the message
        setInput('');
    };

    const handleButtonClick = (buttonValue) => {
        sendMessage(buttonValue);
    };

    const handleOptionClick = (optionValue) => {
        sendMessage(optionValue);
    };

    const clearChat = () => {
        setMessages([]);
        setButtons([]);
        setOptions([]); // Clear options as well
    };

    return (
        <div className="chatbot-container">
            <div className="chat-header">
                <h2>Health Chatbot</h2>
            </div>
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        <div className={`message-bubble ${msg.sender}`}>
                            <strong>{msg.sender === 'bot' ? 'Bot' : 'You'}:</strong> {msg.text}
                        </div>
                    </div>
                ))}
                {options.length > 0 && (
                    <ul className="options-list">
                        {options.map((option, index) => (
                            <li key={index} onClick={() => handleOptionClick(option.value)}>
                                {option.text}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage(input)}
                    placeholder="Talk to Assistant or Chatbot"
                />
                <button className="send-button" onClick={() => sendMessage(input)}>
                    Send
                </button>
                <button className="clear-button" onClick={clearChat}>
                    Clear
                </button>
            </div>
            {buttons.length > 0 && (
                <div className="button-container">
                    {buttons.map((button, index) => (
                        <button 
                            key={index} 
                            className="quick-response-button"
                            onClick={() => handleButtonClick(button.value)}
                        >
                            {button.text}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Chatbot;