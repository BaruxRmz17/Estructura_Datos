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
    <div style={{
      display: "flex", height: "100vh", overflow: "hidden",
      background: "#070711",
      fontFamily: "'DM Sans','Inter',-apple-system,sans-serif",
    }}>

      {/* ══ SIDEBAR ══ */}
      <aside style={{
        width: "360px", flexShrink: 0,
        display: "flex", flexDirection: "column",
        background: "#0b0b1a",
        borderRight: "1px solid rgba(255,255,255,0.06)",
        // overflow visible para que el dropdown de NodeSearch salga
        overflow: "visible",
        zIndex: 100,
        boxShadow: "4px 0 40px rgba(0,0,0,0.5)",
        position: "relative",
      }}>
        {/* scroll solo en el contenido interno, no en el aside */}
        <div style={{ display: "flex", flexDirection: "column", height: "100%", overflowY: "auto", overflowX: "visible" }}>

          {/* Header */}
          <div style={{ padding: "28px 26px 22px", borderBottom: "1px solid rgba(255,255,255,0.05)", flexShrink: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{
                width: 40, height: 40, borderRadius: 12, flexShrink: 0,
                background: "linear-gradient(135deg,#FF3B4E,#8b0000)",
                display: "flex", alignItems: "center", justifyContent: "center",
                boxShadow: "0 0 28px rgba(255,59,78,0.5)",
              }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="3 11 22 2 13 21 11 13 3 11" />
                </svg>
              </div>
              <div>
                <h1 style={{ color: "white", fontSize: 17, fontWeight: 700, margin: 0, letterSpacing: "-0.3px" }}>Rutas Óptimas</h1>
                <p style={{ color: "rgba(255,255,255,0.28)", fontSize: 11, margin: "3px 0 0" }}>Aguascalientes · Dijkstra</p>
              </div>
            </div>
          </div>

          {/* Form */}
          <div style={{ padding: "22px 22px 0", display: "flex", flexDirection: "column", gap: 14, flex: 1 }}>

            {/* Card de búsqueda */}
            <div style={{
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.07)",
              borderRadius: 18,
              padding: "4px 0",
              // overflow visible para que el dropdown salga
              overflow: "visible",
              position: "relative",
            }}>
              {/* Origen */}
              <div style={{ padding: "14px 16px 12px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
                  <div style={{ width: 7, height: 7, borderRadius: "50%", background: "#22c55e", boxShadow: "0 0 8px #22c55e" }} />
                  <span style={{ color: "rgba(255,255,255,0.38)", fontSize: "10px", fontWeight: 700, letterSpacing: "0.12em", textTransform: "uppercase" }}>
                    Punto de origen
                  </span>
                </div>
                <NodeSearch label="" color="green" value={origen}
                  onChange={(n) => { setOrigen(n); setRuta(null); setError(null); }} />
              </div>

              {/* Divider con flecha */}
              <div style={{ display: "flex", alignItems: "center", padding: "0 16px", gap: 8 }}>
                <div style={{ flex: 1, height: 1, background: "rgba(255,255,255,0.06)" }} />
                <div style={{
                  width: 24, height: 24, borderRadius: "50%",
                  border: "1px solid rgba(255,255,255,0.1)",
                  background: "rgba(255,255,255,0.04)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                }}>
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.4)" strokeWidth="2.5" strokeLinecap="round">
                    <line x1="12" y1="5" x2="12" y2="19" /><polyline points="19 12 12 19 5 12" />
                  </svg>
                </div>
                <div style={{ flex: 1, height: 1, background: "rgba(255,255,255,0.06)" }} />
              </div>

              {/* Destino */}
              <div style={{ padding: "12px 16px 14px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
                  <div style={{ width: 7, height: 7, borderRadius: "50%", background: "#FF3B4E", boxShadow: "0 0 8px #FF3B4E" }} />
                  <span style={{ color: "rgba(255,255,255,0.38)", fontSize: "10px", fontWeight: 700, letterSpacing: "0.12em", textTransform: "uppercase" }}>
                    Punto de destino
                  </span>
                </div>
                <NodeSearch label="" color="red" value={destino}
                  onChange={(n) => { setDestino(n); setRuta(null); setError(null); }} />
              </div>
            </div>

            {/* Error */}
            {error && (
              <div style={{
                display: "flex", alignItems: "flex-start", gap: 10,
                background: "rgba(255,59,78,0.08)", border: "1px solid rgba(255,59,78,0.22)",
                borderRadius: 12, padding: "11px 14px", color: "#ff8a92", fontSize: 12,
              }}>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" style={{ flexShrink: 0, marginTop: 1 }}>
                  <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {error}
              </div>
            )}

            {/* Botones */}
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={calcularRuta} disabled={!canCalc}
                style={{
                  flex: 1, display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
                  padding: "13px", borderRadius: 13, border: "none",
                  cursor: canCalc ? "pointer" : "not-allowed",
                  background: canCalc ? "linear-gradient(135deg,#FF3B4E,#c0152a)" : "rgba(255,255,255,0.06)",
                  color: "white", fontSize: 14, fontWeight: 700,
                  boxShadow: canCalc ? "0 8px 28px rgba(255,59,78,0.4)" : "none",
                  opacity: canCalc ? 1 : 0.4, transition: "all 0.2s",
                }}>
                {loading ? (
                  <>
                    <div style={{ width: 15, height: 15, border: "2px solid rgba(255,255,255,0.3)", borderTopColor: "white", borderRadius: "50%", animation: "spin .8s linear infinite" }} />
                    Calculando...
                  </>
                ) : (
                  <>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
                    </svg>
                    Calcular ruta
                  </>
                )}
              </button>
              {(origen || destino || ruta) && (
                <button onClick={limpiar}
                  style={{ padding: "13px 14px", borderRadius: 13, border: "1px solid rgba(255,255,255,0.09)", background: "transparent", color: "rgba(255,255,255,0.4)", cursor: "pointer", display: "flex", alignItems: "center" }}
                  onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderColor = "rgba(255,255,255,0.2)"; (e.currentTarget as HTMLElement).style.color = "white"; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderColor = "rgba(255,255,255,0.09)"; (e.currentTarget as HTMLElement).style.color = "rgba(255,255,255,0.4)"; }}
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" /><path d="M3 3v5h5" />
                  </svg>
                </button>
              )}
            </div>

            {/* Panel de resultado */}
            {ruta && <ResultPanel ruta={ruta} />}
          </div>

          {/* Footer */}
          <div style={{ padding: "14px 22px", borderTop: "1px solid rgba(255,255,255,0.04)", textAlign: "center", color: "rgba(255,255,255,0.15)", fontSize: 10, marginTop: "auto", flexShrink: 0 }}>
            Estructuras de Datos · Proyecto Integrador 2025
          </div>
        </div>
      </aside>

      {/* ══ MAPA ══ */}
      <main style={{ flex: 1, position: "relative" }}>
        <RouteMap ruta={ruta} origenPreview={origen} destinoPreview={destino} />

        {!origen && !destino && !ruta && (
          <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", pointerEvents: "none" }}>
            <div style={{
              background: "rgba(7,7,17,0.88)", backdropFilter: "blur(20px)",
              border: "1px solid rgba(255,255,255,0.08)", borderRadius: 20,
              padding: "30px 40px", textAlign: "center",
              display: "flex", flexDirection: "column", alignItems: "center", gap: 14,
            }}>
              <div style={{ width: 50, height: 50, borderRadius: 15, background: "rgba(255,59,78,0.12)", border: "1px solid rgba(255,59,78,0.2)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF3B4E" strokeWidth="2" strokeLinecap="round">
                  <polygon points="3 11 22 2 13 21 11 13 3 11" />
                </svg>
              </div>
              <div>
                <p style={{ color: "white", fontWeight: 700, fontSize: 15, margin: "0 0 6px" }}>Selecciona origen y destino</p>
                <p style={{ color: "rgba(255,255,255,0.3)", fontSize: 12, margin: 0 }}>Busca localidades en el panel izquierdo</p>
              </div>
            </div>
          </div>
        )}

        {/* Badge fuente */}
        <div style={{
          position: "absolute", top: 14, right: 14,
          background: "rgba(7,7,17,0.82)", backdropFilter: "blur(10px)",
          border: "1px solid rgba(255,255,255,0.08)", borderRadius: 8,
          padding: "5px 10px", fontSize: 10, color: "rgba(255,255,255,0.4)",
          display: "flex", alignItems: "center", gap: 6,
        }}>
          <div style={{ width: 7, height: 7, borderRadius: "50%", background: "#FF3B4E" }} />
          OpenStreetMap · relation/2610002
        </div>
      </main>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}