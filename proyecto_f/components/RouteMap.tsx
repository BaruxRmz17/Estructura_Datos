"use client";
import { useEffect, useRef } from "react";
import {
  Map,
  MapMarker,
  MarkerContent,
  MapControls,
  useMap,
  type MapRef,
} from "@/components/ui/map";
import type { RutaResponse, Nodo } from "../app/types";

// Carto Positron (claro y limpio como Google Maps)
const STYLE_LIGHT = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json";
// Carto Dark Matter (oscuro elegante como el default de mapcn)
const STYLE_DARK  = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json";

const AGS_CENTER: [number, number] = [-102.296, 21.879];

interface Props {
  ruta: RutaResponse | null;
  origenPreview: Nodo | null;
  destinoPreview: Nodo | null;
}

// ── Dibuja la ruta con addSource/addLayer nativos de MapLibre ───
function RutaLayer({ ruta }: { ruta: RutaResponse }) {
  const { map, isLoaded } = useMap();

  useEffect(() => {
    if (!map || !isLoaded) return;

    const coords: [number, number][] = ruta.geojson.geometry.coordinates
      .filter(([ln, la]) => ln != null && la != null && isFinite(ln) && isFinite(la))
      .map(([ln, la]) => [ln, la]);

    if (coords.length < 2) return;

    const geojson: GeoJSON.Feature = {
      type: "Feature",
      properties: {},
      geometry: { type: "LineString", coordinates: coords },
    };

    const cleanup = () => {
      try {
        if (map.getLayer("ags-dots"))   map.removeLayer("ags-dots");
        if (map.getLayer("ags-line"))   map.removeLayer("ags-line");
        if (map.getLayer("ags-casing")) map.removeLayer("ags-casing");
        if (map.getLayer("ags-halo"))   map.removeLayer("ags-halo");
        if (map.getSource("ags-ruta"))  map.removeSource("ags-ruta");
        if (map.getSource("ags-pts"))   map.removeSource("ags-pts");
      } catch (_) {}
    };

    cleanup(); // Limpiar si ya existían de antes

    try {
      // ── Fuente principal de la ruta ──
      map.addSource("ags-ruta", { type: "geojson", data: geojson });

      // Halo exterior difuminado
      map.addLayer({
        id: "ags-halo",
        type: "line",
        source: "ags-ruta",
        layout: { "line-cap": "round", "line-join": "round" },
        paint: { "line-color": "#4285F4", "line-width": 18, "line-opacity": 0.12, "line-blur": 4 },
      });
      // Borde blanco (casing) — igual que Google Maps
      map.addLayer({
        id: "ags-casing",
        type: "line",
        source: "ags-ruta",
        layout: { "line-cap": "round", "line-join": "round" },
        paint: { "line-color": "#ffffff", "line-width": 8, "line-opacity": 0.9 },
      });
      // Línea azul principal (igual que Google Maps)
      map.addLayer({
        id: "ags-line",
        type: "line",
        source: "ags-ruta",
        layout: { "line-cap": "round", "line-join": "round" },
        paint: { "line-color": "#4285F4", "line-width": 5.5, "line-opacity": 1 },
      });

      // ── Puntos intermedios ──
      const ptFeatures: GeoJSON.Feature[] = ruta.paradas.slice(1, -1).map((p) => ({
        type: "Feature",
        properties: {},
        geometry: { type: "Point", coordinates: [p.lon, p.lat] },
      }));
      map.addSource("ags-pts", {
        type: "geojson",
        data: { type: "FeatureCollection", features: ptFeatures },
      });
      map.addLayer({
        id: "ags-dots",
        type: "circle",
        source: "ags-pts",
        paint: {
          "circle-radius": 4,
          "circle-color": "#4285F4",
          "circle-stroke-color": "#ffffff",
          "circle-stroke-width": 2,
          "circle-opacity": 0.8,
        },
      });
    } catch (e) {
      console.warn("Error dibujando ruta:", e);
    }

    // Fit bounds con padding generoso
    const lngs = coords.map((c) => c[0]);
    const lats = coords.map((c) => c[1]);
    map.fitBounds(
      [[Math.min(...lngs), Math.min(...lats)], [Math.max(...lngs), Math.max(...lats)]],
      { padding: { top: 100, bottom: 100, left: 60, right: 60 }, duration: 1100, maxZoom: 14 }
    );

    return cleanup;
  }, [map, isLoaded, ruta]);

  return null;
}

// ── Fly-to cuando se selecciona origen en preview ───────────────
function FlyToPreview({ nodo }: { nodo: Nodo }) {
  const { map, isLoaded } = useMap();
  useEffect(() => {
    if (!map || !isLoaded) return;
    map.flyTo({ center: [nodo.lon, nodo.lat], zoom: 13, duration: 900 });
  }, [map, isLoaded, nodo]);
  return null;
}

// ── Pin A / B ───────────────────────────────────────────────────
function Pin({ nodo, label, bg, glow }: { nodo: Nodo; label: string; bg: string; glow: string }) {
  return (
    <MapMarker longitude={nodo.lon} latitude={nodo.lat} anchor="bottom">
      <MarkerContent>
        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:5, filter:`drop-shadow(0 4px 12px ${glow})` }}>
          {/* Círculo del pin */}
          <div style={{
            width:30, height:30, borderRadius:"50%",
            background:bg, border:"3px solid white",
            display:"flex", alignItems:"center", justifyContent:"center",
            color:"white", fontWeight:800, fontSize:12,
            fontFamily:"'DM Sans','Inter',sans-serif",
            letterSpacing:"-0.5px",
          }}>{label}</div>
          {/* Etiqueta nombre */}
          <div style={{
            background:"rgba(255,255,255,0.97)",
            color:"#111",
            fontSize:10, fontWeight:700,
            fontFamily:"'DM Sans','Inter',sans-serif",
            padding:"3px 9px", borderRadius:8,
            border:"1px solid rgba(0,0,0,0.1)",
            whiteSpace:"nowrap", maxWidth:150,
            overflow:"hidden", textOverflow:"ellipsis",
            boxShadow:"0 2px 12px rgba(0,0,0,0.18)",
          }}>{nodo.nombre}</div>
        </div>
      </MarkerContent>
    </MapMarker>
  );
}

// ── Componente principal ────────────────────────────────────────
export function RouteMap({ ruta, origenPreview, destinoPreview }: Props) {
  const mapRef = useRef<MapRef>(null);
  const origenNodo  = ruta?.origen  ?? origenPreview;
  const destinoNodo = ruta?.destino ?? destinoPreview;

  return (
    <div style={{ width:"100%", height:"100%" }}>
      <Map
        ref={mapRef}
        center={AGS_CENTER}
        zoom={11}
        // Sin pasar `styles` → usa el default Carto de mapcn (igual que la doc)
        // Si quieres el look claro tipo Google Maps descomenta la siguiente línea:
        // styles={{ light: STYLE_LIGHT, dark: STYLE_DARK }}
        className="w-full h-full"
      >
        {ruta && <RutaLayer ruta={ruta} />}

        {!ruta && origenPreview && <FlyToPreview nodo={origenPreview} />}

        {origenNodo && (
          <Pin nodo={origenNodo}  label="A" bg="#22c55e" glow="rgba(34,197,94,0.5)"  />
        )}
        {destinoNodo && (
          <Pin nodo={destinoNodo} label="B" bg="#FF3B4E" glow="rgba(255,59,78,0.5)" />
        )}

        <MapControls position="bottom-right" showZoom showCompass />
      </Map>
    </div>
  );
}