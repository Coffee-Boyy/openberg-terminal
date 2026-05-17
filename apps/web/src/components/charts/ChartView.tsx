import { useEffect, useRef, useState } from 'react';
import {
  createChart,
  ColorType,
  CrosshairMode,
  LineStyle,
  IChartApi,
  ISeriesApi,
} from 'lightweight-charts';
// @ts-ignore — v5 runtime exports these as capitalized aliases, but typings are incomplete
import { CandlestickSeries, HistogramSeries } from 'lightweight-charts';
import { cn } from '@/lib/cn';
import { generatePriceBars } from '@/services/demo-data';

interface ChartViewProps {
  ticker: string;
  interval?: string;
  showVolume?: boolean;
}

interface ChartDataPoint {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export function ChartView({ ticker, interval = '1d', showVolume = true }: ChartViewProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [timeframe, setTimeframe] = useState(interval);
  const [error, setError] = useState<string | null>(null);
  const [bars, setBars] = useState<ChartDataPoint[]>([]);

  // Load chart data
  useEffect(() => {
    try {
      const data = generatePriceBars(ticker, timeframe, 200);
      setBars(data);
    } catch (e) {
      setError(String(e));
    }
  }, [ticker, timeframe]);

  // Initialize chart
  useEffect(() => {
    if (error || !chartContainerRef.current || !bars.length) return;

    let chart: IChartApi | null = null;
    let candleSeries: ISeriesApi<any> | null = null;
    let volumeSeries: ISeriesApi<any> | null = null;
    let observer: ResizeObserver | null = null;

    try {
      chart = createChart(chartContainerRef.current, {
        width: chartContainerRef.current.clientWidth,
        height: chartContainerRef.current.clientHeight || 400,
        layout: {
          background: { type: ColorType.Solid, color: '#0a0e17' },
          textColor: '#94a3b8',
          fontSize: 10,
          fontFamily: 'monospace',
        },
        grid: {
          vertLines: { color: '#1e293b' },
          horzLines: { color: '#1e293b' },
        },
        crosshair: {
          mode: CrosshairMode.Normal,
          vertLine: { color: '#3b82f6', width: 1, style: LineStyle.Dashed },
          horzLine: { color: '#3b82f6', width: 1, style: LineStyle.Dashed },
        },
        rightPriceScale: {
          borderColor: '#1e293b',
          scaleMargins: { top: 0.1, bottom: showVolume ? 0.3 : 0.1 },
        },
        timeScale: {
          borderColor: '#1e293b',
          timeVisible: true,
          secondsVisible: false,
        },
      });

      candleSeries = chart.addSeries(CandlestickSeries, {
        upColor: '#22c55e',
        downColor: '#ef4444',
        borderDownColor: '#ef4444',
        borderUpColor: '#22c55e',
        wickDownColor: '#ef4444',
        wickUpColor: '#22c55e',
      });

      candleSeries.setData(
        bars.map((b) => ({
          time: b.time,
          open: b.open,
          high: b.high,
          low: b.low,
          close: b.close,
        })),
      );

      if (showVolume) {
        volumeSeries = chart.addSeries(HistogramSeries, {
          color: '#3b82f6',
          priceFormat: { type: 'volume' },
          priceScaleId: 'volume',
        });
        chart.priceScale('volume').applyOptions({
          scaleMargins: { top: 0.8, bottom: 0 },
        });

        volumeSeries.setData(
          bars.map((b) => ({
            time: b.time,
            value: b.volume,
            color: b.close >= b.open ? 'rgba(34,197,94,0.4)' : 'rgba(239,68,68,0.4)',
          })),
        );
      }

      observer = new ResizeObserver(() => {
        chart?.applyOptions({
          width: chartContainerRef.current?.clientWidth || 600,
          height: chartContainerRef.current?.clientHeight || 400,
        });
      });
      observer.observe(chartContainerRef.current);
    } catch (e) {
      setError(String(e));
    }

    return () => {
      chart?.remove();
      observer?.disconnect();
    };
  }, [bars, showVolume, error]);

  // Fallback: render an SVG chart when there is no data
  const renderFallbackChart = () => {
    if (!bars.length) return null;
    const width = 800;
    const height = 300;
    const padding = 20;
    const closes = bars.map((b) => b.close);
    const min = Math.min(...closes);
    const max = Math.max(...closes);
    const range = max - min || 1;

    return (
      <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`} className="w-full h-full">
        {[0, 0.25, 0.5, 0.75, 1].map((p) => (
          <line
            key={p}
            x1={0}
            y1={padding + p * (height - 2 * padding)}
            x2={width}
            y2={padding + p * (height - 2 * padding)}
            stroke="#1e293b"
            strokeWidth={1}
          />
        ))}
        <polyline
          fill="none"
          stroke="#22c55e"
          strokeWidth={2}
          points={bars
            .map((b, i) => {
              const x = padding + (i / (bars.length - 1)) * (width - 2 * padding);
              const y = padding + (1 - (b.close - min) / range) * (height - 2 * padding);
              return `${x},${y}`;
            })
            .join(' ')}
        />
        {showVolume &&
          bars.map((b, i) => {
            const x = padding + (i / (bars.length - 1)) * (width - 2 * padding);
            const barH =
              (b.volume / Math.max(...bars.map((bb) => bb.volume))) *
              (height - 2 * padding) *
              0.3;
            return (
              <rect
                key={i}
                x={x - 2}
                y={height - padding - barH}
                width={4}
                height={barH}
                fill={b.close >= b.open ? 'rgba(34,197,94,0.3)' : 'rgba(239,68,68,0.3)'}
              />
            );
          })}
      </svg>
    );
  };

  const TIMELINES = ['1m', '5m', '15m', '1h', '4h', '1d', '1w', '1mo'];

  return (
    <div className="flex flex-col h-full">
      {/* Toolbar */}
      <div className="flex items-center gap-2 px-3 py-1.5 border-b border-bbg-border">
        <span className="text-bbg-green font-bold text-xs font-mono">{ticker}</span>
        <div className="flex gap-0.5">
          {TIMELINES.map((t) => (
            <button
              key={t}
              onClick={() => setTimeframe(t)}
              className={cn(
                'px-1.5 py-0.5 text-[10px] font-mono rounded transition-colors',
                timeframe === t
                  ? 'bg-bbg-green text-bbg-bg font-bold'
                  : 'text-bbg-text-dim hover:bg-bbg-border',
              )}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Chart area */}
      <div ref={containerRef} className="flex-1 min-h-[300px] relative">
        {error ? (
          <div className="flex items-center justify-center h-full text-bbg-text-dim text-xs">
            {error}
          </div>
        ) : (
          <div ref={chartContainerRef} className="w-full h-full" />
        )}
      </div>
    </div>
  );
}
