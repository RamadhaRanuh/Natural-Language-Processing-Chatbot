"use client";

import { useState, useEffect, useRef } from "react";
import { Send, Menu, Search, User, Bot, FileText, Activity, ShieldCheck, ChevronRight, Sparkles, BookOpen } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-focus input on load
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e?: React.FormEvent, customQuery?: string) => {
    e?.preventDefault();
    const text = customQuery || query;
    if (!text.trim() || isLoading) return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setQuery("");
    setIsLoading(true);

    try {
      // Create a placeholder for the assistant message
      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [{ role: "user", content: text }],
        }),
      });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let assistantMessage = "";

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value, { stream: true });
        assistantMessage += chunkValue;

        // Update the last message (assistant)
        setMessages((prev) => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = {
            role: "assistant",
            content: assistantMessage,
          };
          return newMessages;
        });
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: Failed to fetch response. Please ensure the backend server is running." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestions = [
    { text: "What is the normal blood pressure range?", icon: <Activity className="w-5 h-5 text-orange-600" />, label: "Quick Fact" },
    { text: "Does aspirin interact with ibuprofen?", icon: <ShieldCheck className="w-5 h-5 text-orange-600" />, label: "Interaction Check" },
    { text: "Guidelines for treating Type 2 Diabetes?", icon: <BookOpen className="w-5 h-5 text-orange-600" />, label: "Clinical Guidelines" },
  ];

  return (
    <div className="flex h-screen bg-[#F9FAFB] text-gray-900 font-sans antialiased overflow-hidden">
      {/* Sidebar - Desktop */}
      <aside className="w-[280px] border-r border-gray-100 bg-white hidden md:flex flex-col shadow-[2px_0_24px_rgba(0,0,0,0.02)] z-10">
        <div className="p-6 flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-orange-200">OE</div>
          <span className="font-bold text-xl tracking-tight text-gray-900">OpenEvidence</span>
        </div>

        <div className="flex-1 px-4 py-2 space-y-6 overflow-y-auto">
          <div>
            <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-3 mb-3">Library</div>
            <div className="space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-orange-600 bg-orange-50/80 rounded-lg transition-colors">
                <Sparkles className="w-4 h-4" />
                New Conversation
              </button>
              <button className="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                <FileText className="w-4 h-4 text-gray-400" />
                My Sources
              </button>
            </div>
          </div>

          <div>
            <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-3 mb-3">Recent</div>
            <div className="space-y-1">
              <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-500 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors truncate">
                <span>Recent queries...</span>
              </button>
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-gray-100">
          <button className="flex items-center gap-3 w-full p-2 hover:bg-gray-50 rounded-lg transition-colors">
            <div className="w-8 h-8 rounded-full bg-gray-200 border border-white shadow-sm flex items-center justify-center text-gray-500">
              <User className="w-4 h-4" />
            </div>
            <div className="text-left">
              <div className="text-sm font-medium text-gray-900">Medical Professional</div>
              <div className="text-xs text-gray-500">Free Plan</div>
            </div>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full relative">
        {/* Mobile Header */}
        <header className="h-16 border-b border-gray-100 bg-white/80 backdrop-blur-md flex items-center justify-between px-6 md:hidden sticky top-0 z-20">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-orange-600 rounded-lg flex items-center justify-center text-white font-bold text-xs">OE</div>
            <span className="font-bold text-lg text-gray-900">OpenEvidence</span>
          </div>
          <Menu className="w-5 h-5 text-gray-500" />
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto scroll-smooth">
          {messages.length === 0 ? (
            <div className="min-h-full flex flex-col items-center justify-center p-6 md:p-12 pb-32">
              <div className="text-center space-y-6 max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
                <div className="w-16 h-16 bg-orange-100 rounded-2xl flex items-center justify-center mx-auto mb-6 text-orange-600">
                  <Sparkles className="w-8 h-8" />
                </div>
                <h1 className="text-4xl md:text-5xl font-serif font-medium text-gray-900 tracking-tight">
                  Evidence-based answers<br />at the point of care.
                </h1>
                <p className="text-lg text-gray-500 font-light max-w-lg mx-auto">
                  Ask complex medical questions and get answers grounded in trusted peer-reviewed literature.
                </p>
              </div>

              {/* Suggestions */}
              <div className="mt-12 w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-4">
                {suggestions.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => handleSubmit(undefined, s.text)}
                    disabled={isLoading}
                    className="group flex flex-col items-start gap-3 p-5 bg-white border border-gray-200/60 rounded-2xl hover:border-orange-200 hover:shadow-lg hover:shadow-orange-500/5 transition-all text-left"
                  >
                    <div className="w-8 h-8 rounded-full bg-orange-50 flex items-center justify-center group-hover:bg-orange-600 group-hover:text-white transition-colors">
                      {s.icon}
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-orange-600 uppercase tracking-wide mb-1">{s.label}</div>
                      <div className="text-sm font-medium text-gray-900 group-hover:text-orange-900">{s.text}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto py-8 md:py-12 px-4 space-y-10 pb-32">
              {messages.map((msg, i) => (
                <div key={i} className="animate-in fade-in slide-in-from-bottom-2 duration-500">
                  {msg.role === 'user' ? (
                    <div className="flex justify-end mb-8">
                      <div className="bg-gray-100 text-gray-900 px-6 py-4 rounded-3xl rounded-tr-sm max-w-[85%] md:max-w-2xl text-lg leading-relaxed shadow-sm">
                        {msg.content}
                      </div>
                    </div>
                  ) : (
                    <div className="flex gap-4 md:gap-6">
                      <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-gradient-to-br from-orange-500 to-red-500 flex-shrink-0 flex items-center justify-center text-white shadow-md mt-1">
                        <Bot className="w-5 h-5 md:w-6 md:h-6" />
                      </div>
                      <div className="flex-1 min-w-0 space-y-2">
                        <div className="text-sm font-bold text-gray-900 flex items-center gap-2">
                          OpenEvidence AI
                          {isLoading && i === messages.length - 1 && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800 animate-pulse">
                              Thinking...
                            </span>
                          )}
                        </div>
                        <div className="prose prose-lg prose-gray max-w-none prose-p:leading-relaxed prose-headings:font-serif prose-headings:font-medium prose-a:text-orange-600 hover:prose-a:text-orange-700">
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} className="h-4" />
            </div>
          )}
        </div>

        {/* Floating Input Area */}
        <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-white via-white/80 to-transparent pt-10 pb-6 md:pb-8 px-4 z-20">
          <div className="max-w-3xl mx-auto shadow-2xl shadow-gray-200/50 rounded-[2rem] bg-white ring-1 ring-gray-100 relative group overflow-hidden">
            <div className="absolute inset-0 bg-orange-50 opacity-0 group-focus-within:opacity-10 transition-opacity pointer-events-none" />
            <form onSubmit={handleSubmit} className="flex items-end gap-2 p-2 pl-6">
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a medical question..."
                className="flex-1 py-4 bg-transparent border-none focus:ring-0 focus:outline-none text-lg text-gray-900 placeholder:text-gray-400 min-h-[60px]"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!query.trim() || isLoading}
                className="w-12 h-12 bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-full flex items-center justify-center text-white transition-all shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:scale-105 active:scale-95 mb-1 mr-1"
              >
                <Send className="w-5 h-5 ml-0.5" />
              </button>
            </form>
          </div>
          <p className="text-center mt-3 text-xs text-gray-400 font-medium tracking-wide">
            AI generated content can be inaccurate. Always verify with primary sources.
          </p>
        </div>
      </main>
    </div>
  );
}
