"use client";
import { useState } from "react";
import type { RutaResponse } from "../app/types";

export function ResultPanel({ ruta }: { ruta: RutaResponse }) {
  const [expanded, setExpanded] = useState(false);
  const mins = Math.round(ruta.tiempo_min);
  const hrs = Math.floor(mins / 60);
  const minResto = mins % 60;
  const tiempoStr = hrs > 0 ? `${hrs}h ${minResto}m` : `${mins} min`;

  return (
    <div style={{ background:"rgba(255,255,255,0.03)", border:"1px solid rgba(255,255,255,0.07)", borderRadius:16, overflow:"hidden" }}>

      {/* Header */}
      <div style={{ padding:"12px 16px", background:"linear-gradient(90deg,rgba(255,59,78,0.12) 0%,transparent 100%)", borderBottom:"1px solid rgba(255,255,255,0.05)", display:"flex", alignItems:"center", gap:8 }}>
        <div style={{ width:6, height:6, borderRadius:"50%", background:"#FF3B4E", boxShadow:"0 0 8px #FF3B4E" }}/>
        <span style={{ color:"white", fontSize:12, fontWeight:700, letterSpacing:"0.04em" }}>RUTA CALCULADA</span>
      </div>

      {/* Stats grid */}
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:1, background:"rgba(255,255,255,0.04)", margin:"12px 12px 0" , borderRadius:12, overflow:"hidden" }}>
        <div style={{ background:"#0b0b18", padding:"14px 16px" }}>
          <p style={{ color:"rgba(255,255,255,0.35)", fontSize:"9px", fontWeight:700, letterSpacing:"0.12em", textTransform:"uppercase", margin:"0 0 6px" }}>Distancia</p>
          <p style={{ color:"white", fontSize:22, fontWeight:700, margin:0, letterSpacing:"-0.5px" }}>
            {ruta.distancia_km.toFixed(1)}
            <span style={{ color:"rgba(255,255,255,0.35)", fontSize:12, fontWeight:400, marginLeft:4 }}>km</span>
          </p>
        </div>
        <div style={{ background:"#0b0b18", padding:"14px 16px", borderLeft:"1px solid rgba(255,255,255,0.05)" }}>
          <p style={{ color:"rgba(255,255,255,0.35)", fontSize:"9px", fontWeight:700, letterSpacing:"0.12em", textTransform:"uppercase", margin:"0 0 6px" }}>Tiempo est.</p>
          <p style={{ color:"white", fontSize:22, fontWeight:700, margin:0, letterSpacing:"-0.5px" }}>
            {tiempoStr}
          </p>
        </div>
      </div>

      {/* Origen → Destino */}
      <div style={{ padding:"14px 16px", display:"flex", flexDirection:"column", gap:10 }}>
        <div style={{ display:"flex", alignItems:"flex-start", gap:10 }}>
          <div style={{ marginTop:5, width:8, height:8, borderRadius:"50%", background:"#22c55e", boxShadow:"0 0 8px #22c55e", flexShrink:0 }}/>
          <div>
            <p style={{ color:"rgba(255,255,255,0.3)", fontSize:"9px", textTransform:"uppercase", letterSpacing:"0.08em", margin:"0 0 2px" }}>Desde</p>
            <p style={{ color:"white", fontSize:12, fontWeight:600, margin:0, lineHeight:1.3 }}>{ruta.origen.nombre}</p>
          </div>
        </div>
        <div style={{ marginLeft:3, width:1, height:16, background:"linear-gradient(to bottom,rgba(34,197,94,0.5),rgba(255,59,78,0.5))" }}/>
        <div style={{ display:"flex", alignItems:"flex-start", gap:10 }}>
          <div style={{ marginTop:5, width:8, height:8, borderRadius:"50%", background:"#FF3B4E", boxShadow:"0 0 8px #FF3B4E", flexShrink:0 }}/>
          <div>
            <p style={{ color:"rgba(255,255,255,0.3)", fontSize:"9px", textTransform:"uppercase", letterSpacing:"0.08em", margin:"0 0 2px" }}>Hasta</p>
            <p style={{ color:"white", fontSize:12, fontWeight:600, margin:0, lineHeight:1.3 }}>{ruta.destino.nombre}</p>
          </div>
        </div>
      </div>

      {/* Paradas expandibles */}
      <div style={{ borderTop:"1px solid rgba(255,255,255,0.05)" }}>
        <button onClick={() => setExpanded(!expanded)}
          style={{ width:"100%", display:"flex", alignItems:"center", justifyContent:"space-between", padding:"11px 16px", background:"transparent", border:"none", color:"rgba(255,255,255,0.35)", fontSize:11, cursor:"pointer" }}
          onMouseEnter={e => (e.currentTarget.style.background = "rgba(255,255,255,0.03)")}
          onMouseLeave={e => (e.currentTarget.style.background = "transparent")}>
          <span style={{ display:"flex", alignItems:"center", gap:7 }}>
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
            {ruta.total_paradas} paradas en la ruta
          </span>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"
            style={{ transform: expanded ? "rotate(180deg)" : "none", transition:"transform 0.2s" }}>
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>

        {expanded && (
          <div style={{ maxHeight:180, overflowY:"auto", padding:"0 16px 12px", display:"flex", flexDirection:"column", gap:6 }}>
            {ruta.paradas.map((p, i) => (
              <div key={p.id} style={{ display:"flex", alignItems:"center", gap:8 }}>
                <div style={{ width:5, height:5, borderRadius:"50%", flexShrink:0, background: i===0?"#22c55e":i===ruta.paradas.length-1?"#FF3B4E":"rgba(255,255,255,0.2)" }}/>
                <span style={{ fontSize:11, color: i===0||i===ruta.paradas.length-1 ? "rgba(255,255,255,0.85)" : "rgba(255,255,255,0.4)", overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>
                  {i===0?"▶ ":i===ruta.paradas.length-1?"■ ":`${i}. `}{p.nombre}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div style={{ padding:"8px 16px 10px", borderTop:"1px solid rgba(255,255,255,0.04)", textAlign:"center" }}>
        <p style={{ color:"rgba(255,255,255,0.18)", fontSize:"9px", margin:0 }}>Velocidad promedio 40 km/h · Dijkstra + heapq</p>
      </div>
    </div>
  );
}