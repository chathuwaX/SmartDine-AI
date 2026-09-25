import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Bot, User, Trash2 } from 'lucide-react';
import { chatWithAgent, clearChat } from '../api';

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'ai', content: 'Hello! Welcome to SmartDine Restaurant. 🍽️ How can I help you today?\n\nI can help you with:\n• Browse our menu\n• Food recommendations\n• Calculate order prices\n• Table reservations\n• Restaurant information' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e?.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const result = await chatWithAgent(userMessage);
            setMessages(prev => [...prev, { role: 'ai', content: result.response || 'No response received.' }]);
        } catch (error) {
            const errorMsg = error.response?.data?.detail || error.message || 'Unknown error';
            setMessages(prev => [...prev, { role: 'ai', content: `Sorry, the AI assistant encountered an issue. (${errorMsg})` }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClear = async () => {
        try {
            await clearChat();
        } catch (e) {
            // ignore
        }
        setMessages([
            { role: 'ai', content: 'Chat cleared! How can I help you?' }
        ]);
    };

    return (
        <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-lg border overflow-hidden flex flex-col h-[600px]">
            <div className="bg-orange-600 text-white p-4 font-bold flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Bot /> AI Assistant
                </div>
                <button onClick={handleClear} className="text-white/80 hover:text-white flex items-center gap-1 text-sm" title="Clear chat">
                    <Trash2 size={16} /> Clear
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-blue-600' : 'bg-orange-600'} text-white`}>
                                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                            </div>
                            <div className={`p-3 rounded-2xl ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-gray-800 border shadow-sm rounded-tl-none'}`}>
                                <p className="whitespace-pre-wrap">{msg.content}</p>
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex gap-3 max-w-[80%] flex-row">
                            <div className="w-8 h-8 rounded-full bg-orange-600 text-white flex items-center justify-center shrink-0">
                                <Bot size={16} />
                            </div>
                            <div className="p-3 rounded-2xl bg-white border shadow-sm rounded-tl-none flex items-center gap-2 text-gray-500">
                                <Loader2 className="animate-spin" size={16} />
                                <span className="text-sm">Agent is thinking...</span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSend} className="p-4 bg-white border-t flex gap-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    disabled={isLoading}
                    className="bg-orange-600 text-white p-2 rounded-lg hover:bg-orange-700 disabled:opacity-50 transition"
                >
                    <Send size={20} />
                </button>
            </form>
        </div>
    );
}
