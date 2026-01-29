'use client'

import { useEffect } from 'react'

interface FunctionKeyBarProps {
  activePanel: string
  onPanelChange: (panel: string) => void
}

// Use number keys 1-8 instead of F1-F8 (F-keys are reserved by browsers)
const functionKeys = [
  { key: '1', label: 'Help', panel: 'help' },
  { key: '2', label: 'Calendar', panel: 'calendar' },
  { key: '3', label: 'Analytics', panel: 'analytics' },
  { key: '4', label: 'Channels', panel: 'channels' },
  { key: '5', label: 'Inventory', panel: 'inventory' },
  { key: '6', label: 'Budget', panel: 'budget' },
  { key: '7', label: 'Competitors', panel: 'competitors' },
  { key: '8', label: 'Settings', panel: 'settings' },
]

export function FunctionKeyBar({ activePanel, onPanelChange }: FunctionKeyBarProps) {
  // Handle keyboard shortcuts (Alt + number key)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Only trigger with Alt key to avoid conflicts with typing
      if (!e.altKey) return

      const fk = functionKeys.find((f) => f.key === e.key)
      if (fk) {
        e.preventDefault()
        onPanelChange(fk.panel)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onPanelChange])

  return (
    <div className="h-8 bg-terminal-bg-secondary border-t border-terminal-border flex items-center px-2 gap-1">
      {functionKeys.map((fk) => (
        <button
          key={fk.key}
          onClick={() => onPanelChange(fk.panel)}
          className={`function-key rounded ${
            activePanel === fk.panel ? 'bg-terminal-text-primary text-black' : ''
          }`}
        >
          <span className="text-terminal-text-primary mr-1">[Alt+{fk.key}]</span>
          <span>{fk.label}</span>
        </button>
      ))}

      <div className="flex-1" />

      <div className="flex items-center gap-2 text-xs text-terminal-text-muted">
        <span>21 Agents</span>
        <span>|</span>
        <span>5 Divisions</span>
        <span>|</span>
        <span className="text-terminal-accent-positive">System Ready</span>
      </div>
    </div>
  )
}
