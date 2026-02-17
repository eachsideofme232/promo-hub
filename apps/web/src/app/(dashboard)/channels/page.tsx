'use client'

import { useCallback, useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { Plus, Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import { useTeam } from '@/components/providers/TeamProvider'
import { ChannelList, ChannelForm } from '@/components/channels'
import type { Channel, ChannelFormData } from '@/components/channels'

export default function ChannelsPage() {
  const t = useTranslations('channels')
  const { teamId, isLoading: isTeamLoading } = useTeam()

  const [channels, setChannels] = useState<Channel[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingChannel, setEditingChannel] = useState<Channel | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Fetch channels from API
  const fetchChannels = useCallback(async () => {
    try {
      setIsLoading(true)
      const res = await fetch('/api/channels')
      if (!res.ok) {
        throw new Error('Failed to fetch channels')
      }
      const json = await res.json()
      setChannels(json.data ?? [])
    } catch {
      toast.error(t('loadError'))
    } finally {
      setIsLoading(false)
    }
  }, [t])

  // Load channels when team is ready
  useEffect(() => {
    if (!isTeamLoading && teamId) {
      fetchChannels()
    }
  }, [isTeamLoading, teamId, fetchChannels])

  // Handle create channel
  const handleCreate = async (data: ChannelFormData) => {
    setIsSubmitting(true)
    try {
      const res = await fetch('/api/channels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        const errorJson = await res.json().catch(() => null)
        throw new Error(errorJson?.error ?? 'Failed to create channel')
      }

      toast.success(t('createSuccess'))
      setShowForm(false)
      await fetchChannels()
    } catch (err) {
      toast.error(t('createError'))
      console.error('Channel create error:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle edit channel
  const handleEdit = async (data: ChannelFormData) => {
    if (!editingChannel) return

    setIsSubmitting(true)
    try {
      const res = await fetch(`/api/channels/${editingChannel.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        const errorJson = await res.json().catch(() => null)
        throw new Error(errorJson?.error ?? 'Failed to update channel')
      }

      toast.success(t('updateSuccess'))
      setEditingChannel(null)
      setShowForm(false)
      await fetchChannels()
    } catch (err) {
      toast.error(t('updateError'))
      console.error('Channel update error:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle delete channel
  const handleDelete = async (channelId: string) => {
    try {
      const res = await fetch(`/api/channels/${channelId}`, {
        method: 'DELETE',
      })

      if (!res.ok && res.status !== 204) {
        throw new Error('Failed to delete channel')
      }

      toast.success(t('deleteSuccess'))
      await fetchChannels()
    } catch (err) {
      toast.error(t('deleteError'))
      console.error('Channel delete error:', err)
    }
  }

  // Open form for editing
  const handleEditClick = (channel: Channel) => {
    setEditingChannel(channel)
    setShowForm(true)
  }

  // Close form
  const handleFormCancel = () => {
    setShowForm(false)
    setEditingChannel(null)
  }

  // Loading state while team is loading
  if (isTeamLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-6 h-6 text-sky-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* Page header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">{t('title')}</h1>
        <button
          onClick={() => {
            setEditingChannel(null)
            setShowForm(true)
          }}
          className="inline-flex items-center gap-2 bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          <Plus className="w-4 h-4" />
          {t('addChannel')}
        </button>
      </div>

      {/* Channel list */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <Loader2 className="w-6 h-6 text-sky-500 animate-spin" />
        </div>
      ) : (
        <ChannelList
          channels={channels}
          onEdit={handleEditClick}
          onDelete={handleDelete}
        />
      )}

      {/* Form slide-over */}
      {showForm && (
        <ChannelForm
          channel={editingChannel}
          onSubmit={editingChannel ? handleEdit : handleCreate}
          onCancel={handleFormCancel}
          isSubmitting={isSubmitting}
        />
      )}
    </div>
  )
}
