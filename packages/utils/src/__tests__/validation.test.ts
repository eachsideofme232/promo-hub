import { describe, it, expect } from 'vitest'
import {
  loginSchema,
  signupSchema,
  promotionSchema,
  teamSchema,
  teamInviteSchema,
  productFormSchema,
  calendarFilterSchema,
  safeParse,
} from '../validation'

const UUID = 'c1000000-0000-0000-0000-000000000001'
const UUID2 = 'a1000000-0000-0000-0000-000000000002'

describe('loginSchema', () => {
  it('accepts a valid email and password', () => {
    const result = loginSchema.safeParse({ email: 'user@example.com', password: 'secret' })
    expect(result.success).toBe(true)
  })

  it('rejects an invalid email', () => {
    const result = loginSchema.safeParse({ email: 'not-an-email', password: 'secret' })
    expect(result.success).toBe(false)
  })

  it('rejects an empty password', () => {
    const result = loginSchema.safeParse({ email: 'user@example.com', password: '' })
    expect(result.success).toBe(false)
  })
})

describe('signupSchema', () => {
  const valid = {
    email: 'user@example.com',
    password: 'Password1',
    confirmPassword: 'Password1',
    name: '홍길동',
    agreeToTerms: true,
  }

  it('accepts a valid signup payload', () => {
    expect(signupSchema.safeParse(valid).success).toBe(true)
  })

  it('rejects mismatched password confirmation', () => {
    const result = signupSchema.safeParse({ ...valid, confirmPassword: 'Password2' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.errors[0].path).toContain('confirmPassword')
    }
  })

  it.each([
    ['too short', 'Pw1'],
    ['no uppercase', 'password1'],
    ['no lowercase', 'PASSWORD1'],
    ['no digit', 'PasswordX'],
  ])('rejects weak password (%s)', (_label, password) => {
    const result = signupSchema.safeParse({ ...valid, password, confirmPassword: password })
    expect(result.success).toBe(false)
  })

  it('rejects when terms are not agreed', () => {
    expect(signupSchema.safeParse({ ...valid, agreeToTerms: false }).success).toBe(false)
  })
})

describe('promotionSchema', () => {
  const valid = {
    title: '올리브영 7월 세일',
    channelId: UUID,
    teamId: UUID2,
    discountType: 'percentage',
    discountValue: '20',
    startDate: '2026-07-01',
    endDate: '2026-07-15',
  }

  it('accepts a valid promotion', () => {
    expect(promotionSchema.safeParse(valid).success).toBe(true)
  })

  it('accepts a single-day promotion (start == end)', () => {
    expect(
      promotionSchema.safeParse({ ...valid, startDate: '2026-07-01', endDate: '2026-07-01' }).success
    ).toBe(true)
  })

  it('rejects endDate before startDate', () => {
    const result = promotionSchema.safeParse({ ...valid, startDate: '2026-07-15', endDate: '2026-07-01' })
    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.errors[0].path).toContain('endDate')
    }
  })

  it('rejects an empty title and a title over 200 chars', () => {
    expect(promotionSchema.safeParse({ ...valid, title: '' }).success).toBe(false)
    expect(promotionSchema.safeParse({ ...valid, title: 'a'.repeat(201) }).success).toBe(false)
  })

  it('rejects a non-uuid channelId', () => {
    expect(promotionSchema.safeParse({ ...valid, channelId: 'oliveyoung' }).success).toBe(false)
  })

  it('rejects an unknown discountType', () => {
    expect(promotionSchema.safeParse({ ...valid, discountType: 'flat' }).success).toBe(false)
  })

  it('rejects an unparseable date', () => {
    expect(promotionSchema.safeParse({ ...valid, startDate: 'not-a-date' }).success).toBe(false)
  })
})

describe('teamSchema', () => {
  it('accepts a valid team', () => {
    expect(teamSchema.safeParse({ name: '마케팅팀', slug: 'marketing-1' }).success).toBe(true)
  })

  it.each([
    ['uppercase', 'Marketing'],
    ['spaces', 'my team'],
    ['korean', '마케팅'],
    ['underscore', 'my_team'],
  ])('rejects invalid slug (%s)', (_label, slug) => {
    expect(teamSchema.safeParse({ name: 'Team', slug }).success).toBe(false)
  })
})

describe('teamInviteSchema', () => {
  it('accepts valid roles', () => {
    for (const role of ['admin', 'member', 'viewer']) {
      expect(teamInviteSchema.safeParse({ email: 'a@b.com', role }).success).toBe(true)
    }
  })

  it('rejects the owner role via invite', () => {
    expect(teamInviteSchema.safeParse({ email: 'a@b.com', role: 'owner' }).success).toBe(false)
  })
})

describe('productFormSchema', () => {
  const valid = {
    name: '수분 크림 50ml',
    sku: 'CRM-001',
    basePrice: 25000,
  }

  it('accepts a minimal valid product and defaults channelPrices to []', () => {
    const result = productFormSchema.safeParse(valid)
    expect(result.success).toBe(true)
    if (result.success) {
      expect(result.data.channelPrices).toEqual([])
    }
  })

  it('rejects negative and non-integer prices', () => {
    expect(productFormSchema.safeParse({ ...valid, basePrice: -1 }).success).toBe(false)
    expect(productFormSchema.safeParse({ ...valid, basePrice: 100.5 }).success).toBe(false)
  })

  it('trims whitespace on name and sku', () => {
    const result = productFormSchema.safeParse({ ...valid, name: '  크림  ', sku: ' CRM-002 ' })
    expect(result.success).toBe(true)
    if (result.success) {
      expect(result.data.name).toBe('크림')
      expect(result.data.sku).toBe('CRM-002')
    }
  })

  it('validates nested channel prices', () => {
    const result = productFormSchema.safeParse({
      ...valid,
      channelPrices: [{ channelId: UUID, sellingPrice: 23000, channelFeeRate: 30 }],
    })
    expect(result.success).toBe(true)

    const bad = productFormSchema.safeParse({
      ...valid,
      channelPrices: [{ channelId: UUID, sellingPrice: 23000, channelFeeRate: 101 }],
    })
    expect(bad.success).toBe(false)
  })
})

describe('calendarFilterSchema', () => {
  it('accepts a valid date range with optional filters', () => {
    const result = calendarFilterSchema.safeParse({
      startDate: '2026-07-01',
      endDate: '2026-07-31',
      channels: [UUID],
      status: ['planned', 'active'],
    })
    expect(result.success).toBe(true)
  })

  it('rejects a reversed date range', () => {
    expect(
      calendarFilterSchema.safeParse({ startDate: '2026-07-31', endDate: '2026-07-01' }).success
    ).toBe(false)
  })
})

describe('safeParse helper', () => {
  it('returns data on success', () => {
    const result = safeParse(loginSchema, { email: 'a@b.com', password: 'pw' })
    expect(result.success).toBe(true)
    expect(result.data).toEqual({ email: 'a@b.com', password: 'pw' })
    expect(result.errors).toBeUndefined()
  })

  it('maps errors by dotted path on failure', () => {
    const result = safeParse(promotionSchema, {
      title: '',
      channelId: 'bad',
      teamId: UUID,
      discountType: 'percentage',
      discountValue: '10',
      startDate: '2026-07-01',
      endDate: '2026-07-31',
    })
    expect(result.success).toBe(false)
    expect(result.errors).toBeDefined()
    expect(result.errors!['title']).toBeTruthy()
    expect(result.errors!['channelId']).toBeTruthy()
  })
})
