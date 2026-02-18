"use client";
import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import type { RutaResponse, Nodo } from "../app/types";

const STYLE = "https://tiles.openfreemap.org/styles/liberty";
const AGS = { lng: -102.296, lat: 21.879, zoom: 11 };

interface Props {
  ruta: RutaResponse | null;
  origenPreview: Nodo | null;
  destinoPreview: Nodo | null;
}

export function RouteMap({ ruta, origenPreview, destinoPreview }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<maplibregl.Marker[]>([]);
  const [ready, setReady] = useState(false);

  // ── Init mapa ──────────────────────────────────────────────
  useEffect(() => {
    if (!containerRef.current) return;
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: STYLE,
      center: [AGS.lng, AGS.lat],
      zoom: AGS.zoom,
      attributionControl: false,
    });
    map.addControl(new maplibregl.NavigationControl(), "bottom-right");
    map.addControl(new maplibregl.AttributionControl({ compact: true }), "bottom-left");
    map.on("load", () => {
      // Fuente + capas para la ruta (vacías al inicio)
      map.addSource("ruta", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addLayer({
        id: "ruta-halo",
        type: "line",
        source: "ruta",
        paint: { "line-color": "#FF3B4E", "line-width": 12, "line-opacity": 0.18 },
        layout: { "line-cap": "round", "line-join": "round" },
      });
      map.addLayer({
        id: "ruta-line",
        type: "line",
        source: "ruta",
        paint: { "line-color": "#FF3B4E", "line-width": 4.5, "line-opacity": 0.95 },
        layout: { "line-cap": "round", "line-join": "round" },
      });
      // Paradas intermedias
      map.addSource("paradas", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addLayer({
        id: "paradas-dots",
        type: "circle",
        source: "paradas",
        paint: {
          "circle-radius": 4,
          "circle-color": "#ffffff",
          "circle-opacity": 0.6,
          "circle-stroke-color": "#FF3B4E",
          "circle-stroke-width": 1.5,
        },
      });
      setReady(true);
    });
    mapRef.current = map;
    return () => { map.remove(); mapRef.current = null; };
  }, []);

  // ── Limpiar marcadores helper ──────────────────────────────
  function clearMarkers() {
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];
  }

  function addMarker(lng: number, lat: number, color: string, label: string) {
    if (!mapRef.current) return;
    const el = document.createElement("div");
    el.style.cssText = `
      display:flex; flex-direction:column; align-items:center; gap:4px; cursor:default;
    `;
    el.innerHTML = `
      <div style="width:18px;height:18px;border-radius:50%;background:${color};border:2.5px solid white;box-shadow:0 2px 12px ${color}99;"></div>
      <div style="background:rgba(8,8,16,0.88);color:white;font-size:10px;font-weight:600;padding:2px 7px;border-radius:6px;border:1px solid rgba(255,255,255,0.12);white-space:nowrap;max-width:120px;overflow:hidden;text-overflow:ellipsis;">${label}</div>
    `;
    const marker = new maplibregl.Marker({ element: el, anchor: "bottom" })
      .setLngLat([lng, lat])
      .addTo(mapRef.current);
    markersRef.current.push(marker);
  }

  // ── Preview markers (antes de calcular) ───────────────────
  useEffect(() => {
    if (!ready || ruta) return;
    clearMarkers();
    if (origenPreview) {
      addMarker(origenPreview.lon, origenPreview.lat, "#22c55e", origenPreview.nombre);
      mapRef.current?.flyTo({ center: [origenPreview.lon, origenPreview.lat], zoom: 13, duration: 800 });
    }
    if (destinoPreview) {
      addMarker(destinoPreview.lon, destinoPreview.lat, "#FF3B4E", destinoPreview.nombre);
    }
  }, [origenPreview, destinoPreview, ready, ruta]);

  // ── Dibujar ruta ──────────────────────────────────────────
  useEffect(() => {
    if (!ready || !mapRef.current) return;
    const map = mapRef.current;
    clearMarkers();

    if (!ruta) {
      // Limpiar fuentes
      (map.getSource("ruta") as maplibregl.GeoJSONSource)?.setData({ type: "FeatureCollection", features: [] });
      (map.getSource("paradas") as maplibregl.GeoJSONSource)?.setData({ type: "FeatureCollection", features: [] });
      return;
    }

    // Dibujar línea de ruta
    (map.getSource("ruta") as maplibregl.GeoJSONSource).setData(ruta.geojson);

    // Puntos intermedios
    const features = ruta.paradas.slice(1, -1).map((p) => ({
      type: "Feature" as const,
      geometry: { type: "Point" as const, coordinates: [p.lon, p.lat] },
      properties: {},
    }));
    (map.getSource("paradas") as maplibregl.GeoJSONSource).setData({
      type: "FeatureCollection",
      features,
    });

    // Marcadores origen / destino
    addMarker(ruta.origen.lon, ruta.origen.lat, "#22c55e", `▶ ${ruta.origen.nombre}`);
    addMarker(ruta.destino.lon, ruta.destino.lat, "#FF3B4E", `■ ${ruta.destino.nombre}`);

    // Fit bounds
    const coords = ruta.geojson.geometry.coordinates;
    const lngs = coords.map((c) => c[0]);
    const lats = coords.map((c) => c[1]);
    map.fitBounds(
      [[Math.min(...lngs), Math.min(...lats)], [Math.max(...lngs), Math.max(...lats)]],
      { padding: 80, duration: 1000 }
    );
  }, [ruta, ready]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
    </div>
  );
}