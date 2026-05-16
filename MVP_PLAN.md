# OpenBerg Terminal — MVP Implementation Plan

> **Target**: Retail traders (individual investors, self-directed accounts, active traders)
> **Platform**: Browser-first (React + Vite), responsive to desktop/mobile
> **Goal**: Ship a usable, self-hostable financial terminal in ~12 weeks

---

## 1. North Star

A browser-based terminal that gives retail traders real-time equities/options data, interactive charting, watchlists, news, a command palette, and portfolio tracking — all free, open-source, and self-hostable.

---

## 2. Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| **UI Framework** | React 19 + TypeScript | Ecosystem, component libraries, developer familiarity |
| **Build** | Vite 6 | Fast HMR, zero-config for production |
| **Styling** | Tailwind CSS 4 + headless UI components (Radix UI) | Rapid styling, accessibility out of the box |
| **Charts** | Lightweight Charts (TradingView) + D3 for custom overlays | Bloomberg-like candlestick/line charts, performant |
| **State** | Zustand + TanStack Query (server state) | Minimal boilerplate, devtools support |
| **Command Palette** | cmdk (or custom) | Bloomberg command-line feel |
| **Real-time** | WebSocket (native) + Server-Sent Events for fallback | Sub-second data updates |
| **Backend API** | FastAPI (Python) — MVP phase; migrate to Rust in Phase 2 | Fast data integrations, async I/O for data providers |
| **Database** | PostgreSQL (reference data, user state) + TimescaleDB (timeseries) | SQL familiarity, timescale for price history |
| **Cache** | Redis | Rate limiting, WebSocket fan-out, hot data cache |
| **Message Bus** | Redis Streams (MVP) → Kafka (Phase 2) | Lightweight for MVP, scales later |
| **Container** | Docker + docker-compose | Self-host with one command |
| **Auth** | Better Auth (or Supabase Auth) | Email/password, OAuth (Google), session management |
| **Deploy** | Docker Compose (self-host) + Render/Railway (managed demo) | Low barrier for self-hosting |

---

## 3. MVP Scope

### 3.1. Must-Have (Ship)

| Feature | Description |
|---|---|
| **Command Palette** | Bloomberg-style `cmd` bar: type ticker + function, press Enter |
| **Real-Time Watchlists** | Persistent, customizable watchlists with live price updates |
| **Interactive Charts** | Candlestick/line charts with overlays (MA, RSI, MACD, Bollinger) |
| **News Feed** | Aggregated financial news with sentiment tagging |
| **Portfolio Tracker** | Import holdings, track P&L, basic performance metrics |
| **Price Alerts** | User-configurable alerts (email/browser notification) |
| **Security Search** | Universal search across tickers, companies, indices |
| **User Accounts** | Sign-up, login, saved preferences, multi-device |
| **Dark Theme** | Bloomberg-classic black/green theme + light mode |
| **Responsive Layout** | Panel-based layout that adapts from phone to ultrawide |
| **Self-Hostable** | `docker compose up` → fully functional instance |

### 3.2. Nice-to-Have (Post-MVP)

| Feature | Notes |
|---|---|
| Options chain viewer | Greeks, IV surface |
| iB messaging | XMPP/Matrix-based chat |
| Technical analysis tools | Drawing tools, Fibonacci, trendlines |
| Screener | Filter stocks by criteria (P/E, volume, etc.) |
| Paper trading | Simulated order entry |
| Mobile app | PWA / React Native wrapper |
| Excel/Sheets add-in | Spreadsheet data feeds |
| Custom connectors | User-defined data source plugins |

### 3.3. Explicitly Out of Scope for MVP

- Fixed income / bonds
- Derivatives beyond basic options data
- Regulatory compliance / message archiving
- Institutional portfolio management (Brinson attribution, etc.)
- Bloomberg-style IRC chat
- Trade execution / brokerage integration
- Alternative data feeds (satellite, web traffic, etc.)

---

## 4. Information Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  STATUS BAR (connection, time, session, alerts)                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌────────────────────────────────────────────┐│
│  │ WATCHLIST    │  │                                              ││
│  │              │  │  MAIN PANEL (current function)              ││
│  │ AAPL  $198.2 │  │                                              ││
│  │ +1.2% ▲      │  │  ┌────────────────────────────────────────┐ ││
│  │              │  │  │ CHART / DATA / NEWS / PORTFOLIO        │ ││
│  │ GOOG  $172.5 │  │  │                                        │ ││
│  │ -0.3% ▼      │  │  │  [interactive content area]            │ ││
│  │              │  │  │                                        │ ││
│  │ MSFT  $389.1 │  │  └────────────────────────────────────────┘ ││
│  │ +0.8% ▲      │  │                                              ││
│  │              │  │  ┌────────────────────────────────────────┐ ││
│  │ TSLA  $177.4 │  │  │ NEWS FEED                              │ ││
│  │ -2.1% ▼      │  │  │                                        │ ││
│  │              │  │  │ • Apple beats Q4 earnings by $0.40     │ ││
│  │ NVDA  $875.3 │  │  │ • Fed holds rates steady at 5.25%      │ ││
│  │ +3.4% ▲      │  │  │ • TSLA delivery numbers miss estimates  │ ││
│  │              │  │  │                                        │ ││
│  └──────────────┘  │  └────────────────────────────────────────┘ ││
│                    └────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│  COMMAND BAR  [ AAPL CG ]                    (F2 GOVT) (F8 EQ)  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Core Components

### 5.1. Frontend Component Tree

```
<App>
├── <StatusBar>                    # Connection, clock, session, alerts
├── <TerminalLayout>               # Resizable panel system
│   ├── <Sidebar>                   # Left sidebar
│   │   ├── <WatchlistPanel>        # Collapsible watchlists
│   │   │   ├── <Watchlist>
│   │   │   │   └── <WatchItem>    # Ticker, price, change, sparkline
│   │   │   └── <AddWatchButton>
│   │   └── <NavigationTree>       # F2-F12 sector shortcuts
│   ├── <MainPanel>                 # Content area
│   │   ├── <SecurityView>          # AP-style security description
│   │   ├── <ChartView>             # CG-style charts
│   │   ├── <NewsFeed>              # BN-style news
│   │   ├── <PortfolioView>         # Portfolio tracker
│   │   ├── <HistoricalData>        # HP-style history table
│   │   ├── <AlertsView>            # Manage price alerts
│   │   └── <SettingsView>          # User preferences
│   └── <NewsPanel>                 # Right sidebar (optional)
│       └── <NewsItem>              # Headline + sentiment chip
├── <CommandPalette>              # Cmd+K overlay (cmdk)
├── <CommandBar>                   # Bottom bar (Bloomberg style)
└── <NotificationCenter>          # Alert toasts
```

### 5.2. Panel System

```typescript
// Panel management — resizable, splittable layout
interface Panel {
  id: string;
  type: PanelType;      // 'chart' | 'watchlist' | 'news' | 'data' | 'portfolio'
  config: Record<string, unknown>;
  size: number;          // percentage of parent
  splitAxis: 'row' | 'column';
  children?: Panel[];
}

type PanelType =
  | 'security'    // AP — security description
  | 'chart'       // CG — interactive chart
  | 'news'        // BN — news feed
  | 'portfolio'   // PP — portfolio view
  | 'history'     // HP — historical data table
  | 'alerts'      // PA — alerts management
  | 'watchlist'   // WC — watchlist panel
  | 'settings';   // user preferences
```

---

## 6. Data Architecture

### 6.1. Data Flow (MVP)

```
┌─────────────────┐     WebSocket/REST      ┌─────────────────────┐
│  Data Providers │ ◄──────────────────────► │  Backend API        │
│  (Yahoo, Alpha  │                          │  (FastAPI)          │
│   Vantage, etc.)│                          │                     │
└─────────────────┘                          │  ┌───────────────┐  │
                                              │  │ Data Adapters │  │
┌─────────────────┐     REST                 │  │ (pluggable   │  │
│  Frontend App   │ ──REST/SSE─────────────►│  │  provider    │  │
│  (React/Vite)   │◄────WebSocket───────────│  │  pattern)    │  │
└─────────────────┘                          │  └──────┬────────┘  │
                                              │         │           │
                                              │  ┌──────┴────────┐  │
                                              │  │ TimescaleDB   │  │
                                              │  │ (price history)│  │
                                              │  └───────────────┘  │
                                              │  ┌───────────────┐  │
                                              │  │ PostgreSQL    │  │
                                              │  │ (users, prefs) │  │
                                              │  └───────────────┘  │
                                              └─────────────────────┘
```

### 6.2. Free Data Providers (MVP)

| Provider | Coverage | Rate Limit | Use For |
|---|---|---|---|
| **Yahoo Finance** (yfinance) | Equities, FX, Crypto | Generous | Delayed 15-min quotes, daily history |
| **Alpha Vantage** | Equities, FX, Crypto | 5 calls/min (free) | Technical indicators, intraday |
| **Polygon.io** | Equities, Options, Crypto | 1,000/day (free) | Real-time snapshots, daily aggregates |
| **Finnhub** | Equities, News, Sentiment | 60/60 (free) | Real-time quotes, news feed |
| **Twelve Data** | Equities, Crypto, FX | 800/day (free) | Charts, technical analysis |
| **SEC EDGAR** | Filings | Unlimited | 13F, 10-K, 10-Q data |
| **Stooq** | Historical | Unlimited | Long-term price history (CSV) |
| **FRED** | Economics | Generous | Macro data, rates |
| **CoinGecko** | Crypto | 10/min | Crypto prices, market cap |

### 6.3. Real-Time Data Strategy

| Approach | Description | Trade-off |
|---|---|---|
| **Polling (MVP)** | WebSocket connection polls free APIs every 5–30s | Simple, rate-limited |
| **SSE (Phase 1.5)** | Server-Sent Events for one-way streaming | Better UX, needs server push |
| **WebSocket fan-out (Phase 2)** | Paid real-time feeds (IEX Cloud, Databento) | True real-time, costs money |
| **Community relay (Phase 3)** | Users with paid data share via relay nodes | Decentralized, trust model |

---

## 7. Command System

### 7.1. Command Syntax

```
<TICKER> <FUNCTION>              # Quick execute
<FUNCTION> <PARAMS>             # Function with parameters
BLOOM <QUERY>                     # Universal search
HELP <TOPIC>                       # Inline help
```

### 7.2. MVP Function Codes

| Code | Function | Description |
|---|---|---|
| `AP` | Security Description | Full security fact sheet |
| `CG` | Chart | Interactive chart with indicators |
| `HP` | Historical Pricing | Downloadable price history |
| `WC` | Watchlist | Create/manage watchlists |
| `PA` | Price Alert | Set/remove price alerts |
| `BN` | Bloomberg News | News feed |
| `CN` | Corporate News | Security-specific news |
| `PP` | Portfolio | Portfolio tracker |
| `DVDF` | Dividends | Dividend history |
| `GL` | Global List | Security search |
| `CALC` | Calculator | Financial calculator |
| `EFP` | Earnings Calendar | Upcoming earnings |
| `RAT` | Ratios | Fundamental ratios |
| `RC` | Correlation | Return correlation matrix |
| `SPC` | Peer Comparison | Compare peer companies |

### 7.3. Command Palette Design

```typescript
interface Command {
  id: string;
  label: string;            // Display label
  description: string;      // Help text
  keystrokes?: string;      // Keyboard shortcut
  category: CommandCategory;
  handler: (args: CommandArgs) => void;
  requiresTicker?: boolean;
  icon: React.ComponentType;
}

type CommandCategory =
  | 'security'    // AP, SD, EQS
  | 'chart'       // CG, CAG
  | 'data'        // HP, WM
  | 'news'        // BN, CN, NLS
  | 'portfolio'   // PP, PB
  | 'alerts'      // PA
  | 'watchlist'   // WC
  | 'analytics'   // FA, RC, CALC
  | 'system';     // Settings, help, theme
```

---

## 8. Charting Engine

### 8.1. Chart Features (MVP)

| Feature | Description |
|---|---|
| **Types** | Candlestick, line, bar, area, volume |
| **Timeframes** | 1m, 5m, 15m, 1h, 4h, 1d, 1w, 1mo |
| **Overlays** | SMA, EMA, Bollinger Bands, envelope |
| **Indicators** | RSI, MACD, Stochastic, ATR, VWAP |
| **Drawing** | Trendlines, horizontal lines, Fibonacci |
| **Comparatives** | Overlay another security or index |
| **Crosshair** | Price/time inspection on hover |
| **Export** | PNG, SVG, CSV data export |
| **Annotations** | User notes on chart points |

### 8.2. Charting Library Choice

```
Primary: Lightweight Charts (TradingView)
  ✓ High performance (canvas/WebGL)
  ✓ Candlestick, volume, moving averages
  ✓ Touch-friendly, responsive
  ✓ Permissive license (Apache 2.0)
  ✗ Limited customization for advanced overlays

Fallback for custom charts: D3.js
  ✓ Full customization
  ✗ Manual performance optimization needed

Phase 2: Consider Plotly.js or Chart.js for analytics charts
```

---

## 9. Implementation Phases

### Phase 1: Foundation (Weeks 1–3)

**Goal**: Scaffold, auth, basic data display

| Week | Deliverable |
|---|---|
| **1** | Project scaffolding (Vite + React + TypeScript), component library setup (Tailwind + Radix UI), panel layout system, command bar UI |
| **2** | Backend API (FastAPI scaffold), data adapter layer (Yahoo Finance + Finnhub), security search (GL), security description (AP), user auth (Better Auth) |
| **3** | Real-time polling engine, watchlist panel with live updates, basic chart (CG) with Lightweight Charts, news feed (BN) |

**Acceptance Criteria**:
- [ ] User can sign up and log in
- [ ] User can search for a ticker and see a security description page
- [ ] User can add tickers to a watchlist with live-updating prices
- [ ] User can view a basic candlestick chart with volume
- [ ] User can see a news feed with headlines
- [ ] `docker compose up` starts a fully functional instance

### Phase 2: Core Terminal (Weeks 4–6)

**Goal**: Bloomberg-like command system, charts, data

| Week | Deliverable |
|---|---|
| **4** | Command palette (cmdk), function code parser, keyboard shortcuts (F2–F12), historical data table (HP) with CSV export |
| **5** | Chart indicators (SMA/EMA/RSI/MACD/Bollinger), chart overlays, multiple chart types, portfolio tracker (PP) — import holdings via CSV |
| **6** | Price alerts (PA) with browser notifications, dividend history (DVDF), earnings calendar (EFP), fundamental ratios (RAT), responsive layout polish |

**Acceptance Criteria**:
- [ ] Command palette opens with Cmd+K, executes any function
- [ ] Charts support 5+ indicators with configurable parameters
- [ ] Users can import a portfolio and see P&L tracking
- [ ] Price alerts trigger browser notifications
- [ ] Layout adapts cleanly from mobile to ultrawide displays
- [ ] Dark theme looks polished (Bloomberg aesthetic)

### Phase 3: Polish & Launch (Weeks 7–9)

**Goal**: Refine UX, performance, docs, launch readiness

| Week | Deliverable |
|---|---|
| **7** | Panel split/rename, drag-and-drop resizing, layout save/load, user preferences (theme, default layout, time zone), security master improvements (better ticker resolution) |
| **8** | Performance optimization (virtualized lists, chart data pagination, WebSocket batching), PWA support (installable), keyboard navigation throughout, accessibility audit (WCAG AA) |
| **9** | Documentation (README, quickstart, API docs), Docker self-host guide, contributing guide, test coverage (E2E with Playwright, unit with Vitest), demo data mode (works without API keys) |

**Acceptance Criteria**:
- [ ] First-time user can go from clone → working terminal in <5 minutes
- [ ] All major interactions support keyboard-only navigation
- [ ] E2E tests cover critical paths (auth, search, watchlist, chart, portfolio)
- [ ] Demo mode shows the app with no API keys configured
- [ ] Lighthouse score >90 on performance, accessibility, best practices

### Phase 4: Community & Ecosystem (Weeks 10–12)

**Goal**: Open governance, extensibility, community onboarding

| Week | Deliverable |
|---|---|
| **10** | Plugin system (user-defined data connectors via TypeScript SDK), custom watchlist sharing, community forum/discord setup |
| **11** | API key management UI (users configure their own data providers), rate limit dashboard, data quality indicators (source freshness badges) |
| **12** | v0.1.0 release, GitHub release notes, blog post, outreach to r/algotrading, r/opensource, Hacker News |

**Acceptance Criteria**:
- [ ] Anyone can write a data connector plugin in <200 lines of TypeScript
- [ ] Users can self-configure data sources without touching code
- [ ] Project has clear CONTRIBUTING.md, CODE_OF_CONDUCT.md, governance model
- [ ] v0.1.0 release is demo-ready on video

---

## 10. Repository Structure

```
openberg-terminal/
├── apps/
│   ├── web/                    # React + Vite frontend
│   │   ├── src/
│   │   │   ├── components/     # UI components
│   │   │   │   ├── layout/    # Panels, sidebar, command bar
│   │   │   │   ├── charts/    # Chart components
│   │   │   │   ├── tables/    # Data tables
│   │   │   │   ├── command-palette/
│   │   │   │   └── ui/        # Shared primitives
│   │   │   ├── features/       # Feature slices
│   │   │   │   ├── watchlist/
│   │   │   │   ├── security/
│   │   │   │   ├── chart/
│   │   │   │   ├── portfolio/
│   │   │   │   ├── news/
│   │   │   │   ├── alerts/
│   │   │   │   └── settings/
│   │   │   ├── hooks/          # Custom React hooks
│   │   │   ├── store/          # Zustand stores
│   │   │   ├── lib/          # Utilities, formatters
│   │   │   ├── types/        # TypeScript types
│   │   │   ├── App.tsx
│   │   │   └── main.tsx
│   │   ├── index.html
│   │   ├── tailwind.config.ts
│   │   ├── vite.config.ts
│   │   └── package.json
│   └── server/                  # FastAPI backend
│       ├── app/
│       │   ├── api/           # API routes
│       │   ├── adapters/      # Data provider adapters
│       │   ├── models/        # Pydantic models
│       │   ├── services/      # Business logic
│       │   ├── workers/       # Async tasks (Celery/ARQ)
│       │   └── main.py
│       ├── requirements.txt
│       └── Dockerfile
├── packages/
│   ├── shared/                # Shared types (TS ↔ Python)
│   ├── plugin-sdk/          # Data connector SDK
│   └── config/              # Shared ESLint, TS config
├── infra/
│   ├── docker-compose.yml   # Full stack
│   ├── docker-compose.dev.yml
│   ├── .env.example
│   └── k8s/                  # Phase 2 Kubernetes manifests
├── docs/                       # Documentation
├── tools/                       # Scripts, seed data, testing
├── .github/
│   ├── workflows/            # CI/CD
│   └── CODEOWNERS
├── package.json                # Root (pnpm workspaces)
├── pnpm-workspace.yaml
├── SPEC.md                       # Feature specification
└── MVP_PLAN.md                   # This document
```

---

## 11. Data Connector Plugin System

### 11.1. Plugin Interface

```typescript
// packages/plugin-sdk/src/types.ts

interface DataConnector {
  id: string;                    // 'yahoo', 'finnhub', 'polygon'
  name: string;
  version: string;
  capabilities: ConnectorCapability[];

  // Core methods
  searchSecurity(query: string): Promise<Security[]>;
  getSecurityDescription(oid: string): Promise<SecurityDetail>;
  getQuote(ticker: string): Promise<RealTimeQuote>;
  getHistoricalPrices(params: HistoryParams): Promise<PriceBar[]>;
  getDividends(ticker: string): Promise<Dividend[]>;

  // Optional
  getNews?(ticker?: string): Promise<NewsItem[]>;
  getOptionsChain?(ticker: string): Promise<OptionContract[]>;
  getFundamentals?(ticker: string): Promise<FinancialStatements>;
}

type ConnectorCapability =
  | 'quotes'
  | 'history'
  | 'options'
  | 'news'
  | 'dividends'
  | 'fundamentals'
  | 'search'
  | 'realtime';
```

### 11.2. Adapter Aggregation Pattern

```
User Request → Router → [Yahoo ┐
                                 ├── Results → Normalizer → User
                            [Finnhub ┼
                                 ├── (fallback chain)
                            [Polygon ┘
```

- **Fallback chain**: If primary source fails or rate-limits, tries next adapter
- **Normalization**: All adapters return the same normalized schema
- **User-configurable**: Users prioritize their own adapters based on API keys

---

## 12. Security & Privacy

| Concern | Approach |
|---|---|
| **API Keys** | Stored encrypted in PostgreSQL (AES-256), never logged |
| **Auth** | JWT sessions, HTTP-only cookies, CSRF protection |
| **Rate Limiting** | Per-user rate limits, Redis-based sliding window |
| **XSS** | React auto-escapes, CSP headers, no `dangerouslySetInnerHTML` |
| **CSRF** | SameSite cookies, custom headers for API calls |
| **Self-host** | No telemetry by default, opt-in analytics only |
| **Data** | Users own their data — export/delete all |

---

## 13. Key Metrics (MVP Success Criteria)

| Metric | Target |
|---|---|
| **First paint** | <1.5s on mid-range laptop |
| **Chart render** | <100ms for 1,000 candles |
| **Watchlist update** | <3s from source data to UI |
| **Command palette open** | <50ms |
| **Lighthouse score** | >90 performance, >90 accessibility |
| **Test coverage** | >80% unit, >70% E2E on critical paths |
| **Self-host time** | Clone to running in <5 minutes |
| **Demo mode** | Functional with zero configuration |

---

## 14. Team Roles (Minimal Team)

| Role | Responsibility | Count |
|---|---|---|
| **Frontend Lead** | React components, charts, command system | 1–2 |
| **Backend Lead** | API, data adapters, WebSocket, auth | 1 |
| **UI/UX Designer** | Bloomberg aesthetic, responsive layouts, accessibility | 1 (part-time) |
| **DevOps** | Docker, CI/CD, self-host experience | 0.5 (shared) |
| **Community** | Docs, onboarding, first users | 1 (maintainer) |

---

## 15. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Free data APIs rate-limit or change** | Core data broken | Multi-adapter fallback, user-supplied API keys, demo mode |
| **Yahoo Finance blocks scraping** | Primary data source lost | Finnhub + Polygon as primary, Yahoo as fallback |
| **Real-time feels sluggish** | Poor UX | SSE upgrade path, optimistic UI updates, loading states |
| **Chart performance on large datasets** | Slow rendering | Virtualized rendering, data pagination, WebGL fallback |
| **Scope creep** | Never ships | Strict MVP scope, clear Phase 2+ backlog, community-driven prioritization |
| **Legal: data redistribution** | Takedown | Display only, no caching of proprietary data, user-provided keys |
| **Adoption** | No users | Target r/algotrading, r/opensource, Hacker News, indie hacker communities |

---

## 16. Milestone Timeline

```
Week 1  ██████████ Scaffold + Layout + Command Bar UI
Week 2  ██████████ Backend + Data Adapters + Auth + AP
Week 3  ██████████ Polling + Watchlist + Basic Chart + News
        ────────── Phase 1 Complete: Basic terminal works ──────────
Week 4  ██████████ Command Palette + Function Codes + HP
Week 5  ██████████ Chart Indicators + Portfolio Tracker
Week 6  ██████████ Alerts + Dividends + Earnings + Ratios
        ────────── Phase 2 Complete: Terminal feels real ──────────
Week 7  ██████████ Layout polish + Preferences + Security master
Week 8  ██████████ Performance + PWA + Keyboard nav + A11y
Week 9  ██████████ Docs + Tests + Demo mode
        ────────── Phase 3 Complete: Launch-ready ──────────
Week 10 ██████████ Plugin SDK + Sharing + Community
Week 11 ██████████ API key UI + Rate limits + Data quality
Week 12 ██████████ v0.1.0 Release + Outreach
        ────────── Phase 4 Complete: Public launch ──────────
```

---

## 17. Post-MVP Roadmap (Quarter 2)

| Feature | Priority |
|---|---|
| **Options chain viewer** with Greeks | High |
| **iB messaging** (Matrix-based) | High |
| **Screener** — filter by P/E, volume, RSI, etc. | High |
| **Technical analysis** — drawing tools, Fibonacci | Medium |
| **Paper trading** — simulated orders | Medium |
| **Custom alerts** — Python-expression conditions | Medium |
| **Mobile app** — React Native wrapper | Medium |
| **Real-time data upgrade path** — paid connectors | Low |
| **Social features** — shared watchlists, annotations | Low |
| **Excel/Sheets add-in** | Low |

---

*Generated: 2026-05-16*
*Status: Draft v1.0 — Ready for team review*
*Decision needed: Start with Phase 1 Week 1 scaffolding?*
