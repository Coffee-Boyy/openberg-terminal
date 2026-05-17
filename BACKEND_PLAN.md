# Backend Wiring Plan — Connecting the Frontend to Real Data

> **Goal**: Connect the React frontend to the FastAPI backend so the terminal works with real market data. Zero-configuration demo mode continues to work via MockAdapter.
> **Current State**: Frontend uses hardcoded demo data. Backend has adapter pattern (Yahoo → Finnhub → Mock) but adapters are incomplete and frontend never calls the backend.

---

## 1. What Exists Today

### Backend (`apps/server/`)

| Component | State |
|---|---|
| `app/main.py` | FastAPI app with 6 endpoints, no async, no models |
| `app/services/data.py` | Service layer with try/fallback to MockAdapter |
| `app/adapters/base.py` | Abstract adapter interface — complete |
| `app/adapters/mock.py` | 13 securities, deterministic — works perfectly |
| `app/adapters/yahoo.py` | Uses `yfinance`, sync blocking calls, no async |
| `app/adapters/finnhub.py` | Uses `aiohttp` + `asyncio.run()` hack, broken in prod |
| `pyproject.toml` | Missing `yfinance`, `aiohttp`, `httpx` from deps |

### Frontend (`apps/web/`)

| Component | State |
|---|---|
| `src/services/demo-data.ts` | Hardcoded generators — all data comes from here |
| `src/components/layout/Sidebar.tsx` | Calls `generateQuotes()` from demo-data |
| `src/components/charts/ChartView.tsx` | Calls `generatePriceBars()` from demo-data |
| `src/features/security/SecurityView.tsx` | Calls `generateSecurity()` from demo-data |
| `src/components/layout/NewsPanel.tsx` | Uses `useTerminal().newsItems` (initialized from demo-data) |
| `src/features/portfolio/PortfolioView.tsx` | Local state only, no API |
| `docker-compose.yml` | Has `web`, `server`, `db`, `redis` — but web never calls server |

---

## 2. What Needs to Happen

### A — Backend Foundation

**A1. Fix Finnhub adapter**
- Replace `aiohttp` + `_run()` hack with `httpx` async client
- Proper `async def` methods, no `asyncio.run()` shims
- Add `FINNHUB_API_KEY` env var check in `is_available()`
- File: `apps/server/app/adapters/finnhub.py`

**A2. Improve Yahoo adapter**
- Keep `yfinance` but wrap blocking calls in `asyncio.to_thread()`
- Add proper error handling (timeout, retry, circuit breaker)
- File: `apps/server/app/adapters/yahoo.py`

**A3. Add Pydantic models**
- Define response models for Quote, PriceBar, Security, NewsItem, Dividend
- Use models in endpoint return types for OpenAPI docs
- File: `apps/server/app/models.py`

**A4. Add caching layer**
- In-memory LRU cache as default (no external dependency needed)
- Optional Redis cache for distributed deployments
- TTL: 10s for quotes, 60s for prices, 300s for security descriptions
- File: `apps/server/app/cache.py`

**A5. WebSocket endpoint**
- `GET /ws/quotes?tickers=AAPL,GOOG` — pushes quotes every 30s
- Auto-reconnect on disconnect
- File: `apps/server/app/websocket.py`

### B — Frontend API Client

**B1. Typed fetch client**
- Central API client with base URL, error handling, and caching
- Uses `fetch` + `tanstack-query` for caching/swr
- File: `apps/web/src/services/api.ts`

**B2. TanStack Query hooks**
- `useQuotes(tickers)`: Polls quotes every 30s
- `usePriceHistory(ticker, interval)`: Caches for 5min
- `useSecurity(ticker)`: Cache indefinitely
- `useSearch(query)`: Debounced search
- `useNews(ticker)`: Refresh every 5min
- `useDividends(ticker)`: Cache indefinitely
- File: `apps/web/src/hooks/useApi.ts`

**B3. WebSocket client hook**
- `useWebSocketQuotes(tickers)`: Subscribes to live quotes
- Auto-reconnect with exponential backoff
- Falls back to polling if WebSocket unavailable
- File: `apps/web/src/hooks/useWebSocket.ts`

### C — Component Integration

**C1. Sidebar (watchlist)**
- Replace `generateQuotes()` call with `useQuotes()`
- Watchlist prices update automatically via polling/WebSocket
- File: `apps/web/src/components/layout/Sidebar.tsx`

**C2. ChartView**
- Replace `generatePriceBars()` with `usePriceHistory()`
- Chart loads real price bars from backend
- Timeframe buttons switch interval parameter
- File: `apps/web/src/components/charts/ChartView.tsx`

**C3. SecurityView**
- Replace `generateSecurity()` with `useSecurity()`
- Security description page loads real data
- File: `apps/web/src/features/security/SecurityView.tsx`

**C4. NewsPanel**
- Replace demo-data news with `useNews()`
- Right panel refreshes news feed automatically
- File: `apps/web/src/components/layout/NewsPanel.tsx`

**C5. PortfolioView**
- Keep local state for user-added holdings
- Use `useQuotes()` to resolve live prices for holdings
- Portfolio P&L updates in real-time
- File: `apps/web/src/features/portfolio/PortfolioView.tsx`

### D — Configuration & Dev Experience

**D1. Environment variables**
- `.env` template for `YAHOO_API_KEY`, `FINNHUB_API_KEY`, `OPENBERG_API_URL`
- Frontend reads `VITE_API_URL` from env (defaults to `/api` for proxy)
- File: `apps/web/.env.example`, `apps/server/.env.example`

**D2. Docker Compose**
- Update `docker-compose.yml` to wire web ↔ server properly
- Server exposes `/api` on port 8000
- Web proxies `/api` → `server:8000`
- File: `docker-compose.yml`

**D3. Settings page**
- Settings view can submit API keys to server via `POST /api/settings`
- Server persists keys to env file or database
- File: `apps/web/src/features/settings/SettingsView.tsx`

---

## 3. API Contract

### Endpoints

```
GET /api/health
  → { status: "ok", version: "0.1.0", adapters: ["mock", "finnhub"] }

GET /api/securities?q=AAPL
  → Security[]

GET /api/securities/{ticker}
  → Security

GET /api/quotes?tickers=AAPL,GOOG
  → Quote[]

GET /api/prices/{ticker}?interval=1d&count=200
  → PriceBar[]

GET /api/news?ticker=AAPL&limit=50
  → NewsItem[]

GET /api/dividends/{ticker}
  → Dividend[]

POST /api/settings
  → { ok: true }  (saves API keys)

WS /ws/quotes?tickers=AAPL,GOOG
  → Quote (pushed every 30s)
```

### Models

```typescript
interface Quote {
  ticker: string;
  exchange: string;
  currency: string;
  bid: number;
  ask: number;
  last: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number | null;
  timestamp: string;  // ISO 8601
}

interface PriceBar {
  time: string;       // ISO 8601
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface Security {
  ticker: string;
  name: string;
  exchange: string;
  currency: string;
  sector: string;
  industry: string;
  type: string;
  status: string;
  marketCap: number | null;
  peRatio: number | null;
  eps: number | null;
  dividendYield: number | null;
  beta: number | null;
}

interface NewsItem {
  id: string;
  headline: string;
  summary: string;
  source: string;
  published: string;  // ISO 8601
  sentiment: 'positive' | 'neutral' | 'negative';
  tickers: string[];
  categories: string[];
}

interface Dividend {
  date: string;       // ISO 8601
  amount: number;
}
```

---

## 4. Frontend Client Architecture

```
api.ts
  ├── createApi(baseUrl) → { get, post, fetch }
  ├── GET /api/quotes?tickers=AAPL → Quote[]
  ├── GET /api/prices/AAPL → PriceBar[]
  ├── GET /api/securities?q=AAPL → Security[]
  ├── GET /api/securities/AAPL → Security
  ├── GET /api/news → NewsItem[]
  └── GET /api/dividends/AAPL → Dividend[]

hooks/useApi.ts
  ├── useQuotes(tickers, refetchMs = 30_000) → { data, isLoading }
  ├── usePriceHistory(ticker, interval, staleTime = 5_000) → { data, isLoading }
  ├── useSecurity(ticker, staleTime = Infinity) → { data, isLoading }
  ├── useSearch(query, debounceMs = 300) → { data, isLoading }
  ├── useNews(ticker, refetchMs = 5_000) → { data, isLoading }
  └── useDividends(ticker, staleTime = Infinity) → { data, isLoading }

hooks/useWebSocket.ts
  └── useWebSocketQuotes(tickers) → Quote[] | null

hooks/useDemoMode.ts
  └── useDemoMode() → boolean  (true when backend unavailable)
```

### Demo Mode Fallback

```
Request → /api/quotes
  ├─ 200 OK → use data
  ├─ 502/503/timeout → fall back to demo-data generators
  └─ 429 → cache existing, retry in 60s
```

---

## 5. File Inventory

### New files (7)

| File | Purpose | Lines |
|---|---|---|
| `apps/server/app/models.py` | Pydantic response models | ~80 |
| `apps/server/app/cache.py` | LRU + Redis cache layer | ~60 |
| `apps/server/app/websocket.py` | WebSocket endpoint | ~40 |
| `apps/web/src/services/api.ts` | Typed HTTP client | ~50 |
| `apps/web/src/hooks/useApi.ts` | TanStack Query hooks | ~100 |
| `apps/web/src/hooks/useWebSocket.ts` | WebSocket client hook | ~60 |
| `apps/web/.env.example` | Environment variable template | ~10 |

### Modified files (8)

| File | Change |
|---|---|
| `apps/server/pyproject.toml` | Add `yfinance`, `httpx`, `redis` |
| `apps/server/app/main.py` | Async handlers, model imports, settings endpoint |
| `apps/server/app/adapters/finnhub.py` | Rewrite with httpx |
| `apps/server/app/adapters/yahoo.py` | Wrap in asyncio.to_thread() |
| `apps/server/app/services/data.py` | Add caching decorator |
| `apps/web/src/components/layout/Sidebar.tsx` | Wire to useQuotes |
| `apps/web/src/components/charts/ChartView.tsx` | Wire to usePriceHistory |
| `apps/web/src/components/layout/NewsPanel.tsx` | Wire to useNews |
| `apps/web/src/features/security/SecurityView.tsx` | Wire to useSecurity |
| `apps/web/src/features/portfolio/PortfolioView.tsx` | Wire to useQuotes for prices |
| `docker-compose.yml` | Update services |

### Unchanged files

| File | Why |
|---|---|
| `apps/web/src/services/demo-data.ts` | Kept as fallback when backend unavailable |
| `apps/web/src/store/terminal.ts` | State structure already supports API data |
| `apps/web/src/store/watchlist.ts` | Add/remove works, just need to fetch prices |
| `apps/server/app/adapters/mock.py` | Works perfectly, no changes needed |
| `apps/server/app/adapters/base.py` | Interface is correct |

---

## 6. Execution Order

```
Week 1: Backend foundation (A1-A5)
  ├─ Day 1: Fix Finnhub adapter + Yahoo async wrapping
  ├─ Day 2: Pydantic models + service layer + caching
  └─ Day 3: WebSocket endpoint + Docker Compose wiring

Week 2: Frontend client (B1-B3, D1)
  ├─ Day 1: api.ts + TanStack Query hooks
  ├─ Day 2: WebSocket client hook
  └─ Day 3: Environment variables + demo-mode fallback

Week 3: Component integration (C1-C5, D2-D3)
  ├─ Day 1: Sidebar + ChartView (highest visibility)
  ├─ Day 2: SecurityView + NewsPanel + PortfolioView
  ├─ Day 3: Settings page API key config + E2E tests
```

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `yfinance` blocks event loop | Server stalls under load | Wrap in `asyncio.to_thread()`, add timeout |
| Yahoo rate limits | Data stops flowing | LRU cache with 10s TTL, Mock fallback |
| Finnhub requires API key | Feature not available | Works without key (MockAdapter always available) |
| WebSocket disconnects | Stale prices | Auto-reconnect with exponential backoff, fall back to polling |
| CORS in dev | Blocked requests | Already configured in main.py |
| Large price history responses | Memory/CPU | Limit count parameter, paginate |

---

## 8. Definition of Done

- [ ] `docker compose up` starts web + server, frontend shows real data
- [ ] No API keys: demo mode works identically to current state
- [ ] With `FINNHUB_API_KEY`: real quotes flow through
- [ ] With Yahoo Finance: real quotes from Yahoo
- [ ] ChartView shows real price history from backend
- [ ] Watchlist prices refresh automatically (polling every 30s)
- [ ] All 17 Playwright tests still pass (demo mode via MockAdapter)
- [ ] Settings page can configure API keys on the server
- [ ] OpenAPI docs at `/api/docs` are auto-generated and accurate
- [ ] `pnpm dev` + `uvicorn` runs without errors
