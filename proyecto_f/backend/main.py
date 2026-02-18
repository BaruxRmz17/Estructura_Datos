"""
Backend - Sistema de Rutas Óptimas Aguascalientes
FastAPI + Dijkstra + Cola de Prioridad + Listas de Adyacencia
Datos: OpenStreetMap (relation/2610002)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import heapq
import math
import ast
import os
import pandas as pd
from functools import lru_cache

app = FastAPI(title="Rutas Aguascalientes API")

# ── CORS: permite peticiones desde el frontend Next.js ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────
# 1. ESTRUCTURAS DE DATOS: GRAFO CON LISTA DE ADYACENCIA
# ─────────────────────────────────────────────────────────────

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia real en km entre dos coordenadas (fórmula Haversine)."""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


@lru_cache(maxsize=1)
def cargar_grafo():
    """
    Lee el Excel y construye:
      - grafo      : lista de adyacencia { id -> [(vecino, dist_km), ...] }
      - nodos      : { id -> {nombre, lat, lon} }
      - nombre_idx : { NOMBRE_UPPER -> id }
    Se cachea en memoria para no releer el archivo en cada petición.
    """
    xlsx = os.path.join(os.path.dirname(__file__), "DataAguascalientes.xlsx")
    df = pd.read_excel(xlsx)

    nodos: dict = {}
    grafo: dict = {}

    for _, row in df.iterrows():
        nid = int(row["ID"])
        nodos[nid] = {
            "nombre": str(row["NOM_LOC"]).strip(),
            "lat": float(row["LAT_DECIMAL"]),
            "lon": float(row["LON_DECIMAL"]),
        }
        grafo[nid] = []

    for _, row in df.iterrows():
        nid = int(row["ID"])
        raw = row["VECINOS"]
        if pd.isna(raw) or not str(raw).strip():
            continue
        try:
            vecinos = ast.literal_eval(str(raw))
        except Exception:
            continue

        lat1, lon1 = nodos[nid]["lat"], nodos[nid]["lon"]
        for vid in vecinos:
            vid = int(vid)
            if vid in nodos:
                dist = haversine(lat1, lon1, nodos[vid]["lat"], nodos[vid]["lon"])
                grafo[nid].append((vid, round(dist, 6)))

    nombre_idx = {v["nombre"].upper(): k for k, v in nodos.items()}
    return grafo, nodos, nombre_idx


# ─────────────────────────────────────────────────────────────
# 2. ALGORITMO DIJKSTRA CON COLA DE PRIORIDAD (heapq)
# ─────────────────────────────────────────────────────────────

def dijkstra(grafo: dict, origen: int, destino: int):
    """
    Dijkstra con min-heap.
    Retorna (distancia_total_km, lista_de_ids_ruta).
    """
    # Cola de prioridad: (costo_acumulado, nodo)
    cola = [(0.0, origen)]
    dist_min = {origen: 0.0}
    predecesor = {origen: None}
    visitados: set = set()

    while cola:
        costo, nodo = heapq.heappop(cola)

        if nodo in visitados:
            continue
        visitados.add(nodo)

        if nodo == destino:
            break

        for vecino, peso in grafo.get(nodo, []):
            if vecino in visitados:
                continue
            nuevo_costo = costo + peso
            if nuevo_costo < dist_min.get(vecino, math.inf):
                dist_min[vecino] = nuevo_costo
                predecesor[vecino] = nodo
                heapq.heappush(cola, (nuevo_costo, vecino))

    if destino not in dist_min:
        return None, []

    # Reconstruir ruta hacia atrás
    ruta, nodo = [], destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = predecesor.get(nodo)
    ruta.reverse()

    return round(dist_min[destino], 4), ruta


# ─────────────────────────────────────────────────────────────
# 3. ENDPOINTS
# ─────────────────────────────────────────────────────────────

class RutaRequest(BaseModel):
    origen_id: int
    destino_id: int


@app.get("/nodos")
def get_nodos(q: str = ""):
    """Lista de nodos (con filtro opcional por nombre)."""
    _, nodos, _ = cargar_grafo()
    q_up = q.upper()
    result = [
        {"id": nid, "nombre": info["nombre"], "lat": info["lat"], "lon": info["lon"]}
        for nid, info in nodos.items()
        if q_up in info["nombre"].upper()
    ]
    # Limitar a 50 resultados para búsqueda
    return result[:50] if q else result


@app.post("/ruta")
def calcular_ruta(req: RutaRequest):
    """Calcula la ruta óptima entre dos nodos usando Dijkstra."""
    grafo, nodos, _ = cargar_grafo()

    if req.origen_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo origen {req.origen_id} no existe")
    if req.destino_id not in nodos:
        raise HTTPException(status_code=404, detail=f"Nodo destino {req.destino_id} no existe")
    if req.origen_id == req.destino_id:
        raise HTTPException(status_code=400, detail="Origen y destino son el mismo nodo")

    distancia, ruta_ids = dijkstra(grafo, req.origen_id, req.destino_id)

    if distancia is None:
        raise HTTPException(status_code=404, detail="No existe ruta entre esos puntos")

    tiempo_min = round((distancia / 40) * 60, 1)  # 40 km/h promedio

    paradas = [
        {"id": nid, "nombre": nodos[nid]["nombre"], "lat": nodos[nid]["lat"], "lon": nodos[nid]["lon"]}
        for nid in ruta_ids
    ]

    return {
        "origen": paradas[0],
        "destino": paradas[-1],
        "distancia_km": distancia,
        "tiempo_min": tiempo_min,
        "total_paradas": len(paradas),
        "paradas": paradas,
        # GeoJSON LineString para el mapa
        "geojson": {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[p["lon"], p["lat"]] for p in paradas],
            },
            "properties": {"distancia_km": distancia, "tiempo_min": tiempo_min},
        },
    }


@app.get("/stats")
def get_stats():
    """Info general del grafo cargado."""
    grafo, nodos, _ = cargar_grafo()
    return {
        "total_nodos": len(nodos),
        "total_aristas": sum(len(v) for v in grafo.values()),
        "fuente": "OpenStreetMap - Aguascalientes (relation/2610002)",
        "algoritmo": "Dijkstra con cola de prioridad (heapq)",
        "estructura": "Lista de adyacencia",
    }
