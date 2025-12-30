import React, { useState } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import '../App.css';

const ChatWidget = ({ globalContextCountry }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [input, setInput] = useState("");
    const [history, setHistory] = useState([
        { sender: "bot", text: "Hi! I'm your travel assistant. Ask me anything about local customs!" }
    ]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setHistory((prev) => [...prev, { sender: "user", text: userMsg }]);
        setInput("");
        setLoading(true);

        const contextToSend = globalContextCountry || "General";

        try {
            const payload = {
                message: userMsg,
                country: contextToSend
            };

            const res = await fetch("http://127.0.0.1:8000/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            setHistory((prev) => [...prev, { sender: "bot", text: data.response }]);
        } catch (err) {
            setHistory((prev) => [...prev, { sender: "bot", text: "Sorry, I had trouble reaching the server." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {!isOpen && (
                <button className="chat-fab" onClick={() => setIsOpen(true)}>
                    <MessageCircle size={28} />
                </button>
            )}

            {isOpen && (
                <div className="chat-panel">
                    <div className="chat-panel-header">
                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                            <MessageCircle size={20} />
                            <span>Geo Assistant</span>
                        </div>
                        <button className="close-btn" onClick={() => setIsOpen(false)}>
                            <X size={20} />
                        </button>
                    </div>

                    <div className="chat-body">
                        {history.map((msg, i) => (
                            <div key={i} className={`chat-bubble ${msg.sender}`}>
                                {msg.text.split('\n').map((line, idx) => (
                                    <div key={idx} style={{ minHeight: line.trim() ? 'auto' : '0.5rem' }}>
                                        {line.split(/(\*\*.*?\*\*)/).map((part, pIdx) =>
                                            part.startsWith('**') && part.endsWith('**') ?
                                                <strong key={pIdx}>{part.slice(2, -2)}</strong> :
                                                part
                                        )}
                                    </div>
                                ))}
                            </div>
                        ))}
                        {loading && <div className="chat-bubble bot">Thinking...</div>}
                    </div>

                    <form className="chat-footer" onSubmit={handleSubmit}>
                        <input
                            className="chat-input"
                            placeholder="Ask me something..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <button type="submit" className="send-btn">
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            )}
        </>
    );
};

export default ChatWidget;
