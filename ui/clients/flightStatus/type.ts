export interface FlightStatus {
  flightId: string;
  time: Date;
  latitude: number;
  longitude: number;
  altitude: number;
  speed: number;
  heading: number;
  alive: boolean;
}
