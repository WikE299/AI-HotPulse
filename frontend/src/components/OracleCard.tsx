import { useState, useEffect, useRef, useCallback } from 'react';
import { fetchTodayPrediction } from '../api/client';
import type { Prediction } from '../types';
import './OracleCard.css';

const STATUS_LABELS: Record<string, string> = {
  pending: 'PENDING',
  approaching: 'APPROACHING',
  fulfilled: 'FULFILLED',
  busted: 'BUSTED',
  partial: 'PARTIAL',
  unfalsifiable: 'UNFALSIFIABLE',
};

const CATEGORY_LABELS: Record<string, string> = {
  timeline: 'TIMELINE',
  product: 'PRODUCT',
  capability: 'CAPABILITY',
  technical: 'TECHNICAL',
  industry: 'INDUSTRY',
};

function daysUntil(deadline: string): number | null {
  const d = new Date(deadline);
  if (isNaN(d.getTime())) return null;
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  return Math.ceil((d.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

function initials(name: string): string {
  return name
    .split(/\s+/)
    .map((w) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

interface Position { x: number; y: number }

function clamp(val: number, min: number, max: number) {
  return Math.max(min, Math.min(max, val));
}

export function OracleCard() {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [open, setOpen] = useState(false);
  const [imgError, setImgError] = useState(false);
  const [pos, setPos] = useState<Position>({ x: window.innerWidth - 72, y: window.innerHeight - 72 });
  const [isDragging, setIsDragging] = useState(false);
  const dragging = useRef(false);
  const dragMoved = useRef(false);
  const offset = useRef<Position>({ x: 0, y: 0 });
  const fabRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    fetchTodayPrediction()
      .then(setPrediction)
      .catch(() => {});
  }, []);

  const onPointerDown = useCallback((e: React.PointerEvent) => {
    dragging.current = true;
    dragMoved.current = false;
    setIsDragging(true);
    offset.current = { x: e.clientX - pos.x, y: e.clientY - pos.y };
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
    e.preventDefault();
  }, [pos]);

  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (!dragging.current) return;
    dragMoved.current = true;
    const nx = clamp(e.clientX - offset.current.x, 0, window.innerWidth - 48);
    const ny = clamp(e.clientY - offset.current.y, 0, window.innerHeight - 48);
    setPos({ x: nx, y: ny });
  }, []);

  const onPointerUp = useCallback(() => {
    if (!dragging.current) return;
    dragging.current = false;
    setIsDragging(false);
    setPos((prev) => {
      const centerX = prev.x + 24;
      const margin = 16;
      const snapX = centerX < window.innerWidth / 2 ? margin : window.innerWidth - 48 - margin;
      const snapY = clamp(prev.y, margin, window.innerHeight - 48 - margin);
      return { x: snapX, y: snapY };
    });
  }, []);

  const handleClick = useCallback(() => {
    if (dragMoved.current) return;
    setOpen((v) => !v);
  }, []);

  if (!prediction) return null;

  const days = prediction.deadline ? daysUntil(prediction.deadline) : null;

  const fabCenterX = pos.x + 24;
  const onRight = fabCenterX > window.innerWidth / 2;
  const cardLeft = onRight ? pos.x - 320 + 48 : pos.x;
  const cardTop = clamp(pos.y - 380, 8, window.innerHeight - 420);

  return (
    <>
      <button
        ref={fabRef}
        className={`oracle-fab ${open ? 'oracle-fab--open' : ''} ${isDragging ? 'dragging' : ''}`}
        style={{ left: pos.x, top: pos.y }}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onClick={handleClick}
        title="Oracle"
      >
        <svg className="oracle-fab-icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          {open ? (
            <>
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </>
          ) : (
            <>
              <circle cx="12" cy="12" r="10" />
              <circle cx="12" cy="12" r="4" />
              <line x1="12" y1="2" x2="12" y2="5" />
              <line x1="12" y1="19" x2="12" y2="22" />
              <line x1="2" y1="12" x2="5" y2="12" />
              <line x1="19" y1="12" x2="22" y2="12" />
            </>
          )}
        </svg>
      </button>

      {open && (
        <div
          className="oracle-card"
          style={{ left: cardLeft, top: cardTop }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="oracle-card-inner">
            <div className="oracle-header">
              <div className="oracle-avatar-wrap">
                {!imgError ? (
                  <img
                    className="oracle-avatar"
                    src={`/avatars/${prediction.avatar_file}`}
                    alt={prediction.person_name}
                    onError={() => setImgError(true)}
                  />
                ) : (
                  <div className="oracle-avatar-fallback">
                    {initials(prediction.person_name)}
                  </div>
                )}
              </div>
              <div className="oracle-person">
                <div className="oracle-name">{prediction.person_name}</div>
                <div className="oracle-title">{prediction.person_title}</div>
              </div>
            </div>

            <div className="oracle-quote-wrap">
              <blockquote className="oracle-quote">
                "{prediction.quote}"
              </blockquote>
            </div>

            <div className="oracle-meta">
              {prediction.quote_date && (
                <span className="oracle-date">{prediction.quote_date}</span>
              )}
              <span className={`oracle-badge oracle-badge--${prediction.category}`}>
                {CATEGORY_LABELS[prediction.category] || prediction.category.toUpperCase()}
              </span>
              <span className={`oracle-badge oracle-badge--${prediction.status}`}>
                {STATUS_LABELS[prediction.status] || prediction.status.toUpperCase()}
              </span>
            </div>

            {days != null && (
              <div className="oracle-countdown">
                {days > 0 ? (
                  <>DEADLINE IN <strong>{days}</strong> DAYS</>
                ) : days === 0 ? (
                  <strong>DEADLINE TODAY</strong>
                ) : (
                  <>DEADLINE PASSED <strong>{Math.abs(days)}</strong> DAYS AGO</>
                )}
              </div>
            )}

            {prediction.credibility_note && (
              <div className="oracle-note">{prediction.credibility_note}</div>
            )}

            {prediction.quote_source && (
              <a
                className="oracle-source"
                href={prediction.quote_source}
                target="_blank"
                rel="noopener noreferrer"
              >
                SOURCE ↗
              </a>
            )}
          </div>
        </div>
      )}
    </>
  );
}
