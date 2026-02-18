"""
Backend - Sistema de Rutas Óptimas Aguascalientes
FastAPI + Dijkstra + Cola de Prioridad + Listas de Adyacencia
Datos: OpenStreetMap (relation/2610002)

GEOMETRÍA REAL: Se usa OSRM (router.project-osrm.org) para obtener
la ruta real por calles sobre el resultado de Dijkstra.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import heapq, math, ast, os, pandas as pd, urllib.request, json
from functools import lru_cache

app = FastAPI(title="Rutas Aguascalientes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Haversine ────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi  = math.radians(lat2 - lat1)
    dlam  = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ─── Carga del grafo ──────────────────────────────────────────────
@lru_cache(maxsize=1)
def cargar_grafo():
    xlsx = os.path.join(os.path.dirname(__file__), "DataAguascalientes.xlsx")
    df   = pd.read_excel(xlsx)
    nodos, grafo = {}, {}

    for _, row in df.iterrows():
        nid = int(row["ID"])
        lat, lon = row["LAT_DECIMAL"], row["LON_DECIMAL"]
        if pd.isna(lat) or pd.isna(lon):
            continue
        nodos[nid] = {
            "nombre": str(row["NOM_LOC"]).strip(),
            "lat": float(lat), "lon": float(lon)
        }
        grafo[nid] = []

    for _, row in df.iterrows():
        nid = int(row["ID"])
        if nid not in nodos:
            continue
        raw = row["VECINOS"]
        if pd.isna(raw) or not str(raw).strip():
            continue
        try:
            vecinos = ast.literal_eval(str(raw))
        except:
            continue
        lat1, lon1 = nodos[nid]["lat"], nodos[nid]["lon"]
        for vid in vecinos:
            vid = int(vid)
            if vid in nodos:
                d = haversine(lat1, lon1, nodos[vid]["lat"], nodos[vid]["lon"])
                grafo[nid].append((vid, round(d, 6)))

    nombre_idx = {v["nombre"].upper(): k for k, v in nodos.items()}
    return grafo, nodos, nombre_idx

# ─── Dijkstra ─────────────────────────────────────────────────────
def dijkstra(grafo, origen, destino):
    cola = [(0.0, origen)]
    dist_min = {origen: 0.0}
    pred = {origen: None}
    vis  = set()

    while cola:
        costo, nodo = heapq.heappop(cola)
        if nodo in vis:
            continue
        vis.add(nodo)
        if nodo == destino:
            break
        for vec, peso in grafo.get(nodo, []):
            if vec in vis:
                continue
            nc = costo + peso
            if nc < dist_min.get(vec, math.inf):
                dist_min[vec] = nc
                pred[vec]     = nodo
                heapq.heappush(cola, (nc, vec))

    if destino not in dist_min:
        return None, []
    ruta, n = [], destino
    while n is not None:
        ruta.append(n)
        n = pred.get(n)
    ruta.reverse()
    return round(dist_min[destino], 4), ruta

# ─── OSRM: geometría real por calles ─────────────────────────────
def obtener_geometria_osrm(paradas: list) -> list:
    """
    Llama a la API pública de OSRM con los waypoints clave de la ruta
    y devuelve las coordenadas reales por calles.
    Usa máximo 25 waypoints para no exceder el límite de URL.
    """
    # Submuestrear a máximo 25 waypoints
    if len(paradas) > 25:
        step = len(paradas) / 24
        indices = [int(i * step) for i in range(24)] + [len(paradas) - 1]
        paradas_sample = [paradas[i] for i in sorted(set(indices))]
    else:
        paradas_sample = paradas

    coords_str = ";".join(f"{p['lon']},{p['lat']}" for p in paradas_sample)
    url = (
        f"http://router.project-osrm.org/route/v1/driving/{coords_str}"
        f"?overview=full&geometries=geojson&steps=false"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AgsRoutesApp/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        if data.get("code") == "Ok" and data.get("routes"):
            return data["routes"][0]["geometry"]["coordinates"]
    except Exception as e:
        print(f"OSRM falló, usando coordenadas directas: {e}")

    # Fallback: línea recta entre paradas si OSRM no responde
    return [[p["lon"], p["lat"]] for p in paradas]

# ─── Endpoints ────────────────────────────────────────────────────
class RutaRequest(BaseModel):
    origen_id: int
    destino_id: int

@app.get("/nodos")
def get_nodos(q: str = ""):
    _, nodos, _ = cargar_grafo()
    q_up = q.upper()
    result = [
        {"id": nid, "nombre": info["nombre"], "lat": info["lat"], "lon": info["lon"]}
        for nid, info in nodos.items()
        if q_up in info["nombre"].upper()
    ]
    return result[:50] if q else result

@app.post("/ruta")
def calcular_ruta(req: RutaRequest):
    grafo, nodos, _ = cargar_grafo()

    if req.origen_id not in nodos:
        raise HTTPException(404, f"Nodo {req.origen_id} no existe")
    if req.destino_id not in nodos:
        raise HTTPException(404, f"Nodo {req.destino_id} no existe")
    if req.origen_id == req.destino_id:
        raise HTTPException(400, "Origen y destino son el mismo")

    distancia, ruta_ids = dijkstra(grafo, req.origen_id, req.destino_id)
    if distancia is None:
        raise HTTPException(404, "No existe ruta entre esos puntos")

    tiempo_min = round((distancia / 40) * 60, 1)
    paradas = [
        {"id": nid, "nombre": nodos[nid]["nombre"],
         "lat": nodos[nid]["lat"], "lon": nodos[nid]["lon"]}
        for nid in ruta_ids
    ]

    # ── Obtener geometría real por calles via OSRM ──
    coords_reales = obtener_geometria_osrm(paradas)

    return {
        "origen":        paradas[0],
        "destino":       paradas[-1],
        "distancia_km":  distancia,
        "tiempo_min":    tiempo_min,
        "total_paradas": len(paradas),
        "paradas":       paradas,
        "geojson": {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                # Coordenadas reales por calles de OSRM
                "coordinates": coords_reales,
            },
            "properties": {
                "distancia_km": distancia,
                "tiempo_min":   tiempo_min,
            },
        },
    }

@app.get("/stats")
def get_stats():
    grafo, nodos, _ = cargar_grafo()
    return {
        "total_nodos":   len(nodos),
        "total_aristas": sum(len(v) for v in grafo.values()),
        "fuente":        "OpenStreetMap - Aguascalientes (relation/2610002)",
        "algoritmo":     "Dijkstra + Cola de Prioridad (heapq) + OSRM geometry",
    }