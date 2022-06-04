import L from "leaflet";
import { useEffect, useMemo, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { createAirportClient } from "../airport/airportClient";
import { Airport } from "../airport/type";
import { createFlightStatusEventSource } from "../flightStatus";
import { FlightStatus } from "../flightStatus/type";
import {
  DEFAULT_MAP_CENTER,
  DEFAULT_MAP_ZOOM_LEVEL,
  FLIGHT_ICON_SIZE,
} from "../settings";
import FlightStatusPopupContent from "./FlightStatusPopContent";

type FlightStatusByFlightId = {
  [flightId: string]: FlightStatus;
};

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
  const [airports, setAirports] = useState<Airport[]>([]);
  const [flightStatus, setFlightStatus] = useState<FlightStatusByFlightId>({});
  const airportClient = useMemo(() => createAirportClient(), []);
  const [eventSource, setEventSource] = useState<EventSource>();
  const currentSimulationTime = useMemo(
    () =>
      Object.values(flightStatus)
        .sort(
          (statusA, statusB) =>
            new Date(statusB.time).getTime() - new Date(statusA.time).getTime()
        )
        .at(0)
        ?.time.toString(),
    [flightStatus]
  );

  useEffect(() => {
    airportClient
      .getAirports()
      .then(setAirports)
      .catch((error) => {
        console.log(error);
      });
  }, [airportClient]);

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
        setFlightStatus((previousStatuss) => ({
          ...previousStatuss,
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
        {Object.values(flightStatus)
          .filter((flightStatus) => flightStatus.alive === true)
          .map((flightStatus) => (
            <Marker
              key={flightStatus.flightId}
              position={[flightStatus.latitude, flightStatus.longitude]}
              icon={createFlightIcon(flightStatus.heading)}
            >
              <Popup minWidth={200}>
                <FlightStatusPopupContent flightStatus={flightStatus} />
              </Popup>
            </Marker>
          ))}
      </MapContainer>
    </div>
  );
};

export default Map;
