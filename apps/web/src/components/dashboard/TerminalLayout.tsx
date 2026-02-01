'use client'

import { useState } from 'react'
import { ChannelStatus } from './ChannelStatus'
import { LiveMetrics } from './LiveMetrics'
import { AgentChat } from './AgentChat'
import { AlertsPanel } from './AlertsPanel'
import { PromotionCalendar } from './PromotionCalendar'
import { FunctionKeyBar } from './FunctionKeyBar'
import { TitleBar } from './TitleBar'

// Placeholder panels for different views
function HelpPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">HELP</div>
      <div className="flex-1 p-4 text-sm text-terminal-text-muted overflow-y-auto">
        <h3 className="text-terminal-text-primary mb-4">PROMOTOR - Beauty Brand Promotion Manager</h3>
        <div className="space-y-3">
          <div>
            <span className="text-terminal-text-secondary">[F1]</span> Help - Show this help screen
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F2]</span> Calendar - View promotion calendar
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F3]</span> Analytics - Performance analytics dashboard
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F4]</span> Channels - Channel management (Oliveyoung, Coupang, Naver, Kakao)
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F5]</span> Inventory - Stock monitoring and alerts
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F6]</span> Budget - Budget allocation and tracking
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F7]</span> Competitors - Competitive intelligence
          </div>
          <div>
            <span className="text-terminal-text-secondary">[F8]</span> Settings - System configuration
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-terminal-border">
          <p className="text-terminal-text-primary mb-2">AI Assistant Commands:</p>
          <div className="space-y-1 text-xs">
            <div>&quot;Plan Q2 sunscreen promotions&quot;</div>
            <div>&quot;Check competitor prices&quot;</div>
            <div>&quot;Analyze last month&apos;s performance&quot;</div>
            <div>&quot;Show inventory alerts&quot;</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function AnalyticsPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">ANALYTICS DASHBOARD</div>
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-terminal-bg-tertiary p-3 rounded">
            <div className="text-terminal-text-muted text-xs mb-1">TOTAL REVENUE (MTD)</div>
            <div className="text-2xl font-bold text-terminal-accent-positive">₩124.5M</div>
            <div className="text-xs text-terminal-accent-positive">+12.3% vs last month</div>
          </div>
          <div className="bg-terminal-bg-tertiary p-3 rounded">
            <div className="text-terminal-text-muted text-xs mb-1">CONVERSION RATE</div>
            <div className="text-2xl font-bold text-terminal-text-secondary">4.2%</div>
            <div className="text-xs text-terminal-accent-positive">+0.8% vs last month</div>
          </div>
          <div className="bg-terminal-bg-tertiary p-3 rounded">
            <div className="text-terminal-text-muted text-xs mb-1">AVG ORDER VALUE</div>
            <div className="text-2xl font-bold text-white">₩45,200</div>
            <div className="text-xs text-terminal-accent-negative">-2.1% vs last month</div>
          </div>
          <div className="bg-terminal-bg-tertiary p-3 rounded">
            <div className="text-terminal-text-muted text-xs mb-1">ACTIVE PROMOTIONS</div>
            <div className="text-2xl font-bold text-terminal-text-primary">7</div>
            <div className="text-xs text-terminal-text-muted">across 4 channels</div>
          </div>
        </div>
        <div className="bg-terminal-bg-tertiary p-3 rounded">
          <div className="text-terminal-text-primary text-sm mb-2">Channel Performance</div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between items-center">
              <span className="text-terminal-text-muted">Oliveyoung</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-terminal-bg-secondary rounded overflow-hidden">
                  <div className="h-full bg-terminal-accent-positive" style={{width: '75%'}}></div>
                </div>
                <span className="text-terminal-accent-positive">₩52.3M</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-terminal-text-muted">Coupang</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-terminal-bg-secondary rounded overflow-hidden">
                  <div className="h-full bg-terminal-text-secondary" style={{width: '60%'}}></div>
                </div>
                <span className="text-terminal-text-secondary">₩38.1M</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-terminal-text-muted">Naver</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-terminal-bg-secondary rounded overflow-hidden">
                  <div className="h-full bg-terminal-text-primary" style={{width: '45%'}}></div>
                </div>
                <span className="text-terminal-text-primary">₩24.8M</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-terminal-text-muted">Kakao</span>
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-terminal-bg-secondary rounded overflow-hidden">
                  <div className="h-full bg-terminal-accent-warning" style={{width: '20%'}}></div>
                </div>
                <span className="text-terminal-accent-warning">₩9.3M</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function ChannelsPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">CHANNEL MANAGEMENT</div>
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-4">
          {[
            { name: 'Oliveyoung', status: 'online', listings: 156, promos: 3 },
            { name: 'Coupang', status: 'online', listings: 142, promos: 2 },
            { name: 'Naver', status: 'online', listings: 89, promos: 1 },
            { name: 'Kakao', status: 'offline', listings: 45, promos: 1 },
          ].map((channel) => (
            <div key={channel.name} className="bg-terminal-bg-tertiary p-3 rounded">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${channel.status === 'online' ? 'bg-terminal-accent-positive' : 'bg-terminal-accent-negative'}`}></span>
                  <span className="text-terminal-text-primary font-medium">{channel.name}</span>
                </div>
                <span className={`text-xs ${channel.status === 'online' ? 'text-terminal-accent-positive' : 'text-terminal-accent-negative'}`}>
                  {channel.status.toUpperCase()}
                </span>
              </div>
              <div className="flex gap-4 text-xs">
                <div>
                  <span className="text-terminal-text-muted">Listings: </span>
                  <span className="text-white">{channel.listings}</span>
                </div>
                <div>
                  <span className="text-terminal-text-muted">Active Promos: </span>
                  <span className="text-terminal-text-secondary">{channel.promos}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function InventoryPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">INVENTORY MONITOR</div>
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-2">
          {[
            { sku: 'SKU-001', name: 'Centella Serum', stock: 45, threshold: 50, status: 'low' },
            { sku: 'SKU-002', name: 'Retinol Cream', stock: 120, threshold: 30, status: 'ok' },
            { sku: 'SKU-003', name: 'Sunscreen SPF50+', stock: 12, threshold: 100, status: 'critical' },
            { sku: 'SKU-004', name: 'Vitamin C Ampoule', stock: 89, threshold: 50, status: 'ok' },
            { sku: 'SKU-005', name: 'Hyaluronic Toner', stock: 200, threshold: 80, status: 'ok' },
          ].map((item) => (
            <div key={item.sku} className="flex items-center justify-between bg-terminal-bg-tertiary p-2 rounded text-sm">
              <div className="flex-1">
                <span className="text-terminal-text-muted">{item.sku}</span>
                <span className="text-white ml-2">{item.name}</span>
              </div>
              <div className="flex items-center gap-4">
                <span className={`
                  ${item.status === 'critical' ? 'text-terminal-accent-negative' : ''}
                  ${item.status === 'low' ? 'text-terminal-accent-warning' : ''}
                  ${item.status === 'ok' ? 'text-terminal-accent-positive' : ''}
                `}>
                  {item.stock} units
                </span>
                <span className={`text-xs px-2 py-0.5 rounded ${
                  item.status === 'critical' ? 'bg-red-900/50 text-red-300' : ''
                }${item.status === 'low' ? 'bg-yellow-900/50 text-yellow-300' : ''}${
                  item.status === 'ok' ? 'bg-green-900/50 text-green-300' : ''
                }`}>
                  {item.status.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function BudgetPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">BUDGET ALLOCATION</div>
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="mb-4">
          <div className="text-terminal-text-muted text-xs mb-1">Q1 2026 TOTAL BUDGET</div>
          <div className="text-2xl font-bold text-terminal-text-primary">₩500,000,000</div>
          <div className="text-sm text-terminal-text-muted">₩342.5M spent (68.5%)</div>
        </div>
        <div className="space-y-3">
          {[
            { category: 'Channel Promotions', allocated: 200, spent: 145, pct: 72 },
            { category: 'Influencer Marketing', allocated: 150, spent: 98, pct: 65 },
            { category: 'Paid Advertising', allocated: 100, spent: 72, pct: 72 },
            { category: 'Content Production', allocated: 50, spent: 27.5, pct: 55 },
          ].map((budget) => (
            <div key={budget.category} className="bg-terminal-bg-tertiary p-3 rounded">
              <div className="flex justify-between items-center mb-2">
                <span className="text-white text-sm">{budget.category}</span>
                <span className="text-terminal-text-secondary text-sm">₩{budget.spent}M / ₩{budget.allocated}M</span>
              </div>
              <div className="w-full h-2 bg-terminal-bg-secondary rounded overflow-hidden">
                <div
                  className="h-full bg-terminal-text-primary"
                  style={{width: `${budget.pct}%`}}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function CompetitorsPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">COMPETITOR INTELLIGENCE</div>
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-3">
          {[
            { brand: 'INNISFREE', activity: 'Flash Sale -20%', channel: 'Oliveyoung', date: 'Today' },
            { brand: 'LANEIGE', activity: 'New Product Launch', channel: 'All Channels', date: 'Yesterday' },
            { brand: 'COSRX', activity: 'Bundle Deal 1+1', channel: 'Coupang', date: '2 days ago' },
            { brand: 'MISSHA', activity: 'Influencer Campaign', channel: 'Naver', date: '3 days ago' },
            { brand: 'ETUDE', activity: 'Price Drop -15%', channel: 'Kakao', date: '4 days ago' },
          ].map((item, idx) => (
            <div key={idx} className="bg-terminal-bg-tertiary p-3 rounded">
              <div className="flex justify-between items-start">
                <div>
                  <div className="text-terminal-text-primary font-medium">{item.brand}</div>
                  <div className="text-white text-sm">{item.activity}</div>
                  <div className="text-terminal-text-muted text-xs mt-1">{item.channel}</div>
                </div>
                <span className="text-terminal-text-muted text-xs">{item.date}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function SettingsPanel() {
  return (
    <div className="terminal-panel h-full flex flex-col">
      <div className="terminal-panel-header">SETTINGS</div>
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-4">
          <div className="bg-terminal-bg-tertiary p-3 rounded">
            <div className="text-terminal-text-primary text-sm mb-2">Connected Channels</div>
            <div className="space-y-2">
              {['Oliveyoung', 'Coupang', 'Naver', 'Kakao'].map((ch) => (
                <div key={ch} className="flex items-center justify-between text-sm">
                  <span className="text-white">{ch}</span>
                  <button className="text-terminal-text-secondary text-xs hover:text-terminal-text-primary">
                    Configure
                  </button>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-terminal-bg-tertiary p-3 rounded">
            <div className="text-terminal-text-primary text-sm mb-2">Notification Settings</div>
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-white">Low Stock Alerts</span>
                <span className="text-terminal-accent-positive">ON</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-white">Competitor Updates</span>
                <span className="text-terminal-accent-positive">ON</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-white">Daily Reports</span>
                <span className="text-terminal-accent-negative">OFF</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export function TerminalLayout() {
  const [activePanel, setActivePanel] = useState<string>('dashboard')

  const renderMainPanel = () => {
    switch (activePanel) {
      case 'help':
        return <HelpPanel />
      case 'analytics':
        return <AnalyticsPanel />
      case 'channels':
        return <ChannelsPanel />
      case 'inventory':
        return <InventoryPanel />
      case 'budget':
        return <BudgetPanel />
      case 'competitors':
        return <CompetitorsPanel />
      case 'settings':
        return <SettingsPanel />
      case 'calendar':
      case 'dashboard':
      default:
        return <AgentChat />
    }
  }

  return (
    <div className="h-screen flex flex-col bg-terminal-bg-primary">
      {/* Title Bar */}
      <TitleBar />

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden p-2 gap-2">
        {/* Left Sidebar */}
        <div className="w-64 flex flex-col gap-2">
          <ChannelStatus />
          <LiveMetrics />
          <AlertsPanel />
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col gap-2">
          {/* Main Panel - changes based on activePanel */}
          <div className="flex-1">
            {renderMainPanel()}
          </div>

          {/* Bottom Panel - Calendar */}
          <div className="h-48">
            <PromotionCalendar />
          </div>
        </div>
      </div>

      {/* Function Key Bar */}
      <FunctionKeyBar activePanel={activePanel} onPanelChange={setActivePanel} />
    </div>
  )
}
