// Channel seed data
// Use this to seed the channels table

export const CHANNELS = [
  {
    name: '올리브영',
    slug: 'oliveyoung',
    color: '#00A651',
    logo_url: null,
  },
  {
    name: '쿠팡',
    slug: 'coupang',
    color: '#E31937',
    logo_url: null,
  },
  {
    name: '네이버',
    slug: 'naver',
    color: '#03C75A',
    logo_url: null,
  },
  {
    name: '카카오',
    slug: 'kakao',
    color: '#FEE500',
    logo_url: null,
  },
  {
    name: '무신사',
    slug: 'musinsa',
    color: '#000000',
    logo_url: null,
  },
  {
    name: 'SSG',
    slug: 'ssg',
    color: '#FF5252',
    logo_url: null,
  },
  {
    name: '롯데ON',
    slug: 'lotteon',
    color: '#E60012',
    logo_url: null,
  },
  {
    name: '11번가',
    slug: '11st',
    color: '#FF0050',
    logo_url: null,
  },
]

// SQL to insert channels
export const CHANNELS_INSERT_SQL = `
INSERT INTO channels (name, slug, color, logo_url) VALUES
  ('올리브영', 'oliveyoung', '#00A651', NULL),
  ('쿠팡', 'coupang', '#E31937', NULL),
  ('네이버', 'naver', '#03C75A', NULL),
  ('카카오', 'kakao', '#FEE500', NULL),
  ('무신사', 'musinsa', '#000000', NULL),
  ('SSG', 'ssg', '#FF5252', NULL),
  ('롯데ON', 'lotteon', '#E60012', NULL),
  ('11번가', '11st', '#FF0050', NULL)
ON CONFLICT (slug) DO NOTHING;
`
