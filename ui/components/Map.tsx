import L, { Icon } from "leaflet";
import { useEffect, useMemo, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { createAirportClient } from "../clients/airport/airportClient";
import { createFlightClient } from "../clients/flight/flightClient";
import { createFlightStatusEventSource } from "../clients/flightStatus";
import { FlightStatus } from "../clients/flightStatus/type";
import {
  DEFAULT_MAP_CENTER,
  DEFAULT_MAP_ZOOM_LEVEL,
  FLIGHT_ICON_SIZE,
  LOCATION_ICON_SIZE,
} from "../settings";
import AirportPopupContent from "./AirportPopupContent";
import FlightStatusPopupContent from "./FlightStatusPopContent";
import {
  AirportByIcao,
  FlightByFlightId,
  FlightStatusByFlightId,
} from "./type";

const createFlightIcon = (heading: number) =>
  L.divIcon({
    iconSize: [FLIGHT_ICON_SIZE, FLIGHT_ICON_SIZE],
    iconAnchor: [FLIGHT_ICON_SIZE / 2, FLIGHT_ICON_SIZE / 2],
    html: `
    <img 
      style="transform: rotate(${heading}deg); background: transparent;"
      height="${FLIGHT_ICON_SIZE}" 
      width="${FLIGHT_ICON_SIZE}" 
      src="/air_plane_black.png"
    >`,
  });

const Map = () => {
  const [airports, setAirports] = useState<AirportByIcao>({});
  const [allFlightStatus, setAllFlightStatus] =
    useState<FlightStatusByFlightId>({});
  const [flights, setFlights] = useState<FlightByFlightId>({});
  const airportClient = useMemo(() => createAirportClient(), []);
  const flightClient = useMemo(() => createFlightClient(), []);
  const [eventSource, setEventSource] = useState<EventSource>();
  const currentSimulationTime = useMemo(
    () =>
      Object.values(allFlightStatus)
        .sort(
          (statusA, statusB) =>
            new Date(statusB.time).getTime() - new Date(statusA.time).getTime()
        )
        .at(0)
        ?.time.toString(),
    [allFlightStatus]
  );
  const airportsToDisplay = useMemo(() => {
    const originsToDisplay = Object.values(allFlightStatus)
      .filter((status) => status.alive)
      .map((status) => flights[status.flightId]?.origin);
    const destinationsToDisplay = Object.values(allFlightStatus)
      .filter((status) => status.alive)
      .map((status) => flights[status.flightId]?.destination);
    return Object.values(airports).filter(
      (airport) =>
        originsToDisplay.includes(airport.icao) ||
        destinationsToDisplay.includes(airport.icao)
    );
  }, [airports, allFlightStatus, flights]);

  useEffect(() => {
    airportClient
      .getAirports()
      .then((fetchedAirports) =>
        setAirports(
          fetchedAirports.reduce(
            (acc, airport) => ({
              ...acc,
              [airport.icao]: airport,
            }),
            {}
          )
        )
      )
      .catch((error) => {
        console.log(error);
      });
  }, [airportClient]);

  useEffect(() => {
    flightClient
      .getFlights()
      .then((fetchedFlights) =>
        setFlights(
          fetchedFlights.reduce(
            (acc, flight) => ({
              ...acc,
              [flight.flight_id]: flight,
            }),
            {}
          )
        )
      )
      .catch((error) => {
        console.log(error);
      });
  }, [flightClient]);

  useEffect(() => {
    setEventSource(createFlightStatusEventSource());
  }, []);

  useEffect(() => {
    if (eventSource) {
      eventSource.onmessage = (event: MessageEvent<string>) => {
        const newStatus: FlightStatusByFlightId = (
          JSON.parse(event.data) as FlightStatus[]
        ).reduce(
          (acc, position) => ({
            ...acc,
            [position.flightId]: position,
          }),
          {}
        );
        setAllFlightStatus((allPreviousStatus) => ({
          ...allPreviousStatus,
          ...newStatus,
        }));
      };
    }
    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [eventSource]);
  return (
    <div>
      <div className="simulation-time">{currentSimulationTime}</div>
      <MapContainer
        center={DEFAULT_MAP_CENTER}
        zoom={DEFAULT_MAP_ZOOM_LEVEL}
        style={{ height: "100vh", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {Object.values(airportsToDisplay).map((airport) => (
          <Marker
            key={airport.icao}
            position={[airport.latitude, airport.longitude]}
            zIndexOffset={1}
            icon={
              new Icon({
                iconUrl: "/location.png",
                iconAnchor: [LOCATION_ICON_SIZE / 2, LOCATION_ICON_SIZE / 2],
                iconSize: [LOCATION_ICON_SIZE, LOCATION_ICON_SIZE],
              })
            }
          >
            <Popup minWidth={400} maxWidth={600}>
              {<AirportPopupContent airport={airport} />}
            </Popup>
          </Marker>
        ))}
        {Object.values(allFlightStatus)
          .filter((flightStatus) => flightStatus.alive === true)
          .map((flightStatus) => (
            <Marker
              key={flightStatus.flightId}
              position={[flightStatus.latitude, flightStatus.longitude]}
              icon={createFlightIcon(flightStatus.heading)}
              zIndexOffset={2}
            >
              <Popup minWidth={400} maxWidth={600}>
                {flights[flightStatus.flightId] &&
                airports[flights[flightStatus.flightId].origin] &&
                airports[flights[flightStatus.flightId].destination] ? (
                  <FlightStatusPopupContent
                    flightStatus={flightStatus}
                    flight={flights[flightStatus.flightId]}
                    origin={airports[flights[flightStatus.flightId].origin]}
                    destination={
                      airports[flights[flightStatus.flightId].destination]
                    }
                  />
                ) : null}
              </Popup>
            </Marker>
          ))}
      </MapContainer>
    </div>
  );
};

export default Map;
