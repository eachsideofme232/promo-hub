import { redirect } from 'next/navigation'

export default function Home() {
  // Redirect to dashboard calendar (Phase 1 main feature)
  redirect('/calendar')
}
