"use client";
import { useState } from "react";
import { NodeSearch } from "../components/NodeSearch";
import { RouteMap } from "../components/RouteMap";
import { ResultPanel } from "../components/ResultPanel";
import type { Nodo, RutaResponse } from "./types";

const API = "http://localhost:8000";

export default function Home() {
  const [origen, setOrigen] = useState<Nodo | null>(null);
  const [destino, setDestino] = useState<Nodo | null>(null);
  const [ruta, setRuta] = useState<RutaResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function calcularRuta() {
    if (!origen || !destino) return;
    setLoading(true); setError(null); setRuta(null);
    try {
      const res = await fetch(`${API}/ruta`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ origen_id: origen.id, destino_id: destino.id }),
      });
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
      setRuta(await res.json());
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  }

  function limpiar() { setOrigen(null); setDestino(null); setRuta(null); setError(null); }
  const canCalc = !!origen && !!destino && !loading;

  return (
    <div style={{ display:"flex", height:"100vh", overflow:"hidden", background:"#070711", fontFamily:"'DM Sans','Inter',-apple-system,sans-serif" }}>

      {/* ══════════════ SIDEBAR ══════════════ */}
      <aside style={{
        width:"360px", flexShrink:0,
        display:"flex", flexDirection:"column",
        background:"#0b0b18",
        borderRight:"1px solid rgba(255,255,255,0.06)",
        overflowY:"auto", zIndex:10,
        boxShadow:"4px 0 32px rgba(0,0,0,0.4)",
      }}>
        {/* ── Logo ── */}
        <div style={{ padding:"28px 28px 24px", borderBottom:"1px solid rgba(255,255,255,0.05)" }}>
          <div style={{ display:"flex", alignItems:"center", gap:12 }}>
            <div style={{
              width:40, height:40, borderRadius:12,
              background:"linear-gradient(135deg,#FF3B4E 0%,#8b0000 100%)",
              display:"flex", alignItems:"center", justifyContent:"center",
              boxShadow:"0 0 24px rgba(255,59,78,0.45)",
            }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="3 11 22 2 13 21 11 13 3 11"/>
              </svg>
            </div>
            <div>
              <h1 style={{ color:"white", fontSize:17, fontWeight:700, margin:0, letterSpacing:"-0.3px" }}>
                Rutas Óptimas
              </h1>
              <p style={{ color:"rgba(255,255,255,0.28)", fontSize:11, margin:"3px 0 0" }}>
                Aguascalientes · Dijkstra
              </p>
            </div>
          </div>
        </div>

        {/* ── Campos ── */}
        <div style={{ padding:"24px 24px 0", display:"flex", flexDirection:"column", gap:0 }}>

          {/* Tarjeta contenedor */}
          <div style={{ background:"rgba(255,255,255,0.03)", border:"1px solid rgba(255,255,255,0.07)", borderRadius:16, overflow:"hidden" }}>

            {/* Origen */}
            <div style={{ padding:"16px 16px 14px" }}>
              <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:10 }}>
                <div style={{ width:8, height:8, borderRadius:"50%", background:"#22c55e", boxShadow:"0 0 10px #22c55e", flexShrink:0 }}/>
                <span style={{ color:"rgba(255,255,255,0.4)", fontSize:"10px", fontWeight:700, letterSpacing:"0.12em", textTransform:"uppercase" }}>
                  Punto de origen
                </span>
              </div>
              <NodeSearch label="" color="green" value={origen}
                onChange={(n) => { setOrigen(n); setRuta(null); setError(null); }} />
            </div>

            {/* Separador con ícono swap */}
            <div style={{ display:"flex", alignItems:"center", padding:"0 16px", gap:10 }}>
              <div style={{ flex:1, height:1, background:"rgba(255,255,255,0.06)" }}/>
              <div style={{ width:26, height:26, borderRadius:"50%", border:"1px solid rgba(255,255,255,0.1)", background:"rgba(255,255,255,0.04)", display:"flex", alignItems:"center", justifyContent:"center" }}>
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.4)" strokeWidth="2.5" strokeLinecap="round">
                  <line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/>
                </svg>
              </div>
              <div style={{ flex:1, height:1, background:"rgba(255,255,255,0.06)" }}/>
            </div>

            {/* Destino */}
            <div style={{ padding:"14px 16px 16px" }}>
              <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:10 }}>
                <div style={{ width:8, height:8, borderRadius:"50%", background:"#FF3B4E", boxShadow:"0 0 10px #FF3B4E", flexShrink:0 }}/>
                <span style={{ color:"rgba(255,255,255,0.4)", fontSize:"10px", fontWeight:700, letterSpacing:"0.12em", textTransform:"uppercase" }}>
                  Punto de destino
                </span>
              </div>
              <NodeSearch label="" color="red" value={destino}
                onChange={(n) => { setDestino(n); setRuta(null); setError(null); }} />
            </div>
          </div>

          {/* Error */}
          {error && (
            <div style={{ marginTop:12, display:"flex", alignItems:"flex-start", gap:10, background:"rgba(255,59,78,0.08)", border:"1px solid rgba(255,59,78,0.22)", borderRadius:12, padding:"12px 14px", color:"#ff8a92", fontSize:12 }}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{ flexShrink:0, marginTop:1 }}>
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {error}
            </div>
          )}

          {/* Botones */}
          <div style={{ display:"flex", gap:8, marginTop:12 }}>
            <button onClick={calcularRuta} disabled={!canCalc}
              style={{
                flex:1, display:"flex", alignItems:"center", justifyContent:"center", gap:8,
                padding:"14px", borderRadius:14, border:"none", cursor:canCalc?"pointer":"not-allowed",
                background:canCalc?"linear-gradient(135deg,#FF3B4E,#b5001f)":"rgba(255,255,255,0.05)",
                color:"white", fontSize:14, fontWeight:600,
                boxShadow:canCalc?"0 8px 28px rgba(255,59,78,0.4)":"none",
                transition:"all 0.2s", opacity:canCalc?1:0.4,
              }}>
              {loading ? (
                <><div style={{ width:16,height:16,border:"2px solid rgba(255,255,255,0.3)",borderTopColor:"white",borderRadius:"50%",animation:"spin .8s linear infinite"}}/>Calculando...</>
              ) : (
                <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>Calcular ruta</>
              )}
            </button>
            {(origen||destino||ruta) && (
              <button onClick={limpiar}
                style={{ padding:"14px", borderRadius:14, border:"1px solid rgba(255,255,255,0.09)", background:"transparent", color:"rgba(255,255,255,0.4)", cursor:"pointer", display:"flex", alignItems:"center" }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>
                </svg>
              </button>
            )}
          </div>

          {/* Resultado */}
          {ruta && <div style={{ marginTop:12 }}><ResultPanel ruta={ruta}/></div>}
        </div>

        <div style={{ marginTop:"auto", padding:"16px 24px", borderTop:"1px solid rgba(255,255,255,0.04)", textAlign:"center", color:"rgba(255,255,255,0.15)", fontSize:"10px" }}>
          Estructuras de Datos · Proyecto Integrador 2025
        </div>
      </aside>

      {/* ══════════════ MAPA ══════════════ */}
      <main style={{ flex:1, position:"relative" }}>
        <RouteMap ruta={ruta} origenPreview={origen} destinoPreview={destino}/>

        {!origen && !destino && !ruta && (
          <div style={{ position:"absolute",inset:0,display:"flex",alignItems:"center",justifyContent:"center",pointerEvents:"none" }}>
            <div style={{ background:"rgba(7,7,17,0.85)",backdropFilter:"blur(20px)",border:"1px solid rgba(255,255,255,0.08)",borderRadius:20,padding:"32px 40px",textAlign:"center",display:"flex",flexDirection:"column",alignItems:"center",gap:14 }}>
              <div style={{ width:52,height:52,borderRadius:16,background:"rgba(255,59,78,0.12)",border:"1px solid rgba(255,59,78,0.2)",display:"flex",alignItems:"center",justifyContent:"center" }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF3B4E" strokeWidth="2" strokeLinecap="round">
                  <polygon points="3 11 22 2 13 21 11 13 3 11"/>
                </svg>
              </div>
              <div>
                <p style={{ color:"white",fontWeight:700,fontSize:15,margin:"0 0 6px",letterSpacing:"-0.2px" }}>Selecciona origen y destino</p>
                <p style={{ color:"rgba(255,255,255,0.3)",fontSize:12,margin:0 }}>Busca localidades en el panel izquierdo</p>
              </div>
            </div>
          </div>
        )}

        {/* Badge OpenStreetMap */}
        <div style={{ position:"absolute",top:14,right:14,background:"rgba(7,7,17,0.8)",backdropFilter:"blur(8px)",border:"1px solid rgba(255,255,255,0.08)",borderRadius:8,padding:"5px 10px",fontSize:10,color:"rgba(255,255,255,0.4)",display:"flex",alignItems:"center",gap:6 }}>
          <svg width="9" height="9" viewBox="0 0 24 24" fill="#FF3B4E"><circle cx="12" cy="12" r="10"/></svg>
          OpenStreetMap · relation/2610002
        </div>
      </main>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .maplibregl-ctrl-bottom-right { bottom: 16px !important; right: 16px !important; }
        .maplibregl-ctrl-group { background: rgba(11,11,24,0.9) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
        .maplibregl-ctrl-group button { color: rgba(255,255,255,0.7) !important; }
        .maplibregl-ctrl-group button:hover { background: rgba(255,255,255,0.08) !important; color: white !important; }
      `}</style>
    </div>
  );
}