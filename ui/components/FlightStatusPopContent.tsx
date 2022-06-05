import { Airport } from "../clients/airport/type";
import { Flight } from "../clients/flight/type";
import { FlightStatus } from "../clients/flightStatus/type";

const FlightStatusPopupContent = ({
  flight,
  flightStatus,
  origin,
  destination,
}: {
  flight: Flight;
  flightStatus: FlightStatus;
  origin: Airport;
  destination: Airport;
}): JSX.Element => (
  <div className="flight-status-popup">
    <div>
      <b>Flight number:</b>
      <span>{flightStatus.flightId.split("/")[0]}</span>
    </div>
    <div>
      <b>Callsign:</b>
      <span>{flight.callsign}</span>
    </div>
    <div>
      <b>Aircraft:</b>
      <span>{flight.aircraft}</span>
    </div>
    <div>
      <b>Airline:</b>
      <span>{flight.airline}</span>
    </div>
    <hr />
    <div>
      <b>Origin:</b>
      <span>
        {flight.origin} / {origin.name}
      </span>
    </div>
    <div>
      <b>Destination:</b>
      <span>
        {flight.destination} / {destination.name}
      </span>
    </div>
    <hr />
    <div>
      <b>Latitude:</b>
      <span>{flightStatus.latitude} °</span>
    </div>
    <div>
      <b>Longitude:</b>
      <span>{flightStatus.longitude} °</span>
    </div>
    <div>
      <b>Altitude:</b>
      <span>{Number(flightStatus.altitude * 0.3048).toFixed()} m</span>
    </div>
    <div>
      <b>Speed:</b>
      <span>{Number(flightStatus.speed * 1.852).toFixed()} km/h</span>
    </div>
    <div>
      <b>Heading:</b>
      <span>{flightStatus.heading} °</span>
    </div>
  </div>
);

export default FlightStatusPopupContent;
