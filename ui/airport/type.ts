export interface Airport {
  id: number;
  icao: string;
  name: string;
  country: string;
  latitude: number;
  longitude: number;
  altitude: number;
  iata?: string;
}

export interface GetAirportsArgs {}
