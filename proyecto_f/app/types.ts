export interface Nodo {
  id: number;
  nombre: string;
  lat: number;
  lon: number;
}

export interface RutaResponse {
  origen: Nodo;
  destino: Nodo;
  distancia_km: number;
  tiempo_min: number;
  total_paradas: number;
  paradas: Nodo[];
  geojson: GeoJSONFeature;
}

export interface GeoJSONFeature {
  type: "Feature";
  geometry: {
    type: "LineString";
    coordinates: [number, number][];
  };
  properties: {
    distancia_km: number;
    tiempo_min: number;
  };
}
