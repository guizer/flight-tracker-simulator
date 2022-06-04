import { FlightStatus } from "../flightStatus/type";

const FlightStatusPopupContent = ({
  flightStatus,
}: {
  flightStatus: FlightStatus;
}): JSX.Element => (
  <div className="flight-position-popup">
    <div>
      <b>Flight number:</b>
      <span>{flightStatus.flightId.split("/")[0]}</span>
    </div>
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
