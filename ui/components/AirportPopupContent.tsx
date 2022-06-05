import { Airport } from "../clients/airport/type";

const AirportPopupContent = ({
  airport,
}: {
  airport: Airport;
}): JSX.Element => (
  <div className="airport-popup">
    <div>
      <b>Name:</b>
      <span>{airport.name}</span>
    </div>
    <div>
      <b>ICAO:</b>
      <span>{airport.icao}</span>
    </div>
    <div>
      <b>IATA:</b>
      <span>{airport.iata}</span>
    </div>
    <div>
      <b>Country:</b>
      <span>{airport.country}</span>
    </div>
    <hr />
    <div>
      <b>Altitude:</b>
      <span>{Number(airport.altitude * 0.3048).toFixed()} m</span>
    </div>
    <div>
      <b>Latitude:</b>
      <span>{airport.latitude} °</span>
    </div>
    <div>
      <b>Longitude:</b>
      <span>{airport.longitude} °</span>
    </div>
  </div>
);

export default AirportPopupContent;
