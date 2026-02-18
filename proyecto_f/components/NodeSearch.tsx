"use client";
import { useState, useEffect, useRef } from "react";
import type { Nodo } from "../app/types";

const API = "http://localhost:8000";

interface Props {
  label: string;
  color: "green" | "red";
  value: Nodo | null;
  onChange: (nodo: Nodo | null) => void;
}

export function NodeSearch({ color, value, onChange }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Nodo[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [focused, setFocused] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Cerrar al click afuera
  useEffect(() => {
    const h = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, []);

  // Búsqueda debounced
  useEffect(() => {
    if (query.length < 2) { setResults([]); setOpen(false); return; }
    const t = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API}/nodos?q=${encodeURIComponent(query)}`);
        const data: Nodo[] = await res.json();
        setResults(data.slice(0, 8));
        setOpen(true);
      } catch { setResults([]); }
      finally { setLoading(false); }
    }, 280);
    return () => clearTimeout(t);
  }, [query]);

  const accent = color === "green" ? "#22c55e" : "#FF3B4E";

  if (value) {
    return (
      <div style={{
        display: "flex", alignItems: "center", gap: 10,
        background: "rgba(255,255,255,0.05)",
        border: `1.5px solid ${accent}40`,
        borderRadius: 12, padding: "11px 14px",
        transition: "border-color 0.2s",
      }}>
        <div style={{ width: 8, height: 8, borderRadius: "50%", background: accent, boxShadow: `0 0 8px ${accent}`, flexShrink: 0 }} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <p style={{ color: "white", fontSize: 13, fontWeight: 600, margin: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {value.nombre}
          </p>
          <p style={{ color: "rgba(255,255,255,0.3)", fontSize: 10, margin: "2px 0 0" }}>ID {value.id}</p>
        </div>
        <button
          onClick={() => { onChange(null); setQuery(""); }}
          style={{ background: "none", border: "none", color: "rgba(255,255,255,0.3)", cursor: "pointer", padding: 4, borderRadius: 6, display: "flex", alignItems: "center", transition: "color 0.15s" }}
          onMouseEnter={e => (e.currentTarget.style.color = "white")}
          onMouseLeave={e => (e.currentTarget.style.color = "rgba(255,255,255,0.3)")}
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
    );
  }

  return (
    // position:relative + zIndex alto para que el dropdown salga ENCIMA de todo
    <div ref={containerRef} style={{ position: "relative", zIndex: 200 }}>
      <div style={{ position: "relative" }}>
        <svg
          style={{ position: "absolute", left: 13, top: "50%", transform: "translateY(-50%)", pointerEvents: "none", transition: "stroke 0.2s" }}
          width="13" height="13" viewBox="0 0 24 24" fill="none"
          stroke={focused ? accent : "rgba(255,255,255,0.28)"} strokeWidth="2" strokeLinecap="round"
        >
          <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => { setFocused(true); if (results.length > 0) setOpen(true); }}
          onBlur={() => setFocused(false)}
          placeholder="Escribe una localidad..."
          style={{
            width: "100%",
            background: focused ? "rgba(255,255,255,0.07)" : "rgba(255,255,255,0.04)",
            border: `1.5px solid ${focused ? accent + "60" : "rgba(255,255,255,0.09)"}`,
            borderRadius: 12, paddingLeft: 36, paddingRight: loading ? 36 : 14,
            paddingTop: 11, paddingBottom: 11,
            color: "white", fontSize: 13, outline: "none",
            transition: "border-color 0.2s, background 0.2s",
          }}
        />
        {loading && (
          <div style={{
            position: "absolute", right: 13, top: "50%", transform: "translateY(-50%)",
            width: 14, height: 14, border: "2px solid rgba(255,255,255,0.15)",
            borderTopColor: "rgba(255,255,255,0.7)", borderRadius: "50%",
            animation: "spin .8s linear infinite",
          }} />
        )}
      </div>

      {/* ── Dropdown — fixed position para que nunca quede tapado ── */}
      {open && results.length > 0 && (
        <div style={{
          position: "absolute",
          top: "calc(100% + 6px)",
          left: 0, right: 0,
          // zIndex muy alto para salir por encima del mapa y otros elementos
          zIndex: 9999,
          background: "#0f0f20",
          border: "1px solid rgba(255,255,255,0.12)",
          borderRadius: 13,
          overflow: "hidden",
          boxShadow: "0 20px 60px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.04)",
        }}>
          {results.map((nodo, i) => (
            <button
              key={nodo.id}
              onMouseDown={(e) => {
                // onMouseDown en vez de onClick para que dispare ANTES del onBlur del input
                e.preventDefault();
                onChange(nodo);
                setOpen(false);
                setQuery("");
              }}
              style={{
                width: "100%", display: "flex", alignItems: "center", gap: 10,
                padding: "11px 14px", background: "transparent", border: "none",
                cursor: "pointer", textAlign: "left",
                borderBottom: i < results.length - 1 ? "1px solid rgba(255,255,255,0.05)" : "none",
                transition: "background 0.15s",
              }}
              onMouseEnter={e => (e.currentTarget.style.background = "rgba(255,255,255,0.07)")}
              onMouseLeave={e => (e.currentTarget.style.background = "transparent")}
            >
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke={accent} strokeWidth="2.5" strokeLinecap="round" style={{ flexShrink: 0 }}>
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" /><circle cx="12" cy="10" r="3" />
              </svg>
              <div style={{ minWidth: 0 }}>
                <p style={{ color: "white", fontSize: 12, fontWeight: 600, margin: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {nodo.nombre}
                </p>
                <p style={{ color: "rgba(255,255,255,0.3)", fontSize: 10, margin: "2px 0 0" }}>
                  ID {nodo.id} · {nodo.lat.toFixed(4)}, {nodo.lon.toFixed(4)}
                </p>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}