'use client'

import { useState, useRef, useEffect } from 'react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  divisions?: string[]
  timestamp: Date
}

interface DivisionBadgeProps {
  division: string
}

function DivisionBadge({ division }: DivisionBadgeProps) {
  const colorMap: Record<string, string> = {
    strategic_planning: 'agent-badge-strategic',
    market_intelligence: 'agent-badge-market',
    channel_management: 'agent-badge-channel',
    analytics: 'agent-badge-analytics',
    operations: 'agent-badge-operations',
  }

  const labelMap: Record<string, string> = {
    strategic_planning: 'Strategic',
    market_intelligence: 'Market',
    channel_management: 'Channel',
    analytics: 'Analytics',
    operations: 'Operations',
  }

  return (
    <span className={`agent-badge ${colorMap[division] || 'bg-gray-700 text-gray-300'}`}>
      {labelMap[division] || division}
    </span>
  )
}

export function AgentChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Welcome to PROMOTOR. How can I assist you with your promotion management today?',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          user_id: 'default_user',
          brand_id: 'default_brand',
        }),
      })

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message || 'Request processed.',
        divisions: data.divisions_used,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      // Simulated response for demo
      const simulatedResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I've analyzed your request about "${userMessage.content}". Here's what I found:\n\n• Peak demand expected in Week 18-22\n• Recommended promotions: 3 flash sales\n• Budget allocation: See detailed breakdown\n• Competitor activity: High in this period`,
        divisions: ['strategic_planning', 'market_intelligence', 'analytics'],
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, simulatedResponse])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">
        AI ASSISTANT
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-3 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`${message.role === 'user' ? 'text-right' : ''}`}>
            {message.role === 'user' ? (
              <div className="inline-block bg-terminal-bg-tertiary rounded px-3 py-2 max-w-[80%]">
                <div className="text-terminal-text-secondary text-sm">{'>'} {message.content}</div>
              </div>
            ) : (
              <div>
                {message.divisions && message.divisions.length > 0 && (
                  <div className="flex items-center gap-1 mb-2">
                    <span className="text-terminal-text-muted text-xs">Processing with:</span>
                    {message.divisions.map((div) => (
                      <DivisionBadge key={div} division={div} />
                    ))}
                  </div>
                )}
                <div className="bg-terminal-bg-secondary rounded px-3 py-2 border border-terminal-border">
                  <div className="text-sm text-white whitespace-pre-wrap">{message.content}</div>
                </div>
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-terminal-text-muted">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-terminal-text-primary rounded-full animate-pulse" />
              <span className="w-2 h-2 bg-terminal-text-primary rounded-full animate-pulse delay-100" />
              <span className="w-2 h-2 bg-terminal-text-primary rounded-full animate-pulse delay-200" />
            </div>
            <span className="text-xs">Processing across divisions...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-3 border-t border-terminal-border">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <span className="text-terminal-text-primary">{'>'}</span>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about promotions, analytics, channels..."
            className="flex-1 bg-transparent text-white placeholder-terminal-text-muted focus:outline-none text-sm"
            disabled={isLoading}
          />
          {input && <span className="terminal-cursor" />}
        </form>
      </div>
    </div>
  )
}
