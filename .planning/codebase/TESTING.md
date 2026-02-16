# Testing Patterns

**Analysis Date:** 2026-02-17

## Test Framework

**Status:** Not yet implemented

**Recommended Setup (Pending):**
- Runner: `vitest` or `jest`
- For Next.js: Use `jest` with `@testing-library/react` and `@testing-library/jest-dom`
- Assertion Library: `@testing-library` (for React) + `jest` matchers
- Configuration file: Would be `jest.config.ts` or `vitest.config.ts` in root

**Current Commands:**
```bash
npm run typecheck              # TypeScript checking (available now)
npm run lint                   # ESLint checking (available now)
npm run build                  # Build all packages
npm run test                   # Not yet available - no test framework configured
npm run test:e2e              # Not yet available - no E2E framework configured
```

## Test File Organization

**Location Pattern (To Be Implemented):**
- Co-located with source files: `src/components/[name]/[name].test.tsx`
- Separate test directory: `tests/` at root level
- Recommendation: Co-located for easier refactoring

**Naming Convention (To Be Implemented):**
- Format: `[ComponentName].test.tsx` or `[moduleName].spec.ts`
- Match source file name exactly
- Example: `UserMenu.tsx` → `UserMenu.test.tsx`

**Directory Structure (Planned):**
```
apps/web/src/
├── components/
│   ├── layout/
│   │   ├── UserMenu.tsx
│   │   └── UserMenu.test.tsx
│   ├── promotions/
│   │   ├── PromotionForm.tsx
│   │   └── PromotionForm.test.tsx
├── lib/
│   ├── supabase/
│   │   └── client.ts
├── __tests__/
│   ├── api/
│   │   └── promotions.test.ts
│   └── hooks/
│       └── usePromoCalendar.test.ts

packages/utils/src/
├── date.ts
├── date.test.ts
├── validation.ts
└── validation.test.ts
```

## Test Structure (Recommended Pattern)

**Component Testing Pattern:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { UserMenu } from './UserMenu'
import { createClient } from '@/lib/supabase/client'

jest.mock('@/lib/supabase/client')

describe('UserMenu', () => {
  beforeEach(() => {
    // Setup
    jest.clearAllMocks()
  })

  it('renders login link when no user', () => {
    const mockClient = {
      auth: {
        getUser: jest.fn().mockResolvedValue({ data: { user: null } }),
        onAuthStateChange: jest.fn().mockReturnValue({ data: { subscription: { unsubscribe: jest.fn() } } })
      }
    }
    ;(createClient as jest.Mock).mockReturnValue(mockClient)

    render(<UserMenu />)
    expect(screen.getByText('로그인')).toBeInTheDocument()
  })

  it('opens menu on button click', () => {
    // Test implementation
  })

  it('closes menu on escape key', () => {
    // Test implementation
  })

  afterEach(() => {
    // Cleanup
    jest.clearAllMocks()
  })
})
```

**Patterns:**
- Use `describe` blocks to group related tests
- Use `beforeEach` for setup, `afterEach` for cleanup
- Mock external dependencies (Supabase, router, etc.)
- Test user interactions, not implementation details
- Arrange-Act-Assert pattern for test structure

## Mocking

**Framework:** `jest` (when implemented)

**Mocking Patterns:**

**1. Supabase Client:**
```typescript
jest.mock('@/lib/supabase/client')

const mockClient = {
  auth: {
    getUser: jest.fn(),
    signInWithPassword: jest.fn(),
    signOut: jest.fn(),
    onAuthStateChange: jest.fn().mockReturnValue({
      data: { subscription: { unsubscribe: jest.fn() } }
    })
  },
  from: jest.fn()
}

;(createClient as jest.Mock).mockReturnValue(mockClient)
```

**2. Next.js Router:**
```typescript
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    refresh: jest.fn(),
    pathname: '/calendar'
  }),
  useSearchParams: () => new URLSearchParams()
}))
```

**3. Database Queries:**
```typescript
jest.mock('@promohub/db', () => ({
  getPromotions: jest.fn().mockResolvedValue({
    data: [/* mock promotions */],
    count: 1,
    error: null
  })
}))
```

**What to Mock:**
- External services (Supabase, HTTP clients)
- Next.js navigation (router, search params)
- Database queries (from `@promohub/db`)
- Zustand stores (state management)
- Browser APIs not needed for test (localStorage, if not testing its behavior)

**What NOT to Mock:**
- Utility functions from `@promohub/utils` - test real implementations
- Date/time utilities - can mock if testing specific dates, but prefer using real implementations
- Zod schemas - test validation with real schemas
- UI components from `@promohub/ui` - render real components or use shallow tests
- Custom hooks that don't depend on external services - render with `renderHook`

## Fixtures and Factories

**Test Data (To Be Created):**
```typescript
// packages/db/__tests__/fixtures.ts
export const mockPromotion = {
  id: '123e4567-e89b-12d3-a456-426614174000',
  teamId: 'team-123',
  channelId: 'channel-oliveyoung',
  title: 'Test Promotion',
  description: 'Test Description',
  status: 'planned' as const,
  discountType: 'percentage' as const,
  discountValue: '20',
  startDate: '2026-02-01',
  endDate: '2026-02-28',
  createdAt: '2026-02-17T00:00:00Z',
  updatedAt: '2026-02-17T00:00:00Z',
}

export const mockUser = {
  id: 'user-123',
  email: 'test@example.com',
  user_metadata: {
    full_name: 'Test User'
  }
}
```

**Factory Functions (Recommended):**
```typescript
// apps/web/__tests__/factories.ts
export function createMockPromotion(overrides?: Partial<Promotion>): Promotion {
  return {
    ...mockPromotion,
    ...overrides
  }
}

export function createMockPromotions(count: number): Promotion[] {
  return Array.from({ length: count }, (_, i) =>
    createMockPromotion({ id: `promo-${i}` })
  )
}
```

**Location:**
- Fixtures: `packages/db/__tests__/fixtures.ts` (database test data)
- Factories: `apps/web/__tests__/factories.ts` (component test data)
- Shared: Available via re-exports if needed in multiple test suites

## Coverage

**Requirements:** Not enforced (to be established)

**Recommended Targets:**
- Statements: 70%+
- Branches: 65%+
- Functions: 70%+
- Lines: 70%+

**View Coverage (When Implemented):**
```bash
npm run test:coverage         # Generate coverage report
npm run test:coverage:open    # Open HTML coverage report
```

**Coverage Gaps (Current):**
Since no tests exist yet, entire codebase is untested:
- All components in `apps/web/src/components/` need tests
- All database queries in `packages/db/queries/` need tests
- All utility functions in `packages/utils/src/` should be tested
- All API routes in `apps/web/src/app/api/` need integration tests
- Validation schemas need exhaustive testing

## Test Types

**Unit Tests (Recommended First):**
- Scope: Single function/component in isolation
- Approach: Test inputs and outputs
- Examples to implement:
  - Validation schemas: Test each schema with valid/invalid inputs
  - Utility functions: Test `formatDateKR`, `formatDateRange`, etc.
  - Database query mappers: Test `toPromotion` conversion
  - Component rendering: Test `Button`, `Input`, `Card` components

```typescript
// Example: Validation test
describe('promotionSchema', () => {
  it('validates complete promotion data', () => {
    const validData = {
      title: 'Winter Sale',
      channelId: 'uuid-1',
      teamId: 'uuid-2',
      discountType: 'percentage',
      discountValue: '30',
      startDate: '2026-02-01T00:00:00Z',
      endDate: '2026-02-28T23:59:59Z'
    }
    const result = promotionSchema.safeParse(validData)
    expect(result.success).toBe(true)
  })

  it('rejects missing required fields', () => {
    const invalidData = { title: 'Winter Sale' }
    const result = promotionSchema.safeParse(invalidData)
    expect(result.success).toBe(false)
  })

  it('rejects end date before start date', () => {
    const invalidData = {
      ...validPromotion,
      startDate: '2026-02-28T00:00:00Z',
      endDate: '2026-02-01T00:00:00Z'
    }
    const result = promotionSchema.safeParse(invalidData)
    expect(result.success).toBe(false)
    expect(result.error?.errors[0].path).toContain('endDate')
  })
})
```

**Integration Tests (For API Routes):**
- Scope: Multiple components/functions working together
- Approach: Test API routes with mocked Supabase
- Examples to implement:
  - POST `/api/promotions` with validation and database insert
  - GET `/api/promotions` with filtering and RLS
  - Auth callback route with OAuth flow

```typescript
// Example: API integration test
describe('POST /api/promotions', () => {
  it('creates promotion with valid data', async () => {
    const request = new Request('http://localhost:3000/api/promotions', {
      method: 'POST',
      body: JSON.stringify({
        title: 'New Promotion',
        channelId: 'uuid-1',
        teamId: 'uuid-2',
        discountType: 'percentage',
        discountValue: '20',
        startDate: '2026-03-01',
        endDate: '2026-03-31'
      })
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.id).toBeDefined()
    expect(data.title).toBe('New Promotion')
  })

  it('rejects unauthenticated requests', async () => {
    // Test that returns 401
  })

  it('validates input with Zod', async () => {
    // Test that invalid data returns 400
  })
})
```

**E2E Tests (For User Flows):**
- Framework: Not configured (consider Playwright or Cypress)
- Scope: Complete user workflows
- Examples to implement:
  - User login flow
  - Create promotion from calendar view
  - Filter and search promotions
  - Multi-user team switching

```typescript
// Example structure (Playwright)
describe('Promotion Creation Flow', () => {
  it('user can create promotion from new page', async ({ page }) => {
    await page.goto('/promotions/new')
    await page.fill('input[name="title"]', 'Summer Sale')
    await page.selectOption('select[name="channelId"]', 'oliveyoung-uuid')
    await page.fill('input[name="discountValue"]', '25')
    await page.click('button[type="submit"]')
    await page.waitForURL('/promotions/**')
    expect(page.url()).toContain('/promotions/')
  })
})
```

## Common Patterns

**Async Testing:**
```typescript
// Jest with async/await
it('fetches user data', async () => {
  const result = await getUser(supabase, 'user-id')
  expect(result.data).toBeDefined()
})

// With mocked promises
it('handles fetch error', async () => {
  const mockClient = {
    from: jest.fn().mockReturnValue({
      select: jest.fn().mockReturnValue({
        eq: jest.fn().mockRejectedValue(new Error('Database error'))
      })
    })
  }
  const result = await getPromotion(mockClient, 'id')
  expect(result.error).toBeDefined()
})
```

**Error Testing:**
```typescript
describe('Error Handling', () => {
  it('returns error on validation failure', () => {
    const result = safeParse(promotionSchema, { title: '' })
    expect(result.success).toBe(false)
    expect(result.errors).toBeDefined()
    expect(result.errors.title).toBe('프로모션명을 입력해주세요')
  })

  it('catches Supabase errors gracefully', async () => {
    mockClient.from.mockImplementation(() => {
      throw new Error('Network error')
    })
    const result = await getPromotions(mockClient, { teamId: 'team-1' })
    expect(result.error).toBeDefined()
    expect(result.data).toEqual([])
  })
})
```

**Component Interaction Testing:**
```typescript
describe('PromotionForm', () => {
  it('updates field on input change', () => {
    render(<PromotionForm mode="create" teamId="team-123" />)
    const titleInput = screen.getByLabelText('프로모션명')

    fireEvent.change(titleInput, { target: { value: 'New Title' } })
    expect(titleInput).toHaveValue('New Title')
  })

  it('submits form with valid data', async () => {
    const handleSubmit = jest.fn()
    render(
      <PromotionForm
        mode="create"
        teamId="team-123"
        onSubmit={handleSubmit}
      />
    )

    await userEvent.type(screen.getByLabelText('프로모션명'), 'Sale')
    await userEvent.click(screen.getByRole('button', { name: /저장/ }))

    expect(handleSubmit).toHaveBeenCalled()
  })
})
```

## Test Maintenance

**Principles:**
- Tests should be deterministic (no random data, fixed timestamps)
- Avoid implementation detail testing (test behavior, not internal state)
- Use meaningful assertion messages
- Keep tests focused on one behavior per test
- Refactor tests when requirements change, don't skip failing tests

**Before Writing Tests:**
- Ensure feature is stable (no active refactoring)
- Have clear requirements for behavior
- Plan which layers need testing (unit vs integration)

---

*Testing analysis: 2026-02-17*
