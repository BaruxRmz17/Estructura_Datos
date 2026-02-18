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
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const h = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, []);

  useEffect(() => {
    if (query.length < 2) { setResults([]); return; }
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
      <div style={{ display:"flex", alignItems:"center", gap:10, background:"rgba(255,255,255,0.05)", border:`1px solid ${accent}35`, borderRadius:11, padding:"10px 12px" }}>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke={accent} strokeWidth="2.5" strokeLinecap="round">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
        </svg>
        <div style={{ flex:1, minWidth:0 }}>
          <p style={{ color:"white", fontSize:13, fontWeight:600, margin:0, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{value.nombre}</p>
          <p style={{ color:"rgba(255,255,255,0.3)", fontSize:10, margin:"2px 0 0" }}>ID {value.id}</p>
        </div>
        <button onClick={() => { onChange(null); setQuery(""); }}
          style={{ background:"none", border:"none", color:"rgba(255,255,255,0.3)", cursor:"pointer", padding:2, display:"flex", alignItems:"center" }}
          onMouseEnter={e => (e.currentTarget.style.color = "white")}
          onMouseLeave={e => (e.currentTarget.style.color = "rgba(255,255,255,0.3)")}>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
    );
  }

  return (
    <div ref={ref} style={{ position:"relative" }}>
      <div style={{ position:"relative" }}>
        <svg style={{ position:"absolute", left:12, top:"50%", transform:"translateY(-50%)", pointerEvents:"none" }}
          width="13" height="13" viewBox="0 0 24 24" fill="none" stroke={focused ? accent : "rgba(255,255,255,0.25)"} strokeWidth="2" strokeLinecap="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          type="text" value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => { setFocused(true); results.length > 0 && setOpen(true); }}
          onBlur={() => setFocused(false)}
          placeholder="Buscar localidad o ID..."
          style={{
            width:"100%", background:"rgba(255,255,255,0.04)",
            border:`1px solid ${focused ? accent+"55" : "rgba(255,255,255,0.08)"}`,
            borderRadius:11, paddingLeft:34, paddingRight:36, paddingTop:10, paddingBottom:10,
            color:"white", fontSize:13, outline:"none", transition:"border-color 0.2s",
          }}
        />
        {loading && (
          <div style={{ position:"absolute", right:12, top:"50%", transform:"translateY(-50%)", width:14, height:14, border:"2px solid rgba(255,255,255,0.15)", borderTopColor:"rgba(255,255,255,0.6)", borderRadius:"50%", animation:"spin .8s linear infinite" }}/>
        )}
      </div>

      {open && results.length > 0 && (
        <div style={{ position:"absolute", zIndex:100, width:"100%", marginTop:6, background:"#0f0f1e", border:"1px solid rgba(255,255,255,0.1)", borderRadius:12, overflow:"hidden", boxShadow:"0 16px 48px rgba(0,0,0,0.6)" }}>
          {results.map((nodo, i) => (
            <button key={nodo.id}
              onClick={() => { onChange(nodo); setOpen(false); setQuery(""); }}
              style={{ width:"100%", display:"flex", alignItems:"center", gap:10, padding:"10px 14px", background:"transparent", border:"none", cursor:"pointer", textAlign:"left", borderBottom: i < results.length-1 ? "1px solid rgba(255,255,255,0.04)" : "none" }}
              onMouseEnter={e => (e.currentTarget.style.background = "rgba(255,255,255,0.05)")}
              onMouseLeave={e => (e.currentTarget.style.background = "transparent")}>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="2" strokeLinecap="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
              </svg>
              <div style={{ minWidth:0 }}>
                <p style={{ color:"white", fontSize:12, fontWeight:500, margin:0, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{nodo.nombre}</p>
                <p style={{ color:"rgba(255,255,255,0.25)", fontSize:10, margin:"1px 0 0" }}>ID {nodo.id} · {nodo.lat.toFixed(3)}, {nodo.lon.toFixed(3)}</p>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}