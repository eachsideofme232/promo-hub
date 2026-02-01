'use client'

interface Alert {
  id: string
  severity: 'critical' | 'warning' | 'info'
  title: string
  channel?: string
}

const alerts: Alert[] = []

export function AlertsPanel() {
  return (
    <div className="terminal-panel flex-1">
      <div className="terminal-panel-header flex items-center justify-between">
        <span>ALERTS</span>
        <span className="text-terminal-accent-negative text-xs">{alerts.length}</span>
      </div>
      <div className="terminal-panel-content">
        <div className="space-y-2">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-2 rounded text-xs border-l-2 ${
                alert.severity === 'critical' ? 'bg-red-900/20 border-terminal-accent-negative' :
                alert.severity === 'warning' ? 'bg-yellow-900/20 border-terminal-accent-warning' :
                'bg-blue-900/20 border-terminal-accent-info'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-white">{alert.title}</span>
                {alert.channel && (
                  <span className="text-terminal-text-muted uppercase text-[10px]">
                    {alert.channel}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
