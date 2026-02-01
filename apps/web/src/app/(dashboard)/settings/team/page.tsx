'use client'

import Link from 'next/link'
import { ArrowLeft, Plus, Mail, Shield, MoreVertical } from 'lucide-react'

const DEMO_MEMBERS = [
  { id: '1', name: '김팀장', email: 'team.lead@example.com', role: 'owner', avatar: 'K' },
  { id: '2', name: '이마케터', email: 'marketer@example.com', role: 'admin', avatar: 'L' },
  { id: '3', name: '박운영', email: 'ops@example.com', role: 'member', avatar: 'P' },
]

const ROLE_LABELS = {
  owner: { label: '소유자', color: 'bg-purple-100 text-purple-700' },
  admin: { label: '관리자', color: 'bg-blue-100 text-blue-700' },
  member: { label: '멤버', color: 'bg-gray-100 text-gray-700' },
  viewer: { label: '뷰어', color: 'bg-gray-100 text-gray-600' },
}

export default function TeamSettingsPage() {
  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-4">
          <Link href="/settings" className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft size={20} />
          </Link>
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900">팀 관리</h1>
            <p className="text-sm text-gray-500">팀원을 초대하고 권한을 관리하세요</p>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
            <Plus size={20} />
            팀원 초대
          </button>
        </div>
      </header>

      {/* Team members list */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-3xl mx-auto">
          {/* Team info */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 text-2xl font-bold">
                P
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Phase 1 팀</h2>
                <p className="text-sm text-gray-500">데모 팀 • 3명의 멤버</p>
              </div>
            </div>
          </div>

          {/* Members table */}
          <div className="bg-white rounded-lg border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="font-semibold text-gray-900">팀원 ({DEMO_MEMBERS.length})</h3>
            </div>
            <div className="divide-y divide-gray-100">
              {DEMO_MEMBERS.map((member) => {
                const role = ROLE_LABELS[member.role as keyof typeof ROLE_LABELS]
                return (
                  <div key={member.id} className="px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-medium">
                        {member.avatar}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{member.name}</p>
                        <p className="text-sm text-gray-500 flex items-center gap-1">
                          <Mail size={12} />
                          {member.email}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${role.color}`}>
                        {role.label}
                      </span>
                      <button className="p-2 hover:bg-gray-100 rounded-lg text-gray-400">
                        <MoreVertical size={16} />
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Pending invites */}
          <div className="bg-white rounded-lg border border-gray-200 mt-6">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="font-semibold text-gray-900">대기중인 초대 (0)</h3>
            </div>
            <div className="p-6 text-center text-gray-500">
              <Mail className="w-8 h-8 mx-auto mb-2 text-gray-300" />
              <p className="text-sm">대기중인 초대가 없습니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
