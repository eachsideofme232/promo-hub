// Team types

export type TeamRole = 'owner' | 'admin' | 'member' | 'viewer'

export interface Team {
  id: string
  name: string
  slug: string
  logoUrl?: string
  createdAt: string
  updatedAt: string
}

export interface TeamMember {
  id: string
  teamId: string
  userId: string
  role: TeamRole
  createdAt: string

  // Joined user info
  user?: {
    id: string
    email: string
    name?: string
    avatarUrl?: string
  }
}

export interface TeamInvite {
  id: string
  teamId: string
  email: string
  role: TeamRole
  expiresAt: string
  createdAt: string
  createdBy: string
}
