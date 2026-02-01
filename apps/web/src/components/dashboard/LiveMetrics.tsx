'use client'

interface Metric {
  label: string
  value: string
  change?: number
  changeLabel?: string
}

const metrics: Metric[] = [
  { label: 'Sales (7D)', value: '₩0', change: 0, changeLabel: 'vs last week' },
  { label: 'Active Promos', value: '0', change: 0 },
  { label: 'Alerts', value: '0', change: 0 },
]

export function LiveMetrics() {
  return (
    <div className="terminal-panel">
      <div className="terminal-panel-header">
        LIVE METRICS
      </div>
      <div className="terminal-panel-content">
        <div className="space-y-3">
          {metrics.map((metric) => (
            <div key={metric.label}>
              <div className="data-label">{metric.label}</div>
              <div className="flex items-baseline gap-2">
                <span className="data-value">{metric.value}</span>
                {metric.change !== undefined && (
                  <span className={`text-xs ${
                    metric.change > 0 ? 'data-value-positive' :
                    metric.change < 0 ? 'data-value-negative' :
                    'text-terminal-text-muted'
                  }`}>
                    {metric.change > 0 ? '+' : ''}{metric.change}%
                  </span>
                )}
              </div>
              {metric.changeLabel && (
                <div className="text-xs text-terminal-text-muted">{metric.changeLabel}</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
