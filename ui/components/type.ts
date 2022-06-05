import { Airport } from "../clients/airport/type";
import { Flight } from "../clients/flight/type";
import { FlightStatus } from "../clients/flightStatus/type";

export type FlightStatusByFlightId = {
  [flightId: string]: FlightStatus;
};

export type FlightByFlightId = {
  [flightId: string]: Flight;
};

export type AirportByIcao = {
  [icaoCode: string]: Airport;
};
