export interface Flight {
  id: number;
  number: string;
  flight_id: string;
  callsign: string;
  aircraft: string;
  airline: string;
  origin: string;
  destination: string;
}

export interface GetFlightsArgs {
  flight_id?: string;
  skip?: number;
  limit?: number;
}
