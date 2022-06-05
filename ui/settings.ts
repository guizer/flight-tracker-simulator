import { LatLngExpression } from "leaflet";

export const AIRPORT_SERVICE_URL = "http://localhost:8000";

export const FLIGHT_STATUS_SERVICE_URL = "http://localhost:8001";

export const FLIGHT_SERVICE_URL = "http://localhost:8002";

export const LOCATION_ICON_SIZE = 24;

export const FLIGHT_ICON_SIZE = 16;

export const DEFAULT_MAP_ZOOM_LEVEL = 3;

export const DEFAULT_MAP_CENTER: LatLngExpression = [51.505, -0.09];

export const TILE_LAYER_URL =
  "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";

export const TILE_LAYER_ATTRIBUTION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>';
