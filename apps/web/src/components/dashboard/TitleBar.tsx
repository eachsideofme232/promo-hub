'use client'

import { useState, useEffect } from 'react'

export function TitleBar() {
  const [currentTime, setCurrentTime] = useState<string>('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setCurrentTime(now.toLocaleString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      }))
    }

    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="h-8 bg-terminal-bg-secondary border-b border-terminal-border flex items-center justify-between px-4">
      <div className="flex items-center gap-4">
        <span className="text-terminal-text-primary font-bold text-sm">
          PROMOTOR
        </span>
        <span className="text-terminal-text-muted text-xs">
          Beauty Brand Promotion Manager
        </span>
      </div>

      <div className="flex items-center gap-4">
        <span className="text-terminal-text-secondary text-xs">
          {currentTime}
        </span>
        <div className="flex items-center gap-2">
          <button className="text-terminal-text-muted hover:text-white text-xs">━</button>
          <button className="text-terminal-text-muted hover:text-white text-xs">□</button>
          <button className="text-terminal-text-muted hover:text-terminal-accent-negative text-xs">✕</button>
        </div>
      </div>
    </div>
  )
}
