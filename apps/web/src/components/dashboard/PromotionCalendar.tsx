'use client'

import { useEffect, useState } from 'react'

interface CalendarEvent {
  id: string
  date: string
  type: 'promotion' | 'deadline' | 'event'
  event_type: string
  title: string
  description?: string
  status?: string
  promotion_id?: string
}

interface CalendarResponse {
  timestamp: string
  view: string
  current_month: string
  events: CalendarEvent[]
}

export function PromotionCalendar() {
  const [events, setEvents] = useState<CalendarEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedMonth, setSelectedMonth] = useState('FEB')

  const months = ['FEB', 'MAR', 'APR']
  const monthMap: Record<string, number> = { 'FEB': 2, 'MAR': 3, 'APR': 4 }

  useEffect(() => {
    fetchCalendarEvents()
  }, [])

  const fetchCalendarEvents = async () => {
    try {
      const response = await fetch('/api/dashboard/calendar')
      if (response.ok) {
        const data: CalendarResponse = await response.json()
        setEvents(data.events)
      }
    } catch (error) {
      console.error('Failed to fetch calendar events:', error)
    } finally {
      setLoading(false)
    }
  }

  // Filter events by selected month
  const filteredEvents = events.filter(event => {
    const eventMonth = new Date(event.date).getMonth() + 1
    return eventMonth === monthMap[selectedMonth]
  }).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

  // Calculate timeline progress for each month
  const getMonthProgress = (month: string): number => {
    const monthNum = monthMap[month]
    const monthEvents = events.filter(e => {
      const eventMonth = new Date(e.date).getMonth() + 1
      return eventMonth === monthNum
    })
    // Show some progress based on number of events or scheduled promotions
    const promotionEvents = monthEvents.filter(e => e.type === 'promotion')
    if (monthEvents.length === 0) return 0
    return Math.min(100, promotionEvents.length * 30 + 20)
  }

  const getEventColor = (type: string): string => {
    switch (type) {
      case 'promotion':
        return 'bg-terminal-accent-positive'
      case 'deadline':
        return 'bg-terminal-accent-negative'
      default:
        return 'bg-terminal-text-secondary'
    }
  }

  const formatDate = (dateStr: string): string => {
    return dateStr.slice(5) // Returns MM-DD format
  }

  return (
    <div className="terminal-panel h-full">
      <div className="terminal-panel-header flex items-center justify-between">
        <span>PROMOTION CALENDAR - Q1 2026</span>
        <div className="flex gap-2 text-xs">
          {months.map((month) => (
            <button
              key={month}
              onClick={() => setSelectedMonth(month)}
              className={`px-2 py-0.5 rounded ${
                month === selectedMonth
                  ? 'bg-terminal-text-primary text-black'
                  : 'text-terminal-text-muted hover:text-white'
              }`}
            >
              {month}
            </button>
          ))}
        </div>
      </div>
      <div className="terminal-panel-content flex gap-4 overflow-x-auto">
        {/* Timeline visualization */}
        <div className="flex-1">
          {months.map((month) => (
            <div key={month} className="flex items-center gap-2 mb-3">
              <span className="text-xs text-terminal-text-muted w-16">{month}</span>
              <div className="flex-1 h-4 bg-terminal-bg-tertiary rounded overflow-hidden">
                <div
                  className={`h-full rounded transition-all duration-300 ${
                    month === selectedMonth
                      ? 'bg-terminal-accent-positive/70'
                      : 'bg-terminal-text-secondary/30'
                  }`}
                  style={{ width: `${getMonthProgress(month)}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Events list */}
        <div className="w-72 space-y-2 max-h-32 overflow-y-auto">
          {loading ? (
            <div className="text-xs text-terminal-text-muted">Loading events...</div>
          ) : filteredEvents.length === 0 ? (
            <div className="text-xs text-terminal-text-muted">No events for {selectedMonth}</div>
          ) : (
            filteredEvents.map((event) => (
              <div key={event.id} className="flex items-center gap-2 text-xs">
                <span className={`w-2 h-2 rounded-full ${getEventColor(event.type)}`} />
                <span className="text-terminal-text-muted w-16">{formatDate(event.date)}</span>
                <span className="text-white truncate flex-1" title={event.title}>
                  {event.title}
                </span>
                {event.status && (
                  <span className={`text-[10px] px-1 rounded ${
                    event.status === 'scheduled'
                      ? 'bg-terminal-accent-positive/20 text-terminal-accent-positive'
                      : event.status === 'draft'
                      ? 'bg-terminal-text-secondary/20 text-terminal-text-secondary'
                      : 'bg-terminal-text-primary/20 text-terminal-text-primary'
                  }`}>
                    {event.status}
                  </span>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
