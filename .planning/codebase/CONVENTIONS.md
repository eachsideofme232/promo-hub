# Coding Conventions

**Analysis Date:** 2026-02-17

## Naming Patterns

**Files:**
- Components: `PascalCase.tsx` (e.g., `UserMenu.tsx`, `PromotionForm.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `usePromoCalendar.ts`)
- Utilities: `camelCase.ts` (e.g., `date.ts`, `currency.ts`, `validation.ts`)
- Type definitions: `snake_case` for database-related types (e.g., `PromotionRow`), camelCase for public types
- API Routes: Follow Next.js convention in `src/app/api/[resource]/route.ts`

**Functions:**
- Public functions: `camelCase` (e.g., `getPromotions`, `createPromotion`)
- Helper functions: `camelCase` with descriptive verbs (e.g., `toPromotion`, `formatDateKR`)
- Component functions: `PascalCase` (exports) or `camelCase` (internal handlers like `handleSubmit`, `handleLogout`)
- Event handlers: `handle[Event]` pattern (e.g., `handleSubmit`, `handleKeyDown`, `handleClickOutside`)

**Variables:**
- State variables: `camelCase` (e.g., `isLoading`, `formData`, `errors`)
- Constants: `UPPER_SNAKE_CASE` for module-level constants; `camelCase` for object values
- Type-safe state: Explicitly typed (e.g., `const [user, setUser] = useState<SupabaseUser | null>(null)`)
- Query parameters: Follow Supabase query builder pattern (e.g., `team_id`, `channel_id` in database queries)

**Types:**
- Interfaces: `PascalCase`, extend types explicitly (e.g., `interface PromotionFormProps`)
- Union types: `PascalCase` (e.g., `PromotionStatus = 'planned' | 'active' | 'ended' | 'cancelled'`)
- Enum-like types: Use union types, not enums (e.g., `type DiscountType = 'percentage' | 'bogo' | 'coupon' | 'gift' | 'bundle'`)
- Database row types: `[EntityName]Row` interface (e.g., `PromotionRow` in `packages/db/queries/promotions.ts`)
- Form data types: `[EntityName]FormData` (e.g., `PromotionFormData`)
- Input/Output types: `Create[Entity]Input`, `Update[Entity]Input` (e.g., `CreatePromotionInput`, `UpdatePromotionInput`)

## Code Style

**Formatting:**
- Line length: No hard limit enforced, but prefer readability
- Indentation: 2 spaces
- Semicolons: Required
- Trailing commas: Use in objects/arrays for cleaner diffs
- No specific code formatter configured (ESLint only for linting)

**Linting:**
- ESLint: Uses `next/core-web-vitals` configuration from Next.js
- Enforced in `apps/web` via `npm run lint`
- TypeScript strict mode enabled at `tsconfig.base.json` with:
  - `strict: true`
  - `noEmit: true`
  - `forceConsistentCasingInFileNames: true`
  - `isolatedModules: true`

**Imports:**
Order in all files:
1. React/Next.js core imports
2. Standard library imports (e.g., `from 'react'`)
3. Third-party libraries (e.g., `zustand`, `date-fns`, `zod`)
4. Supabase imports
5. Local absolute imports with `@` alias (e.g., `@/lib/supabase/client`)
6. Monorepo package imports (e.g., `@promohub/types`, `@promohub/utils`)
7. Relative imports (use minimally, prefer aliases)

**Path Aliases:**
Configured in `apps/web/tsconfig.json`:
- `@/*` → `apps/web/src/*` (application code)
- `@promohub/types` → `packages/types/src` (shared types)
- `@promohub/ui` → `packages/ui/src` (shared UI components)
- `@promohub/utils` → `packages/utils/src` (shared utilities)

## Error Handling

**Patterns:**
- Return object pattern: Functions return `{ data: T | null; error: Error | null }` (see `packages/db/queries/promotions.ts`)
- Zod validation: Use `safeParse` helper from `@promohub/utils` for all form inputs
- Client-side: Display user-friendly error messages in Korean (see `apps/web/src/app/(auth)/login/page.tsx`)
- Async operations: Wrap in `try-catch` or use `.then().catch()` with Supabase
- No error throwing in data access layer; return error objects instead

**Error Display:**
```tsx
{error && (
  <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
    {error}
  </div>
)}
```

**API Route Pattern:**
```typescript
if (error) {
  return Response.json({ error: 'message' }, { status: 401 })
}
```

## Logging

**Framework:** `console` (standard browser/Node.js logging)

**Patterns:**
- Use `console.log` for general info
- Use `console.error` for errors
- Prefix with feature/module name for clarity: `console.log('UserMenu:', data)`
- No structured logging framework configured (future consideration)
- Never log sensitive data (passwords, tokens, secrets)

Example from `UserMenu.tsx`:
```typescript
console.log('Switching to team:', teamId)
```

## Comments

**When to Comment:**
- Explain "why", not "what" (code should be self-documenting for "what")
- Complex algorithms or business logic requiring context
- TODO/FIXME comments with specific action items
- Type assertions or non-obvious type conversions

**JSDoc/TSDoc:**
- Used for exported functions and components
- Library-wide adoption not enforced; optional for public APIs
- Example from `promotions.ts`:
```typescript
export async function getPromotions(
  supabase: SupabaseClient,
  params: GetPromotionsParams
): Promise<GetPromotionsResult>
```

**TODO Comments:**
Present throughout codebase for incomplete implementations:
- `// TODO: Implement with Supabase` - API route stubs
- `// TODO: Get actual team ID from auth context/session` - Demo code needing auth integration
- `// TODO: Fetch teams from database` - Pending feature implementation
- Use consistently for unfinished work

## Function Design

**Size:**
- Prefer smaller functions (under 50 lines)
- Example: `toPromotion` converter in `packages/db/queries/promotions.ts` (18 lines)
- Form handlers split into separate functions (e.g., `handleSubmit` separate from `updateField`)

**Parameters:**
- Prefer object parameters for multiple related values:
  ```typescript
  export async function getPromotions(
    supabase: SupabaseClient,
    params: GetPromotionsParams
  ): Promise<GetPromotionsResult>
  ```
- Use discriminated unions for different modes:
  ```typescript
  interface PromotionFormProps {
    mode: 'create' | 'edit'
    promotion?: Promotion
  }
  ```

**Return Values:**
- Single responsibility: Return one main value type
- Use object pattern for multiple returns: `{ data, error, count }` (see `getPromotions`)
- Type return values explicitly: `Promise<GetPromotionsResult>`

## Module Design

**Exports:**
- Named exports for functions and types (prefer over default exports)
- Barrel files in `src/index.ts` for packages:
  ```typescript
  // packages/types/src/index.ts
  export * from './promotion'
  export * from './channel'
  ```
- Single responsibility per module (e.g., `promotions.ts` for promotion-related queries)

**Barrel Files:**
- Used in `packages/*/src/index.ts` for unified exports
- Enables clean imports: `import type { Promotion } from '@promohub/types'`
- Used in component directories only when appropriate (not enforced)

## Client Components

**Use Client Directive:**
- `'use client'` at top of file when using:
  - React hooks (`useState`, `useEffect`, `useRef`, etc.)
  - Browser APIs (event listeners, DOM manipulation)
  - Supabase client instantiation
- Example: `UserMenu.tsx`, `login/page.tsx`, `PromotionForm.tsx`

**Component Props:**
- Always define `interface [ComponentName]Props`
- Include `className?: string` for styling flexibility
- Document optional props with `?`
```typescript
interface UserMenuProps {
  collapsed?: boolean
  showName?: boolean
  className?: string
}
```

**Suspense:**
- Use for search params and other client-side read operations
- Example: `login/page.tsx` wraps `<LoginForm>` in `<Suspense fallback={<LoginFormFallback />}>`
- Provides immediate loading state without hydration mismatch

## Type Safety

**TypeScript Strict Mode:**
- Enabled globally; all new code must pass strict type checking
- No `any` types allowed without explicit escape (use sparingly with comments)
- Explicit return types on all exported functions
- Prefer `type` for object shapes, `interface` for extensible contracts

**Database Type Mapping:**
- Supabase returns snake_case columns
- Convert to camelCase in application layer using `toPromotion` pattern:
  ```typescript
  function toPromotion(row: PromotionRow): Promotion {
    return {
      id: row.id,
      teamId: row.team_id,  // snake_case → camelCase
      ...
    }
  }
  ```

**Form Validation:**
- All form inputs validated with Zod schemas from `@promohub/utils/src/validation.ts`
- Use `safeParse` helper function for type-safe parsing:
  ```typescript
  const result = safeParse(promotionSchema, formData)
  if (!result.success) {
    // Handle errors: result.errors
  }
  ```

## Authentication & Security

**Supabase Client Usage:**
- Browser client: `createClient()` from `@/lib/supabase/client` (client-side only)
- Server client: `createServerClient()` from `@/lib/supabase/server` (Server Components/API routes)
- Never use service role key in API routes that handle user requests
- All queries respect RLS policies automatically

**Session Verification:**
- Server Components can verify session via:
  ```typescript
  const supabase = await createServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  ```
- Client Components listen to auth state changes:
  ```typescript
  supabase.auth.onAuthStateChange((_event, session) => {
    setUser(session?.user ?? null)
  })
  ```

**Input Validation:**
- All user inputs validated server-side with Zod before database operations
- Never trust client-side IDs; verify team membership on server
- Error messages should be user-friendly (Korean where applicable)

---

*Convention analysis: 2026-02-17*
