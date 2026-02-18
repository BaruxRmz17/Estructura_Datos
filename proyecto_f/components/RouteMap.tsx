"use client";
import { useEffect, useRef, useState } from "react";
import { Map, type MapRef } from "@/components/ui/map";
import type { RutaResponse, Nodo } from "../app/types";

// Estilo OpenStreetMap via OpenFreeMap (tiles reales de calles)
const OSM_STYLE = "https://tiles.openfreemap.org/styles/liberty";
const AGS_CENTER: [number, number] = [-102.296, 21.879];

interface Props {
  ruta: RutaResponse | null;
  origenPreview: Nodo | null;
  destinoPreview: Nodo | null;
}

export function RouteMap({ ruta, origenPreview, destinoPreview }: Props) {
  const mapRef = useRef<MapRef>(null);
  const markersRef = useRef<any[]>([]);
  const [mapLoaded, setMapLoaded] = useState(false);

  // ── Esperar a que el mapa esté listo ───────────────────────
  useEffect(() => {
    const interval = setInterval(() => {
      const m = mapRef.current?.getMap?.();
      if (m && m.isStyleLoaded()) {
        // Registrar fuentes vacías al inicio
        if (!m.getSource("ruta")) {
          m.addSource("ruta", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
          m.addLayer({
            id: "ruta-halo",
            type: "line",
            source: "ruta",
            paint: { "line-color": "#FF3B4E", "line-width": 14, "line-opacity": 0.15, "line-blur": 6 },
            layout: { "line-cap": "round", "line-join": "round" },
          });
          m.addLayer({
            id: "ruta-casing",
            type: "line",
            source: "ruta",
            paint: { "line-color": "#ffffff", "line-width": 7, "line-opacity": 0.3 },
            layout: { "line-cap": "round", "line-join": "round" },
          });
          m.addLayer({
            id: "ruta-line",
            type: "line",
            source: "ruta",
            paint: { "line-color": "#FF3B4E", "line-width": 5, "line-opacity": 1 },
            layout: { "line-cap": "round", "line-join": "round" },
          });
          m.addSource("paradas", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
          m.addLayer({
            id: "paradas-outer",
            type: "circle",
            source: "paradas",
            paint: { "circle-radius": 5, "circle-color": "#ffffff", "circle-opacity": 0.9, "circle-stroke-color": "#FF3B4E", "circle-stroke-width": 2 },
          });
        }
        setMapLoaded(true);
        clearInterval(interval);
      }
    }, 200);
    return () => clearInterval(interval);
  }, []);

  // ── Helper: limpiar marcadores ─────────────────────────────
  function clearMarkers() {
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];
  }

  function crearMarker(lng: number, lat: number, color: string, label: string, icon: string) {
    const m = mapRef.current?.getMap?.();
    if (!m) return;

    // Importar Marker desde maplibre-gl que ya viene como dep de @mapcn/map
    const maplibre = require("maplibre-gl");
    const el = document.createElement("div");
    el.style.cssText = "display:flex;flex-direction:column;align-items:center;gap:5px;";
    el.innerHTML = `
      <div style="
        width:22px;height:22px;border-radius:50%;
        background:${color};border:3px solid white;
        box-shadow:0 2px 16px ${color}80;
        display:flex;align-items:center;justify-content:center;
        font-size:9px;color:white;font-weight:700;
      ">${icon}</div>
      <div style="
        background:rgba(7,7,17,0.92);color:white;
        font-size:10px;font-weight:600;font-family:'DM Sans',sans-serif;
        padding:3px 9px;border-radius:8px;
        border:1px solid rgba(255,255,255,0.13);
        white-space:nowrap;max-width:130px;
        overflow:hidden;text-overflow:ellipsis;
        box-shadow:0 4px 16px rgba(0,0,0,0.5);
      ">${label}</div>
    `;
    const marker = new maplibre.Marker({ element: el, anchor: "bottom" })
      .setLngLat([lng, lat])
      .addTo(m);
    markersRef.current.push(marker);
  }

  // ── Preview markers ────────────────────────────────────────
  useEffect(() => {
    if (!mapLoaded || ruta) return;
    clearMarkers();
    const m = mapRef.current?.getMap?.();
    if (!m) return;

    // Limpiar ruta
    (m.getSource("ruta") as any)?.setData({ type: "FeatureCollection", features: [] });
    (m.getSource("paradas") as any)?.setData({ type: "FeatureCollection", features: [] });

    if (origenPreview) {
      crearMarker(origenPreview.lon, origenPreview.lat, "#22c55e", origenPreview.nombre, "A");
      mapRef.current?.flyTo({ center: [origenPreview.lon, origenPreview.lat], zoom: 13, duration: 800 });
    }
    if (destinoPreview) {
      crearMarker(destinoPreview.lon, destinoPreview.lat, "#FF3B4E", destinoPreview.nombre, "B");
    }
  }, [origenPreview, destinoPreview, mapLoaded, ruta]);

  // ── Dibujar ruta real ──────────────────────────────────────
  useEffect(() => {
    if (!mapLoaded) return;
    const m = mapRef.current?.getMap?.();
    if (!m) return;

    clearMarkers();

    if (!ruta) {
      (m.getSource("ruta") as any)?.setData({ type: "FeatureCollection", features: [] });
      (m.getSource("paradas") as any)?.setData({ type: "FeatureCollection", features: [] });
      return;
    }

    // Dibujar línea de ruta sobre las calles
    (m.getSource("ruta") as any).setData(ruta.geojson);

    // Puntos intermedios
    const ptFeatures = ruta.paradas.slice(1, -1).map((p) => ({
      type: "Feature" as const,
      geometry: { type: "Point" as const, coordinates: [p.lon, p.lat] },
      properties: {},
    }));
    (m.getSource("paradas") as any).setData({ type: "FeatureCollection", features: ptFeatures });

    // Marcadores inicio / fin
    crearMarker(ruta.origen.lon, ruta.origen.lat, "#22c55e", ruta.origen.nombre, "A");
    crearMarker(ruta.destino.lon, ruta.destino.lat, "#FF3B4E", ruta.destino.nombre, "B");

    // Auto-zoom para encuadrar toda la ruta
    const coords = ruta.geojson.geometry.coordinates;
    const lngs = coords.map((c) => c[0]);
    const lats = coords.map((c) => c[1]);
    m.fitBounds(
      [[Math.min(...lngs), Math.min(...lats)], [Math.max(...lngs), Math.max(...lats)]],
      { padding: { top: 80, bottom: 80, left: 80, right: 80 }, duration: 1000, maxZoom: 14 }
    );
  }, [ruta, mapLoaded]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <Map
        ref={mapRef}
        center={AGS_CENTER}
        zoom={11}
        styles={{ light: OSM_STYLE, dark: OSM_STYLE }}
      />
    </div>
  );
}