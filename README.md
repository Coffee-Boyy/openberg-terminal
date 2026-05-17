# OpenBerg Terminal

An open-source alternative to the Bloomberg Terminal — a browser-based financial terminal for real-time market data, analytics, and portfolio tracking.

## Why OpenBerg

The Bloomberg Terminal costs $24,000–$30,000 per seat per year and is accessible only through proprietary hardware and closed-source software. OpenBerg delivers the same core experience — real-time market data, interactive charting, watchlists, news aggregation, and portfolio tracking — as a free, open-source, self-hostable application.

| | Bloomberg Terminal | OpenBerg |
|---|---|---|
| Cost | $24,000–$30,000/year | Free |
| License | Closed-source | Open-source (MIT) |
| Hardware | Proprietary keyboard | Any browser |
| Deployment | Bloomberg-only | Self-hosted or cloud |
| Data | Proprietary feeds | Open sources + community |
| API | BLPAPI (licensed) | Open REST + WebSocket |

## Features (MVP)

- **Command Palette** — Bloomberg-style command bar: type a ticker and function, press Enter
- **Real-Time Watchlists** — Persistent watchlists with live price updates via polling and WebSocket
- **Interactive Charts** — Candlestick and line charts with overlays (SMA, EMA, RSI, MACD, Bollinger Bands)
- **News Feed** — Aggregated financial news with sentiment tagging
- **Portfolio Tracker** — Track holdings, cost basis, and P&L
- **Price Alerts** — Configurable alerts for price thresholds and percentage changes
- **Security Search** — Universal search across tickers, companies, and indices
- **Dark Theme** — Bloomberg-inspired black/green aesthetic with light mode toggle
- **Demo Mode** — Full functionality with zero configuration — no API keys required

## Architecture

```
┌─────────────────┐     REST/WS        ┌─────────────────────┐
│  Frontend App   │ ──────────────────► │  Backend API        │
│  React + Vite   │ ◄───────────────── │  FastAPI + Python   │
│  TypeScript     │   WebSocket push   │  SQLAlchemy + SQLite│
└─────────────────┘                    └────────┬────────────┘
                                               │
                                          ┌────┴─────┐
                                          │ Adapters │
                                          │ pluggable│
                                          └────┬─────┘
                                               │
                                 ┌───────────┬┼───────────┐
                                 │         ││           │
                            ┌──────┐  ┌────┐  ┌──────┐
                            │Finnhub│  │Yahoo│  │Mock  │
                            └──────┘  └────┘  └──────┘
```

The backend uses a pluggable adapter pattern for data providers. By default it falls back to a built-in mock adapter so the terminal works out of the box. Connect a Finnhub or Yahoo Finance API key for real market data.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Zustand |
| Backend | FastAPI, Pydantic, SQLAlchemy, SQLite |
| Data Providers | Finnhub, Yahoo Finance, Mock (built-in) |
| Container | Docker + docker-compose |
| Package Manager | pnpm (monorepo workspaces) |

## Quick Start

### Prerequisites

- Node.js >= 20
- pnpm >= 9
- Python >= 3.13 (with `uv` for the server)

### Development

```bash
# Clone and install
git clone https://github.com/openberg-terminal/openberg-terminal.git
cd openberg-terminal
pnpm install

# Start the dev servers
pnpm dev
```

This starts the Vite frontend (port 3000) and FastAPI backend (port 8000) in development mode. The frontend auto-proxies `/api/*` requests to the backend.

### Server-only (manual)

```bash
cd apps/server
uv run uvicorn app.main:app --reload --port 8000
```

### Docker

```bash
docker compose up -d
```

Opens on `http://localhost:3000`.

### API Keys (optional)

Set `OPENBERG_FINNHUB_API_KEY` for real market data. Without any keys, the built-in mock adapter provides demo data that exercises every feature.

```bash
OPENBERG_FINNHUB_API_KEY=your_key_here uv run uvicorn app.main:app --reload --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/securities?q=AAPL` | Search securities |
| GET | `/api/securities/{ticker}` | Security details |
| GET | `/api/quotes?tickers=AAPL,GOOG` | Real-time quotes |
| GET | `/api/prices/{ticker}?interval=1d&count=200` | Historical prices |
| GET | `/api/news?ticker=AAPL&limit=50` | News feed |
| GET | `/api/dividends/{ticker}` | Dividend history |
| GET | `/api/watchlist` | List watchlist |
| POST | `/api/watchlist` | Add to watchlist |
| DELETE | `/api/watchlist?ticker=AAPL` | Remove from watchlist |
| GET | `/api/portfolio` | Portfolio positions |
| GET | `/api/portfolio/summary` | Portfolio summary (P&L) |
| POST | `/api/portfolio` | Add position |
| PATCH | `/api/portfolio/{ticker}/price` | Update price |
| DELETE | `/api/portfolio?ticker=AAPL` | Remove position |
| GET | `/api/alerts` | List alerts |
| POST | `/api/alerts` | Create alert |
| DELETE | `/api/alerts?alert_id=1` | Remove alert |

## Project Structure

```
openberg-terminal/
├── apps/
│   ├── web/                    # React + Vite frontend
│   │   ├── src/
│   │   │   ├── components/     # UI components
│   │   │   ├── features/       # Feature slices (alerts, portfolio, etc.)
│   │   │   ├── hooks/         # Custom React hooks
│   │   │   ├── store/         # Zustand stores
│   │   │   ├── services/      # API client, demo data
│   │   │   ├── types/         # TypeScript types
│   │   │   └── utils/         # Utilities
│   │   └── tests/           # Playwright E2E tests
│   └── server/                  # FastAPI backend
│       ├── app/
│       │   ├── adapters/      # Pluggable data providers
│       │   ├── models/        # Pydantic schemas
│       │   ├── services/      # Business logic
│       │   └── main.py       # FastAPI entry point
│       └── tests/           # pytest test suite
├── docker-compose.yml         # Full stack compose file
├── SPEC.md                     # Feature specification
├── MVP_PLAN.md                  # MVP implementation plan
└── BACKEND_PLAN.md            # Backend integration plan
```

## Roadmap

| Phase | Scope |
|---|---|
| **Phase 1** (done) | Terminal UI, command bar, watchlists, charts, news, mock data, Docker |
| **Phase 2** | Options chain viewer, screener, technical analysis tools, paper trading |
| **Phase 3** | Fixed income, derivatives, FX module, iB messaging, mobile apps |
| **Phase 4** | API gateway, compliance, custom connectors, institutional features |

See [SPEC.md](SPEC.md) for the full feature specification and [MVP_PLAN.md](MVP_PLAN.md) for the implementation timeline.

## License

MIT — see [LICENSE](LICENSE) for details.
