# OpenBerg Terminal — Feature Specification

## 1. Overview

### 1.1. Purpose

The Bloomberg Terminal is the de facto professional-grade financial information platform used by ~325,000+ subscribers globally. It combines real-time market data, news, analytics, communications, trade execution, portfolio/risk management, and regulatory reporting into a single integrated interface — accessible via proprietary hardware or software clients.

OpenBerg is an open-source alternative that aims to provide equivalent functionality for retail traders, analysts, students, and independent institutions. This document enumerates every known Bloomberg Terminal capability and maps it to an implementation target for OpenBerg.

### 1.2. Core Philosophy

| Principle | Description |
|---|---|
| **Unified** | All financial data, tools, and communication in one interface |
| **Real-time** | Streaming market data with sub-second latency |
| **Discoverable** | Command-line + GUI with instant search and function key shortcuts |
| **Extensible** | APIs, custom scripts, third-party integrations, SDKs |
| **Cross-platform** | Desktop, web, mobile, and headless (CLI/SSH) access |
| **Open** | No vendor lock-in, transparent pricing, community-driven data feeds |

### 1.3. Pricing Benchmark

| Product | Approximate Cost |
|---|---|
| Bloomberg Terminal (single seat) | \$24,000–\$30,000/year |
| Bloomberg Mobile | Included with terminal subscription |
| Bloomberg Data (API-only) | Varies, typically \$10,000+ |
| **OpenBerg Target** | Free core + optional paid data tiers |

---

## 2. Hardware & Input Devices

### 2.1. Custom Keyboard (SEA100 / Starboard)

| Feature | Description |
|---|---|
| Color-coded hotkeys | Yellow keys map directly to asset class sectors |
| Biometric fingerprint scanner | User authentication & quick session switching |
| Dedicated function keys | Menu, GO (green), Cancel (red), History, Buy, Sell, Message, News |
| Built-in speakers | Audio alerts for price/news triggers |
| Starboard (modern) | Flat chiclet keys, ergonomic |
| SEA100 (legacy) | 3 kg, 3 mm key travel |

### 2.2. Multi-Monitor Support

- Typically 2–6 displays per workstation
- Each panel/window can independently stream different functions
- Customizable layouts saved as user profiles

### 2.3. OpenBerg Hardware Target

- No proprietary hardware required
- Software hotkey layer simulates Bloomberg key layout
- Configurable JSON keymap file supports custom keyboard layouts
- Web/terminal/CLI access with responsive layout
- Optional open-source hardware keyboard design (QMK/VIA compatible)

---

## 3. Terminal Interface

### 3.1. Core UI Layout

| Element | Description |
|---|---|
| **Command Line** | Bottom-bar input: type function code + `GO` key (Enter) to execute |
| **Panels** | Up to 4 independent windows, each running a separate function |
| **Launchpad** | Persistent mini-windows (components): watchlists, inbox, calculator, news ticker, chat |
| **Dashboard (BLP)** | Customizable home screen with pinned components |
| **Status Bar** | Connection status, session info, alerts, time (UTC + local) |

### 3.2. Command Syntax

```
<TICKER> <VENUE> <SECTOR> GO
```

Examples:
- `VOD LN Equity GO` → Vodafone, London exchange, equity
- `US10Y US GO` → US 10-Year Treasury
- `EURUSD CURNCY GO` → EUR/USD forex pair

### 3.3. Panel Management

| Action | Command |
|---|---|
| Split panel horizontally | `Split Horizontal` or Ctrl+Shift+H |
| Split panel vertically | `Split Vertical` or Ctrl+Shift+V |
| Move window to dashboard | `LLP GO` |
| Auto-load dashboard at startup | `PDFB GO` |
| Close panel | `Ctrl+W` |
| Cycle through panels | Tab / Shift+Tab |
| Resize panel | Drag divider or `Ctrl+Arrow` |

---

## 4. Function Keys (Yellow Hotkeys)

| Key | Label | Sector | Description |
|---|---|---|---|
| F2 | GOVT | Government | Sovereign bonds, treasuries, central bank instruments |
| F3 | CORP | Corporate | Corporate bonds, commercial paper, structured notes |
| F4 | MTGE | Mortgage | Mortgage-backed securities, MBS, CMBS |
| F5 | M-Mkt | Money Market | T-bills, repos, commercial paper, short-term instruments |
| F6 | MUNI | Municipal | US state/local government bonds |
| F7 | PFD | Preferred | Preferred shares, hybrid securities |
| F8 | EQUITY | Equity | Common stocks, ETFs, ADRs |
| F9 | COMDTY | Commodity | Futures, options, spot commodities |
| F10 | INDEX | Index | Market indices, benchmarks, custom indices |
| F11 | CURNCY | Currency | FX spot/forward, swaps, options |
| F12 | CLIENT/ALPHA | Client | Client lists, alpha models, custom tools |

---

## 5. Function Codes (Screens)

### 5.1. Security Description & Profiles

| Code | Name | Description |
|---|---|---|
| `AP` | Security Description | Full security details: issuer, coupon, maturity, rating, ISIN, CUSIP, FIGI |
| `SDQ` | Security Definition Query | Advanced security search across all asset classes |
| `EQS` | Equity Security | Equity-specific description page |
| `SD` | Security Descrip | Quick security identification and fact sheet |
| `GL` | Global List | Global security master search |
| `REF` | Security Reference | Corporate actions, share count, outstanding shares |

### 5.2. Market Data & Pricing

| Code | Name | Description |
|---|---|---|
| `HP` | Historical Pricing | End-of-day or intraday historical price data |
| `GP` | Quote | Real-time bid/ask/last with depth of book |
| `WM` | Where Moved | Price change analysis — which prices moved between sessions |
| `PA` | Price Alert | Set alerts on price crosses, percentage moves |
| `MP` | Market by Price | Full order book snapshot with time-and-sales |
| `LB` | Last Bid | Recent bid/ask activity |
| `LBH` | Last Bid History | Historical bid/ask series |
| `QV` | Quote View | Multi-instrument quote board |

### 5.3. Charts & Visualization

| Code | Name | Description |
|---|---|---|
| `EQD` | Equity Distribution | Shareholder distribution, ownership breakdown |
| `CG` | Chart | Interactive price chart with overlay, indicators |
| `CAG` | Chart Advanced | Multi-chart analysis, technical overlays |
| `PFD` | Portfolio Function Dashboard | Portfolio performance visualization |
| `DCC` | Discount/Coupon Curve | Yield curve construction and visualization |

### 5.4. Analytics & Models

| Code | Name | Description |
|---|---|---|
| `DVDF` | Dividend | Dividend history, yield, payout ratio, ex-dates |
| `DVD` | Dividend & Split | Dividend and stock split summary |
| `BM` | Bond Maturity | Bond maturity analysis, duration, convexity |
| `YCD` | Yield Curve | Yield curve builder for any tenor/issuer |
| `FXR` | FX Return | FX return decomposition (carry, roll, move) |
| `IM` | Implied Metrics | Implied volatility, model pricing |
| `RV` | Risk Volatility | Historical volatility, VaR, stress tests |
| `FA` | Fundamental Analysis | Financial statement analysis, ratios |
| `RC` | Returns Correlation | Cross-asset return correlation matrices |
| `SPC` | Security Price Comparison | Peer comparison pricing |

### 5.5. News & Research

| Code | Name | Description |
|---|---|---|
| `CN` | Corporate News | News filtered to specific company/security |
| `BN` | Bloomberg News | Headline news feed with categories |
| `NLS` | News Search | Full-text news search with filters |
| `RSE` | Research | Equity research reports, broker coverage |
| `EFP` | Earnings | Earnings calendar, estimates, surprises |
| `TRN` | Transcripts | Earnings call transcripts (Bloomberg Original Coverage) |
| `GOVT` | Government | Policy, central bank, regulation news |
| `FNC` | Finance Calendar | Economic calendar, data releases |

### 5.6. Portfolio & Risk

| Code | Name | Description |
|---|---|---|
| `PP` | Portfolio Performance | P&L, returns, attribution, drawdown |
| `PB` | Portfolio Builder | Portfolio construction, rebalancing |
| `PRM` | Portfolio Risk Management | VaR, sensitivity, stress tests, scenario analysis |
| `PAA` | Portfolio Analysis | Factor exposure, style box, peer comparison |
| `PMAP` | Portfolio Manager App | Full PM workflow: orders, reconciliation, reporting |
| `BPP` | Bond Portfolio Performance | Fixed-income specific performance attribution |

### 5.7. Trading & Execution

| Code | Name | Description |
|---|---|---|
| `ET` | Electronic Trading | Access to dark pools, block trading, ATS venues |
| `MKT` | Market | Live market window with execution capability |
| `TWS` | Trade Window | Order entry, order types (market, limit, stop, VWAP, TWAP) |
| `OMS` | Order Management | OMS integration, allocation, blotter |
| `EXEC` | Execution | Execution analytics, implementation shortfall, TCA |
| `LIQ` | Liquidity | Liquidity analysis, trading volume profiles |

### 5.8. Fixed Income

| Code | Name | Description |
|---|---|---|
| `BM` | Bond Maturity | Maturity grid, duration analysis |
| `BG` | Bond Grid | Bond screening across issuer, rating, maturity |
| `BC` | Bond Custom List | Custom bond watchlists |
| `YVC` | Yield Curve | Multi-currency yield curve viewer |
| `ZSPR` | Z-Spread | Z-spread calculation and charting |
| `OAS` | Option-Adjusted Spread | OAS for mortgage-backed/structured securities |
| `CS` | Credit Screen | Credit spread analysis, transition matrices |
| `CACS` | Corporate Actions | Events: mergers, buybacks, special dividends |

### 5.9. Derivatives

| Code | Name | Description |
|---|---|---|
| `OV` | Options Volatility | Volatility surface, skew, term structure |
| `OP` | Option Position | Option chain viewer, Greeks |
| `FD` | Futures Display | Futures prices, contango/backwardation |
| `SW` | Swap | Swap pricing, curves, analytics |
| `FXO` | FX Options | FX volatility, options pricing |
| `CDSD` | CDS Display | Credit default swap pricing |

### 5.10. FX

| Code | Name | Description |
|---|---|---|
| `FX` | FX Quote | Spot/forward FX quotes |
| `FXF` | FX Fundamental | Macroeconomic drivers, valuation |
| `FXR` | FX Return | Return decomposition |
| `FXNC` | FX News | Currency-specific news |
| `FXCAL` | FX Calendar | Central bank meetings, data releases |

### 5.11. Commodity & Energy

| Code | Name | Description |
|---|---|---|
| `CD` | Commodity | Commodity prices, spreads, contango |
| `EG` | Energy | Oil, gas, power, carbon, emissions |
| `AG` | Agriculture | Softs, grains, livestock, sugar, coffee |
| `MT` | Metals | Gold, silver, industrial metals |

### 5.12. Messaging & Communication

| Code | Name | Description |
|---|---|---|
| `IB` | Instant Bloomberg | Bloomberg chat — internal instant messaging |
| `IRC` | IRC Chat | IRC gateway for external chat |
| `EM` | Email | Bloomberg email client |
| `BP` | Bloomberg Chat | Proprietary chat with ~325K subscribers |
| `BIRC` | Bloomberg IRC | Public/private chat rooms |
| `GK` | Group | Distribution lists, group messaging |

### 5.13. Data Management

| Code | Name | Description |
|---|---|---|
| `DATA` | Data | Raw data feed viewer |
| `DB` | Database | Historical data query builder |
| `SF` | Saved Function | Save/reuse function configurations |
| `WC` | Watchlist | Custom watchlists with alerts |
| `CALC` | Calculator | Financial calculator (IRR, duration, option pricing) |
| `XL` | Excel | Excel feed integration |

### 5.14. Index & ETF

| Code | Name | Description |
|---|---|---|
| `IDX` | Index | Index constituents, performance, methodology |
| `ETF` | ETF | ETF pricing, flows, creation/redemption |
| `FUND` | Fund | Mutual fund pricing, NAV, holdings |
| `PMS` | Private Markets | PE/VC fundraising, exits, valuations |

### 5.15. Regulatory & Compliance

| Code | Name | Description |
|---|---|---|
| `LEI` | Legal Entity Identifier | LEI lookup, corporate structure |
| `COMPLIANCE` | Compliance | Trade surveillance, MiFID II, MAR, RFQ logs |
| `TR` | Trade Report | Trade reporting for regulatory requirements |
| `SAN` | Sanctions | Sanctions screening, watchlists |

### 5.16. Crypto & Digital Assets

| Code | Name | Description |
|---|---|---|
| `CRYPTO` | Crypto | Digital asset pricing, on-chain metrics |
| `CB` | Central Bank | CBDC research, central bank digital currency |
| `TOKEN` | Tokenization | Tokenized securities, RWAs |

### 5.17. ESG & Climate

| Code | Name | Description |
|---|---|---|
| `ESG` | ESG | ESG ratings, scores, controversies |
| `CL` | Climate | Carbon pricing, physical/transition risk |
| `SCOPE3` | Scope 3 Emissions | Emissions tracking, TCFD reporting |

### 5.18. Economics & Sovereign

| Code | Name | Description |
|---|---|---|
| `ECR` | Economics | GDP, inflation, employment data |
| `POL` | Politics | Political risk, election impacts, policy |
| `SOF` | Sovereign | Sovereign ratings, CDS, debt sustainability |

### 5.19. Index & Benchmark

| Code | Name | Description |
|---|---|---|
| `BMCH` | Benchmark | Custom benchmark construction |
| `FA` | Factor Analysis | Style factors, smart beta, factor returns |

---

## 6. Bloomberg Launchpad (Persistent Components)

### 6.1. Component Types

| Component | Description |
|---|---|
| **BLOOM** | Search overlay — searches tickers, news, IB contacts, functions |
| **WATCH** | Real-time watchlist with price, change, alerts |
| **NEWS** | Scrolling news ticker with category filters |
| **IB INBOX** | Bloomberg chat inbox, conversations, missed messages |
| **CALC** | Financial calculator with functions for bonds, options, FX |
| **ALARM** | Price, news, and event-based alerts |
| **EFP** | Earnings flow panel — real-time earnings calendar |
| **MKT IND** | Market indicators — top gainers, losers, movers, volume |
| **TASK** | Task manager — notes, to-do, meeting notes |
| **MAP** | Geospatial view — economic events by region |
| **PDF** | PDF viewer and document management |

### 6.2. Launchpad Behavior

- Components persist across sessions
- Drag-and-drop positioning and sizing
- Auto-refresh with configurable intervals
- Component state saved to user profile
- `PDFB GO` loads the Launchpad at terminal startup

---

## 7. APIs & SDK

### 7.1. BLPAPI (Bloomberg API)

| Feature | Description |
|---|---|
| **Languages** | Python, Java, C++, .NET, Perl, Wolfram Language |
| **Protocol** | Bloomberg Communication Library (BCOM) over TCP |
| **Data Types** | Reference data, historical data, intraday data, streaming |
| **Excel Add-in** | Direct Excel integration with formula-based data feeds |
| **FIGI** | Financial Instrument Global Identifier — 12-char stable ID |
| **LEI** | Legal Entity Identifier integration |

### 7.2. OpenBerg API Target

| Feature | Target |
|---|---|
| **Languages** | Python, JavaScript/TypeScript, Rust, Go, Java |
| **Protocol** | WebSocket + REST + gRPC |
| **Data Types** | Reference, historical, streaming, tick-level |
| **FIGI** | Compatible identifier system (open alternative) |
| **Authentication** | API keys + OAuth2 + mDNS for local |
| **Rate Limits** | Tiered: free (100 req/min), pro (10,000), enterprise (unlimited) |
| **SDK** | Auto-generated from OpenAPI spec |

---

## 8. Data Sources & Feeds

### 8.1. Asset Class Coverage

| Category | Instruments |
|---|---|
| **Equities** | Global stocks, ETFs, ADRs, depository receipts |
| **Government Debt** | Treasuries, sovereign bonds, central bank bills |
| **Corporate Debt** | Investment-grade, high-yield, emerging market |
| **Mortgage-Backed** | Agency MBS, CMBS, CDOs, structured products |
| **Money Market** | T-bills, repos, commercial paper, CDs |
| **Municipal** | US/CA state and local bonds |
| **Commodities** | Energy, agriculture, metals, softs, freight |
| **Currencies** | Major, minor, exotic FX pairs, forwards |
| **Indices** | Exchange indices, custom, factor-based |
| **Derivatives** | Options, futures, swaps, forwards, CFDs |
| **Crypto** | Spot, futures, on-chain, DeFi protocols |
| **Preferred** | Preferred shares, convertible notes |

### 8.2. Exchange & Venue Coverage

| Type | Examples |
|---|---|
| **Equity Exchanges** | NYSE, NASDAQ, LSE, TSE, HKEX, ASX, NSE, SX |
| **Futures Exchanges** | CME, ICE, EUREX, SHFE, TOCOM |
| **FX** | Interbank, ECNs, liquidity providers |
| **Dark Pools** | ATS venues, block trading platforms |
| **OTC** | Bonds, structured products, derivatives |
| **Alternative** | Crowdfunding, SPACs, private markets |

### 8.3. Open Data Sources (for OpenBerg)

| Source | Coverage | License |
|---|---|---|
| **Yahoo Finance** | Equities, FX, some derivatives | Free (scraper/API) |
| **Alpha Vantage** | Equities, FX, crypto, technical | Free tier |
| **Finnhub** | Equities, news, sentiment | Free tier |
| **Polygon.io** | Equities, options, crypto | Free tier |
| **Twelve Data** | Equities, crypto, forex | Free tier |
| **Stooq** | Historical prices | Free |
| **FRB/ECB/BOJ** | Central bank data | Public domain |
| **FRED** | Economic data | Public domain |
| **Coingecko/CMC** | Crypto | Free tier |
| **SEC/EDGAR** | Filings, 13F, 10-K | Public domain |
| **WSOAS** | Options chains | Exchange-provided |
| **Kaiko/Chainalysis** | On-chain data | Paid |
| **Refinitiv** | Market data | Paid |
| **Dukascopy** | Historical tick data | Free |
| **Tiingo** | Equity/dividend data | Free tier |

---

## 9. Bloomberg News Service

### 9.1. News Categories

| Category | Description |
|---|---|
| **Original Coverage (BCO)** | Bloomberg-exclusive breaking news |
| **Markets** | Real-time market-moving news |
| **Economics** | Economic data, policy, forecasts |
| **Industry** | Sector-specific reporting |
| **Government** | Sovereign debt, regulation, central bank |
| **Emerging Markets** | EM coverage, frontier markets |
| **Fixed Income** | Bond market news, rates, credit |
| **Funds** | Asset management, flows, AUM |
| **Wealth** | Private wealth, UHNWI, family offices |
| **Technology** | Fintech, market structure, RegTech |
| **ESG** | Climate, governance, sustainability |
| **Legal** | M&A litigation, antitrust, regulatory |

### 9.2. News Features

- **Headline feed** with Bloomberg original tag
- **Full article** with charts, data, references
- **Correlated securities** — click to see price impact
- **Sentiment analysis** — positive/negative/neutral scoring
- **NLP tagging** — entity extraction (companies, people, instruments)
- **RSS/Atom** export for third-party consumption
- **API access** for algorithmic trading signals

### 9.3. OpenBerg News Target

- **Aggregation**: Reuters, AP, Dow Jones, FT via aggregator APIs
- **Free sources**: Reuters.com, MarketWatch, Seeking Alpha, Benzinga
- **NLP pipeline**: Open-source entity extraction, sentiment scoring
- **Real-time feed**: WebSocket-based news delivery
- **Custom filters**: By security, sector, keyword, sentiment

---

## 10. Messaging System (iB)

### 10.1. Features

| Feature | Description |
|---|---|
| **Instant messaging** | Real-time chat with any subscriber |
| **Group chat** | Multi-party conversations |
| **IRC gateway** | External chat integration |
| **Contact list** | Searchable directory with IB numbers |
| **Presence** | Online/away/busy indicators |
| **File sharing** | Document, spreadsheet, chart sharing |
| **Encryption** | End-to-end encrypted channels |
| **Compliance** | Message archiving, e-discovery |
| **Email integration** | Send/receive email via Bloomberg |

### 10.2. OpenBerg Messaging Target

| Feature | Implementation |
|---|---|
| **Protocol** | XMPP or Matrix (open standards) |
| **Clients** | Web, desktop, mobile, CLI |
| **Encryption** | E2E via Olm/Megolm (Matrix) |
| **Compliance** | Configurable archiving to Elasticsearch |
| **Directory** | Email-based contact discovery |
| **Bridges** | Slack, Discord, Teams bridges |

---

## 11. Analytics & Quantitative Tools

### 11.1. Built-In Functions

| Tool | Description |
|---|---|
| **Calculator** | IRR, duration, convexity, option pricing, FX cross rates |
| **Regression** | Correlation, regression, factor attribution |
| **Monte Carlo** | Simulation engine for pricing and risk |
| **Scenario Analysis** | What-if modeling on portfolios |
| **Stress Testing** | Historical and hypothetical stress scenarios |
| **Attribution** | Brinson-style return attribution |
| **Optimization** | Mean-variance, Black-Litterman, risk parity |
| **Backtesting** | Strategy backtesting with historical data |
| **Portfolio Heatmap** | Sensitivity visualization |

### 11.2. Custom Analytics

- **Python notebook** integration (Jupyter)
- **Formula bar** for spreadsheet-like calculations
- **Custom indicators** — user-defined technical/fundamental metrics
- **Scripting** — Python, R, and Lua scripting environments

---

## 12. Excel Integration

### 12.1. Bloomberg Add-In

| Feature | Description |
|---|---|
| **BDH** | Bloomberg Data History — pull historical series |
| **BDP** | Bloomberg Data Point — single snapshot value |
| **BDS** | Bloomberg Data Set — structured datasets |
| **BBG** | Security search formula |
| **Real-time** | Auto-refresh feeds via COM/OLE |
| **Charts** | Embedded charting from Excel |

### 12.2. OpenBerg Target

- **OpenBerg Add-In** for Excel/Google Sheets/LibreOffice
- **Spreadsheet functions**: `=OBH()`, `=OBP()`, `=OBS()`
- **Real-time mode** via WebSocket push to spreadsheet
- **Python alternative**: `openberg-py` with pandas DataFrames

---

## 13. Historical Data & Databases

### 13.1. Data Products

| Product | Description |
|---|---|
| **Intraday** | Tick, minute, bar data with configurable granularity |
| **End-of-day** | Daily OHLCV, adjusted for splits/dividends |
| **Inception** | Securities-inception-date data |
| **Corporate Actions** | Splits, dividends, mergers, reorganizations |
| **Fundamental** | Income statements, balance sheets, cash flow |
| **Estimates** | Analyst estimates, consensus, revisions |
| **Holdings** | 13F, mutual fund, index holdings |
| **Options** | Chains, Greeks, implied vol surfaces |
| **Short Interest** | Borrow costs, availability, utilization |
| **Alternative** | Web traffic, job postings, app downloads, satellite |

### 13.2. Data Formats

| Format | Description |
|---|---|
| **CSV/TSV** | Exportable tabular data |
| **JSON** | API response format |
| **Parquet** | Columnar storage for analytics |
| **HDF5** | High-performance numeric storage |
| **Protocol Buffers** | Binary wire format for streaming |
| **Excel/Sheets** | Direct spreadsheet export |

---

## 14. Bloomberg API Architecture

### 14.1. Backend Stack

| Component | Technology |
|---|---|
| **Server** | Multiprocessor Unix (Solaris/Linux) |
| **Languages** | Fortran, C, C++ |
| **Client** | Windows application |
| **Embedded** | JavaScript for client-side operations |
| **Protocol** | BCOM (Bloomberg Communications) |
| **Context** | Proprietary session state tracking across distributed processes |

### 14.2. Access Methods

| Method | Description |
|---|---|
| **Direct IP** | Dedicated terminal session |
| **Bloomberg Anywhere** | Remote desktop / Citrix |
| **Web client** | HTML5 terminal via browser |
| **Mobile** | iOS/Android apps |
| **API** | BLPAPI SDK for programmatic access |

### 14.3. OpenBerg Architecture Target

| Component | Target |
|---|---|
| **Server** | Kubernetes cluster, gRPC microservices |
| **Languages** | Rust (core), Python (analytics), TypeScript (frontend) |
| **Client** | Electron desktop, web (React/Next.js), CLI (Rust) |
| **Mobile** | React Native or Flutter |
| **Protocol** | WebSocket (streaming), gRPC (internal), REST (public) |
| **Database** | ClickHouse (timeseries), PostgreSQL (reference), Redis (cache) |
| **Message bus** | Kafka or Redpanda |
| **Auth** | OAuth2/OIDC, API keys, mDNS for local |

---

## 15. FIGI (Financial Instrument Global Identifier)

### 15.1. FIGI Structure

| Property | Value |
|---|---|
| **Format** | 12-character alphanumeric |
| **Stability** | IDs never recycled across instrument lifecycle |
| **Uniqueness** | One FIGI per instrument across all exchanges |
| **Complement** | Complements ISIN, CUSIP, SEDOL, ticker symbols |
| **API** | FIGI can be resolved via BLPAPI reference data |

### 15.2. OpenBerg Identifier System

- **OpenBerg ID (OID)**: 12-character stable identifier
- Compatible with FIGI where Bloomberg provides it
- Open-source mapping: ISIN ↔ CUSIP ↔ SEDOL ↔ Ticker ↔ OID
- Community-maintained security master database
- Pulls from open sources: Yahoo Finance, SEC EDGAR, exchange APIs

---

## 16. Corporate Actions & Events

### 16.1. Event Types

| Type | Code | Description |
|---|---|---|
| **Dividends** | `DVD` | Cash and stock dividends |
| **Splits** | `DVD` | Forward and reverse splits |
| **Mergers** | `CACS` | M&A announcements, completions |
| **Buybacks** | `CACS` | Share repurchase programs |
| **IPOs** | `IPO` | New listings, pricing, underwriters |
| **Offerings** | `OF` | Secondary offerings, ATMs |
| **Restructuring** | `CACS` | Chapter 11, debt restructures |
| **Delistings** | `DEL` | Exchange delistings, suspensions |
| **Rating Changes** | `RAT` | Credit rating upgrades/downgrades |
| **Estimates** | `EFP` | Analyst estimate revisions |

---

## 17. Yield Curve & Rates

### 17.1. Curve Construction

| Component | Description |
|---|---|
| **Bootstrapping** | Zero curve from par coupons |
| **Interpolation** | Spline, logarithmic, natural cubic |
| **Extrapolation** | Flat forward, key rate, decay |
| **Multi-currency** | Cross-currency basis, FX forwards |
| **Historical** | Curve snapshots, curve shifts |

### 17.2. Rate Instruments

| Instrument | Description |
|---|---|
| **OIS** | Overnight index swap curve |
| **SOFR** | Secured overnight financing rate |
| **SONIA** | Sterling overnight index average |
| **€STR** | Euro short-term rate |
| **Term rates** | Term SOFR, term STR, term €STR |
| **Forward curves** | Forward rate agreements, futures-implied |

---

## 18. Portfolio Management

### 18.1. Portfolio Operations

| Operation | Description |
|---|---|
| **Import/Export** | CSV, XBRL, SWIFT MT/MSG, FIX |
| **Reconciliation** | Auto-reconcile against custodians |
| **P&L** | Realized/unrealized, currency impact |
| **Attribution** | Brinson, style, sector, factor |
| **Performance** | Time-weighted, money-weighted returns |
| **Benchmarking** | Against indices, custom benchmarks |
| **Risk** | VaR, CVaR, stress, scenario |
| **Cash management** | Cash drag, sweeps, collateral |
| **Order management** | OMS integration, allocation |
| **Compliance** | Pre-trade, restrictions, watchlists |

### 18.2. Reporting

| Report | Description |
|---|---|
| **Client statements** | Customizable PDF/Excel output |
| **NAV** | Daily fund valuation |
| **Trade blotter** | Executed trades with P&L |
| **Exposure** | Concentration, sector, geographic |
| **Turnover** | Trading activity, capacity analysis |
| **Regulatory** | AIFMD, Dodd-Frank, UCITS |

---

## 19. Search & Discovery

### 19.1. BLOOM (Universal Search)

| Input | Searches Across |
|---|---|
| **Ticker** | Security master, all exchanges |
| **Company name** | Corporate reference, news |
| **IB number** | iB contacts, chat history |
| **Function code** | Terminal screens, help |
| **News keyword** | Full-text article search |
| **Topic** | Economic events, themes |

### 19.2. Search Features

- **Fuzzy matching** for misspellings
- **Autocomplete** with most-used functions
- **Contextual results** — recent searches prioritized
- **Saved searches** as reusable watchlists
- **Natural language** — "Show me all US investment-grade bonds maturing in 2028"

---

## 20. Alerts & Notifications

### 20.1. Alert Types

| Type | Trigger |
|---|---|
| **Price** | Absolute price, percentage change, ATR breach |
| **Volume** | Unusual volume spikes, volume profile |
| **News** | Keyword alerts, sentiment shifts |
| **Earnings** | Earnings beats/misses, guidance |
| **Technical** | Moving average crosses, pattern completion |
| **Fundamental** | Ratio changes, revenue surprises |
| **Macro** | Economic data releases, rate decisions |
| **Custom** | User-defined conditions, Python expressions |

### 20.2. Delivery Channels

- In-terminal (Launchpad notification)
- Email
- SMS
- Push notification (mobile)
- Webhook (for automated trading)

---

## 21. Customization & User Profiles

### 21.1. User Configuration

| Feature | Description |
|---|---|
| **Themes** | Light, dark, Bloomberg-classic (black/green) |
| **Layouts** | Saved panel configurations |
| **Hotkeys** | Custom key bindings, per-function |
| **Watchlists** | Named, shared, or personal |
| **Favorites** | Pinned functions, quick access |
| **Preferences** | Data formats, locales, time zones |
| **Profiles** | Per-user or team-level settings |

### 21.2. Multi-User Features

| Feature | Description |
|---|---|
| **Teams** | Shared workspaces, shared watchlists |
| **Admin** | User management, permissions |
| **Audit** | Login history, data access logs |
| **SSO** | SAML/OIDC integration |
| **RBAC** | Role-based access control |

---

## 22. Regulatory & Compliance

### 22.1. Regulatory Features

| Feature | Description |
|---|---|
| **Message archiving** | MiFID II, MAR, SEC Rule 17a-4 |
| **Trade reporting** | MiFID II RTS 2, SEC Rule 613 |
| **Surveillance** | Algorithmic trading surveillance |
| **Best execution** | ATS reporting, implementation shortfall |
| **KYC/AML** | Customer due diligence, transaction monitoring |
| **Sanctions** | OFAC, UN, EU sanctions screening |
| **Tax reporting** | FATCA, CRS, Form 1099 |
| **LEI** | Legal Entity Identifier lookup |

### 22.2. OpenBerg Compliance Target

- **Open-source archiving** to Elasticsearch/S3
- **Regulation-agnostic** — user selects applicable ruleset
- **Audit trail** — immutable log of all terminal actions
- **Export** — regulatory reports in required formats

---

## 23. Bloomberg Intelligence & Research

### 23.1. Research Products

| Product | Description |
|---|---|
| **Equity Research** | Bloomberg original analyst coverage |
| **Strategy** | Macro strategy, asset allocation research |
| **Intelligence** | Bloomberg Intelligence (BI) reports |
| **Economic Research** | Forecasts, economic models |
| **Fixed Income Research** | Rates, credit, EM strategy |
| **Quantitative** | Factor models, smart beta research |

### 23.2. OpenBerg Research Target

- **Aggregated research**: Broker reports via subscription
- **Community**: Crowdsourced analysis, Seeking Alpha-style
- **Quantitative**: Open-source factor research, academic papers
- **Macro**: FRED, OECD, World Bank data aggregation

---

## 24. Bloomberg NEXT

### 24.1. Description

Bloomberg NEXT is a ~$100 million multi-year overhaul of the Terminal UI focused on:

- Improved feature discoverability
- Modern UI/UX with better search
- Component-based architecture
- Improved onboarding for new users
- Better mobile experience

### 24.2. OpenBerg Approach

OpenBerg starts from a modern, component-based architecture:

- **Progressive web app** with offline support
- **Drag-and-drop dashboard** as primary interface
- **Command palette** (Cmd+K style) for function discovery
- **Responsive design** for all screen sizes
- **Accessibility** — WCAG 2.1 AA compliant

---

## 25. Enterprise Features

### 25.1. Deployment Options

| Feature | Bloomberg | OpenBerg Target |
|---|---|---|
| **On-premise** | Bloomberg Local | Self-hosted Docker/K8s |
| **Cloud** | Bloomberg Cloud | Public cloud, managed service |
| **Hybrid** | Mixed deployment | K8s with edge nodes |
| **API-first** | BLPAPI | REST + WebSocket + gRPC |

### 25.2. Enterprise Integrations

| Integration | Description |
|---|---|
| **Algo** | Algorithmic trading strategies |
| **Bloomberg Message API** | Programmatic chat access |
| **Bloomberg Subscription API** | Streaming subscriptions |
| **SSE** | Bloomberg's event system |
| **FIX** | Financial Information eXchange |
| **SWIFT** | Payment messaging |
| **Refinitiv** | Cross-vendor data |

---

## 26. Technical Implementation Plan

### 26.1. Phase 1 — Core Infrastructure

| Component | Description | Status |
|---|---|---|
| **Terminal UI** | Web-based interface, command line | To build |
| **Data connectors** | Yahoo Finance, Alpha Vantage, Polygon.io | To build |
| **Command engine** | Function code parser and router | To build |
| **Security master** | Ticker resolution, identifier mapping | To build |
| **Watchlists** | Real-time tracking panels | To build |
| **News aggregator** | Multi-source news feed | To build |

### 26.2. Phase 2 — Analytics & Messaging

| Component | Description | Status |
|---|---|---|
| **Charting engine** | Interactive charts with indicators | To build |
| **Portfolio module** | P&L, attribution, risk | To build |
| **iB messaging** | XMPP/Matrix-based chat | To build |
| **Historical data** | Intraday/Historical data queries | To build |
| **Alerts** | Price, news, volume alerts | To build |

### 26.3. Phase 3 — Advanced Features

| Component | Description | Status |
|---|---|---|
| **Fixed income** | Bond analytics, yield curves | To build |
| **Options** | Volatility surfaces, Greeks | To build |
| **FX module** | Spot/forward, crosses | To build |
| **Derivatives** | Futures, swaps, structured | To build |
| **Excel integration** | Spreadsheet add-in | To build |
| **Mobile apps** | iOS/Android clients | To build |

### 26.4. Phase 4 — Enterprise

| Component | Description | Status |
|---|---|---|
| **API gateway** | Rate-limited public API | To build |
| **Compliance** | Message archiving, trade surveillance | To build |
| **Admin** | Multi-tenant, SSO, RBAC | To build |
| **Custom data** | User-defined connectors | To build |
| **Research** | Broker integration, community | To build |

---

## 27. Key Differentiators vs. Bloomberg

| Dimension | Bloomberg | OpenBerg |
|---|---|---|
| **Cost** | \$24,000–\$30,000/year | Free–\$50/month |
| **Data** | Proprietary, comprehensive | Open sources + community |
| **Code** | Closed-source | Open-source (MIT/Apache 2.0) |
| **Hardware** | Proprietary keyboard | Any device |
| **API** | BLPAPI (licensed) | Open APIs |
| **Community** | N/A | Community-driven features |
| **Transparency** | Black-box models | Open models, reproducible |
| **Customization** | Limited | Unlimited (code access) |
| **Deployment** | Bloomberg-only | Self-hosted or cloud |
| **Maturity** | 40+ years | New |

---

## 28. OpenBerg Command Set

### 28.1. Command Syntax

```
<FUNCTION_CODE> GO        # Execute a function
<TICKER> <FUNCTION> GO    # Execute on a security
<TICKER> GO                # Quick lookup
BLOOM <QUERY>              # Universal search
HELP <FUNCTION>            # Function help
SF <FUNCTION>              # Save current function
WC <NAME> <TICKERS>        # Create watchlist
PA <CONDITION>             # Set price alert
```

### 28.2. Command Categories

| Prefix | Category |
|---|---|
| `A*` | Analytics, attribution |
| `B*` | Bonds, Bloomberg functions |
| `C*` | Charts, commodities, corporate |
| `D*` | Data, dividends, derivatives |
| `E*` | Equities, earnings, economy |
| `F*` | FX, funds, fundamentals |
| `G*` | Government, global lists |
| `H*` | History, help, heatmaps |
| `I*` | Indices, implied metrics |
| `M*` | Markets, messaging |
| `N*` | News, NAV |
| `O*` | Options, orders |
| `P*` | Portfolio, pricing |
| `R*` | Research, risk, returns |
| `S*` | Security, search, swaps |
| `T*` | Trading, technical |
| `W*` | Watchlists, where moved |
| `Y*` | Yield, y-o-y |

---

## 29. Data Models

### 29.1. Core Entities

```
Security {
  oid:         string(12)    # OpenBerg ID
  ticker:      string       # Exchange-specific ticker
  isin:        string(12)   # International Security Identification Number
  cusip:       string      # US security identifier
  sedol:       string(7)   # UK security identifier
  name:        string      # Security name
  type:        enum        # equity/bond/derivative/fx/crypto/...
  exchange:    string      # Trading venue
  currency:    string(3)   # ISO 4217
  sector:      string      # GICS sector
  industry:    string      # GICS industry
  country:     string(2)   # ISO 3166
  inception:   date        # First trading date
  status:      enum        # active/suspended/delisted
}

Price {
  security_oid: string(12)
  timestamp:    datetime  # UTC, nanosecond precision
  bid:          decimal
  ask:          decimal
  last:         decimal
  volume:       integer
  exchange:     string
  trade_type:   enum       # regular/after-hours/auction/...
}

NewsItem {
  id:           string(36) # UUID
  headline:     string
  body:         text
  source:       string
  published:    datetime   # Wire time
  updated:      datetime   # Correction time
  sentiment:    enum       # positive/neutral/negative
  entities:     Security[] # Related securities
  categories:   string[]   # Tags
  url:          string     # Full article
}

Portfolio {
  name:       string
  owner:      user_id
  currency:   string(3)
  holdings:   Holding[]
  inception:  date
  benchmark:  Security?    # Reference benchmark
}

Holding {
  security_oid: string(12)
  quantity:     decimal
  currency:     string(3)
  cost_basis:   decimal
  acquired:     date
}

Alert {
  id:         string(36)   # UUID
  owner:      user_id
  type:       enum        # price/news/volume/technical/custom
  conditions: JSON        # Alert trigger definition
  channels:   string[]    # email/sms/push/webhook
  active:     bool
  triggered:  datetime?
}

Message {
  id:         string(36)   # UUID
  sender:     user_id
  recipients: user_id[]
  body:       text
  timestamp:  datetime
  encrypted:  bool
  archived:   bool
}
```

---

## 30. API Endpoints (Proposed)

### 30.1. REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/securities` | Search securities |
| `GET` | `/api/v1/securities/{oid}` | Security details |
| `GET` | `/api/v1/prices/{oid}` | Current price |
| `GET` | `/api/v1/prices/{oid}/history` | Historical prices |
| `GET` | `/api/v1/news` | News feed |
| `GET` | `/api/v1/news/{id}` | Article details |
| `GET` | `/api/v1/portfolios` | List portfolios |
| `POST` | `/api/v1/portfolios` | Create portfolio |
| `GET` | `/api/v1/alerts` | List alerts |
| `POST` | `/api/v1/alerts` | Create alert |
| `GET` | `/api/v1/watchlists` | List watchlists |
| `POST` | `/api/v1/watchlists` | Create watchlist |
| `GET` | `/api/v1/economics` | Economic calendar |
| `GET` | `/api/v1/calendar` | Earnings/calendar events |
| `GET` | `/api/v1/yield-curves` | Yield curve data |
| `GET` | `/api/v1/fundamentals/{oid}` | Financial statements |

### 30.2. WebSocket API

| Channel | Description |
|---|---|
| `ws://openberg/v1/ticker` | Real-time price streaming |
| `ws://openberg/v1/news` | Real-time news feed |
| `ws://openberg/v1/chat` | iB messaging |
| `ws://openberg/v1/alerts` | Alert notifications |
| `ws://openberg/v1/orderbook` | Level 2 market data |

### 30.3. gRPC API (Internal)

| Service | Description |
|---|---|
| `SecurityService` | Security master, identifier resolution |
| `MarketDataService` | Real-time and historical pricing |
| `NewsService` | News aggregation, NLP pipeline |
| `PortfolioService` | Portfolio CRUD, P&L calculations |
| `AlertService` | Alert management, condition evaluation |
| `ChatService` | Messaging, presence, contacts |
| `AnalyticsService` | Quantitative analysis, risk metrics |

---

## 31. Technology Stack

### 31.1. Frontend

| Layer | Technology |
|---|---|
| **UI Framework** | React + TypeScript |
| **Styling** | Tailwind CSS + headless components |
| **Charts** | D3.js or lightweight canvas engine |
| **State** | Zustand or Redux Toolkit |
| **Build** | Vite or Turbopack |
| **Desktop** | Electron (or Tauri for smaller binary) |
| **Mobile** | React Native |

### 31.2. Backend

| Layer | Technology |
|---|---|
| **API Gateway** | FastAPI (Python) or Axum (Rust) |
| **Core Engine** | Rust — streaming, pricing, analytics |
| **Task Queue** | Celery (Python) or async-std (Rust) |
| **Cache** | Redis |
| **Search** | Elasticsearch or Meilisearch |

### 31.3. Data Layer

| Layer | Technology |
|---|---|
| **Timeseries DB** | ClickHouse or TimescaleDB |
| **Reference DB** | PostgreSQL |
| **Message Bus** | Kafka or Redpanda |
| **Object Store** | S3-compatible (MinIO/Ceph) |
| **Graph DB** | Neo4j (security relationships) |

### 31.4. Infrastructure

| Layer | Technology |
|---|---|
| **Container** | Docker |
| **Orchestration** | Kubernetes / K3s |
| **CI/CD** | GitHub Actions |
| **Observability** | Prometheus + Grafana + OpenTelemetry |
| **DNS** | Cloudflare |
| **CDN** | Cloudflare / Fastly |

---

## 32. Subscription Tiers

| Tier | Price | Features |
|---|---|---|
| **Free** | \$0 | Delayed equity data, basic news, community data, 100 API req/min |
| **Starter** | \$10/month | Real-time equities, 5 watchlists, basic charts, 1,000 API req/min |
| **Pro** | \$49/month | All asset classes, unlimited watchlists, analytics, messaging, 10,000 API req/min |
| **Institutional** | Custom | Full data, dedicated support, SLA, white-label, custom connectors |

---

## 33. Glossary

| Term | Definition |
|---|---|
| **FIGI** | Financial Instrument Global Identifier — 12-char stable security ID |
| **LEI** | Legal Entity Identifier — 20-char identifier for legal entities |
| **FIX** | Financial Information eXchange — trade order protocol |
| **ISIN** | International Security Identification Number |
| **CUSIP** | US security identifier |
| **SEDOL** | UK security identifier |
| **GICS** | Global Industry Classification Standard |
| **VaR** | Value at Risk |
| **OAS** | Option-Adjusted Spread |
| **TWAP** | Time-Weighted Average Price |
| **VWAP** | Volume-Weighted Average Price |
| **MiFID II** | Markets in Financial Instruments Directive (EU) |
| **OMS** | Order Management System |
| **EMS** | Execution Management System |
| **ATN** | Algorithmic Trading Network |
| **BCO** | Bloomberg Original Coverage |
| **iB** | Instant Bloomberg — Bloomberg's instant messaging |
| **BLPAPI** | Bloomberg API — programmatic Terminal access |
| **BCOM** | Bloomberg Communications — Terminal protocol |

---

*Generated: 2026-05-16*
*Status: Draft v1.0 — Foundation for OpenBerg Terminal project*
*Next steps: Community review, prioritize implementation phases, design data connectors*
