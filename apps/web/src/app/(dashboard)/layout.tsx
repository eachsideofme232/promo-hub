'use client'

import { Suspense, useState, useCallback } from 'react'
import { usePathname } from 'next/navigation'
import { FilterProvider, FilterSidebar, MobileFilterButton } from '@/components/filters'
import { Sidebar, Header, MobileNav } from '@/components/layout'
import { TeamProvider } from '@/components/providers/TeamProvider'
import { ChannelProvider } from '@/components/providers/ChannelProvider'

// Route title mappings for dynamic header titles
const routeTitles: Record<string, { name: string; nameEn: string }> = {
  '/dashboard': { name: '대시보드', nameEn: 'Dashboard' },
  '/calendar': { name: '캘린더', nameEn: 'Calendar' },
  '/promotions': { name: '프로모션', nameEn: 'Promotions' },
  '/products': { name: '상품', nameEn: 'Products' },
  '/channels': { name: '채널', nameEn: 'Channels' },
  '/settings': { name: '설정', nameEn: 'Settings' },
}

// Pages that should show the filter sidebar
const FILTER_ENABLED_PATHS = ['/calendar', '/promotions']

function DashboardLayoutContent({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [mobileNavOpen, setMobileNavOpen] = useState(false)

  // Check if current page should show filters
  const showFilters = FILTER_ENABLED_PATHS.some((path) =>
    pathname.startsWith(path)
  )

  // Get the current page title
  const getPageTitle = useCallback(() => {
    // Find exact match first
    if (routeTitles[pathname]) {
      return routeTitles[pathname].name
    }
    // Find prefix match
    const matchedRoute = Object.keys(routeTitles).find((route) =>
      pathname.startsWith(route)
    )
    if (matchedRoute) {
      return routeTitles[matchedRoute].name
    }
    return ''
  }, [pathname])

  const handleMobileMenuToggle = useCallback(() => {
    setMobileNavOpen((prev) => !prev)
  }, [])

  const handleMobileNavClose = useCallback(() => {
    setMobileNavOpen(false)
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Main Navigation Sidebar - Desktop */}
      <Sidebar
        collapsed={sidebarCollapsed}
        onCollapsedChange={setSidebarCollapsed}
      />

      {/* Mobile Navigation Drawer */}
      <MobileNav isOpen={mobileNavOpen} onClose={handleMobileNavClose} />

      {/* Filter Sidebar (conditionally rendered) - Desktop only */}
      {showFilters && <FilterSidebar />}

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header - Mobile & Desktop */}
        <Header
          title={getPageTitle()}
          onMobileMenuToggle={handleMobileMenuToggle}
        />

        {/* Mobile filter button for pages with filters */}
        {showFilters && (
          <div className="lg:hidden px-4 py-2 bg-white border-b border-gray-200">
            <MobileFilterButton />
          </div>
        )}

        {/* Page content */}
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  )
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <Suspense fallback={<DashboardLayoutSkeleton />}>
      <TeamProvider>
        <ChannelProvider>
          <FilterProvider>
            <DashboardLayoutContent>{children}</DashboardLayoutContent>
          </FilterProvider>
        </ChannelProvider>
      </TeamProvider>
    </Suspense>
  )
}

function DashboardLayoutSkeleton() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar skeleton */}
      <aside className="w-64 bg-white border-r border-gray-200 flex-col hidden lg:flex">
        <div className="h-16 flex items-center px-4 border-b border-gray-200">
          <div className="h-6 w-24 bg-gray-200 rounded animate-pulse" />
        </div>
        <nav className="flex-1 p-4 space-y-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className="h-10 bg-gray-100 rounded-lg animate-pulse"
            />
          ))}
        </nav>
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-gray-200 rounded-full animate-pulse" />
            <div className="flex-1">
              <div className="h-4 w-20 bg-gray-200 rounded animate-pulse" />
              <div className="h-3 w-16 bg-gray-100 rounded animate-pulse mt-1" />
            </div>
          </div>
        </div>
      </aside>

      {/* Main content area skeleton */}
      <div className="flex-1 flex flex-col">
        {/* Header skeleton */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 lg:px-6">
          <div className="flex items-center gap-4">
            <div className="lg:hidden w-8 h-8 bg-gray-100 rounded animate-pulse" />
            <div className="h-6 w-32 bg-gray-200 rounded animate-pulse hidden sm:block" />
          </div>
          <div className="flex items-center gap-3">
            <div className="w-24 h-9 bg-gray-100 rounded-lg animate-pulse" />
            <div className="w-9 h-9 bg-gray-100 rounded-lg animate-pulse" />
            <div className="hidden lg:flex items-center gap-2 pl-4 border-l border-gray-200">
              <div className="w-9 h-9 bg-gray-200 rounded-full animate-pulse" />
            </div>
          </div>
        </header>

        {/* Main content skeleton */}
        <main className="flex-1 p-6">
          <div className="h-8 w-48 bg-gray-200 rounded animate-pulse mb-4" />
          <div className="h-64 bg-white rounded-lg border border-gray-200 animate-pulse" />
        </main>
      </div>
    </div>
  )
}
