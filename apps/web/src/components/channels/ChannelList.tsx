'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { Pencil, Trash2, Lock } from 'lucide-react'

export interface Channel {
  id: string
  name: string
  slug: string
  color: string
  isActive: boolean
  isSystem: boolean
  teamId: string | null
  promoTypes: string[]
}

interface ChannelListProps {
  channels: Channel[]
  onEdit: (channel: Channel) => void
  onDelete: (channelId: string) => void
}

export function ChannelList({ channels, onEdit, onDelete }: ChannelListProps) {
  const t = useTranslations('channels')
  const [deletingId, setDeletingId] = useState<string | null>(null)

  const handleDeleteClick = (channelId: string) => {
    setDeletingId(channelId)
  }

  const handleDeleteConfirm = (channelId: string) => {
    onDelete(channelId)
    setDeletingId(null)
  }

  const handleDeleteCancel = () => {
    setDeletingId(null)
  }

  if (channels.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-12 text-center">
        <p className="text-gray-500">{t('noChannels')}</p>
      </div>
    )
  }

  return (
    <>
      {/* Desktop table */}
      <div className="hidden lg:block bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('name')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('slug')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('promoTypes')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('status')}
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('type')}
              </th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                {t('actions')}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {channels.map((channel) => (
              <tr key={channel.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <span
                      className="w-4 h-4 rounded-full flex-shrink-0"
                      style={{ backgroundColor: channel.color }}
                    />
                    <span className="font-medium text-gray-900">{channel.name}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <code className="text-sm text-gray-600 bg-gray-100 px-2 py-0.5 rounded">
                    {channel.slug}
                  </code>
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-wrap gap-1">
                    {channel.promoTypes.length > 0 ? (
                      channel.promoTypes.map((type) => (
                        <span
                          key={type}
                          className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-700"
                        >
                          {type}
                        </span>
                      ))
                    ) : (
                      <span className="text-sm text-gray-400">-</span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4">
                  {channel.isActive ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      {t('active')}
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-600">
                      {t('inactive')}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4">
                  {channel.isSystem ? (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                      <Lock className="w-3 h-3" />
                      {t('preseeded')}
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-sky-100 text-sky-700">
                      {t('custom')}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 text-right">
                  {channel.isSystem ? (
                    <span className="text-sm text-gray-400">-</span>
                  ) : (
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => onEdit(channel)}
                        className="p-1.5 text-gray-500 hover:text-sky-600 hover:bg-sky-50 rounded-md transition-colors"
                        title={t('editChannel')}
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteClick(channel.id)}
                        className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                        title={t('deleteChannel')}
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile card layout */}
      <div className="lg:hidden space-y-3">
        {channels.map((channel) => (
          <div
            key={channel.id}
            className="bg-white rounded-lg border border-gray-200 shadow-sm p-4"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <span
                  className="w-4 h-4 rounded-full flex-shrink-0"
                  style={{ backgroundColor: channel.color }}
                />
                <div>
                  <div className="font-medium text-gray-900">{channel.name}</div>
                  <code className="text-xs text-gray-500">{channel.slug}</code>
                </div>
              </div>
              <div className="flex items-center gap-1">
                {channel.isSystem ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                    <Lock className="w-3 h-3" />
                    {t('preseeded')}
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-sky-100 text-sky-700">
                    {t('custom')}
                  </span>
                )}
              </div>
            </div>

            {channel.promoTypes.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {channel.promoTypes.map((type) => (
                  <span
                    key={type}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-700"
                  >
                    {type}
                  </span>
                ))}
              </div>
            )}

            <div className="mt-3 flex items-center justify-between">
              <div>
                {channel.isActive ? (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">
                    {t('active')}
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-600">
                    {t('inactive')}
                  </span>
                )}
              </div>
              {!channel.isSystem && (
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onEdit(channel)}
                    className="p-1.5 text-gray-500 hover:text-sky-600 hover:bg-sky-50 rounded-md transition-colors"
                    title={t('editChannel')}
                  >
                    <Pencil className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteClick(channel.id)}
                    className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                    title={t('deleteChannel')}
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Delete confirmation dialog */}
      {deletingId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-sm mx-4 w-full">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {t('deleteChannel')}
            </h3>
            <p className="text-sm text-gray-600 mb-1">{t('confirmDelete')}</p>
            <p className="text-sm text-gray-500 mb-6">{t('confirmDeleteDesc')}</p>
            <div className="flex justify-end gap-3">
              <button
                onClick={handleDeleteCancel}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                {t('cancel')}
              </button>
              <button
                onClick={() => handleDeleteConfirm(deletingId)}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
              >
                {t('deleteChannel')}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
