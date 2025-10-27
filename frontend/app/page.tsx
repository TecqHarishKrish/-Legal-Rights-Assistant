'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Scale, BookOpen, Users, Shield, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: string;
}

interface Source {
  source: string;
  page: number;
  snippet: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const suggestedQuestions = [
    "What are the basic rights of workers in India?",
    "How can I file a consumer complaint?",
    "What is the minimum wage law?",
    "What are my digital privacy rights?"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (question?: string) => {
    const questionText = question || input;
    
    if (!questionText.trim()) return;

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: questionText,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/ask`, {
        question: questionText,
        top_k: 3
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: response.data.timestamp
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      
      const errorMessage: Message = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error while processing your question. Please try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Scale className="w-10 h-10" />
              <div>
                <h1 className="text-3xl font-bold">Legal Rights Education Platform</h1>
                <p className="text-blue-100 text-sm">Empowering Citizens with Legal Knowledge</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Mission Banner */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-center space-x-8 text-sm">
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-primary-600" />
              <span className="text-gray-700">For Students & Citizens</span>
            </div>
            <div className="flex items-center space-x-2">
              <BookOpen className="w-5 h-5 text-primary-600" />
              <span className="text-gray-700">Educational Purpose</span>
            </div>
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-primary-600" />
              <span className="text-gray-700">Know Your Rights</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Disclaimer */}
        {showDisclaimer && (
          <div className="mb-6 bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-orange-400 rounded-xl p-6 shadow-lg animate-fade-in">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-3">
                  <AlertCircle className="w-6 h-6 text-orange-600" />
                  <h3 className="text-lg font-bold text-orange-900">Important Legal Disclaimer</h3>
                </div>
                <div className="text-orange-900 space-y-2">
                  <p className="font-semibold">
                    Educational Purpose Only: This platform provides general legal information to help you understand your rights. 
                    <span className="text-red-700"> It is NOT a substitute for professional legal advice.</span>
                  </p>
                  <p className="text-sm">
                    <strong>Please Note:</strong> Laws and regulations change frequently. The information provided may not be complete, 
                    current, or applicable to your specific situation.
                  </p>
                  <p className="text-sm font-medium">
                    <strong>Action Required:</strong> For specific legal matters, disputes, or advice, always consult with a 
                    qualified legal professional or official authority.
                  </p>
                </div>
              </div>
              <button
                onClick={() => setShowDisclaimer(false)}
                className="ml-4 text-orange-600 hover:text-orange-800 font-semibold"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Chat Messages */}
          <div className="h-[600px] overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <Scale className="w-16 h-16 text-primary-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Welcome to Legal Rights Education</h2>
                <p className="text-gray-600 mb-6">Ask me anything about your legal rights in India</p>
                
                {/* Suggested Questions */}
                <div className="max-w-2xl mx-auto">
                  <p className="text-sm font-semibold text-gray-700 mb-3">💡 Try asking:</p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {suggestedQuestions.map((q, i) => (
                      <button
                        key={i}
                        onClick={() => handleSend(q)}
                        className="bg-gradient-to-r from-primary-50 to-secondary-50 hover:from-primary-100 hover:to-secondary-100 
                                 border-2 border-primary-200 rounded-lg p-3 text-left text-sm font-medium text-gray-700 
                                 transition-all duration-200 hover:shadow-md hover:-translate-y-0.5"
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl p-4 shadow-md ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white'
                      : 'bg-white border-2 border-gray-200 text-gray-800'
                  }`}
                >
                  <div className="flex items-center space-x-2 mb-2">
                    {message.role === 'user' ? (
                      <span className="font-semibold">You</span>
                    ) : (
                      <>
                        <Scale className="w-5 h-5 text-primary-600" />
                        <span className="font-semibold text-primary-700">Legal Assistant</span>
                      </>
                    )}
                  </div>
                  <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                  
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <p className="text-sm font-semibold text-gray-700 mb-2">📚 Sources:</p>
                      <div className="space-y-2">
                        {message.sources.map((source, i) => (
                          <div key={i} className="bg-gray-50 rounded-lg p-3 text-sm">
                            <p className="font-medium text-primary-700">
                              {source.source} (Page {source.page})
                            </p>
                            <p className="text-gray-600 italic mt-1">"{source.snippet}"</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start animate-slide-up">
                <div className="bg-white border-2 border-gray-200 rounded-2xl p-4 shadow-md">
                  <div className="flex items-center space-x-2">
                    <Loader2 className="w-5 h-5 text-primary-600 animate-spin" />
                    <span className="text-gray-600">Analyzing legal documents...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t-2 border-gray-200 p-4 bg-gray-50">
            <div className="flex space-x-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about your legal rights..."
                className="flex-1 px-6 py-3 border-2 border-gray-300 rounded-full focus:outline-none focus:border-primary-500 
                         focus:ring-2 focus:ring-primary-200 transition-all duration-200"
                disabled={isLoading}
              />
              <button
                onClick={() => handleSend()}
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white px-8 py-3 rounded-full 
                         font-semibold hover:shadow-lg transition-all duration-200 disabled:opacity-50 
                         disabled:cursor-not-allowed flex items-center space-x-2"
              >
                <span>Send</span>
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-600">
          <p className="text-sm">
            Legal Rights Education Platform • A Social Welfare Initiative
          </p>
          <p className="text-xs mt-2">
            Built with ❤️ using Next.js, React, FastAPI, and AI
          </p>
        </div>
      </main>
    </div>
  );
}
