import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PromoHub - K-beauty 브랜드를 위한 프로모션 관리 플랫폼',
  description: '올리브영, 쿠팡, 네이버 등 모든 채널의 프로모션을 한 곳에서 관리하세요.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
