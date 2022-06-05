import { FLIGHT_STATUS_SERVICE_URL } from "../../settings";

export const createFlightStatusEventSource = () =>
  new EventSource(`${FLIGHT_STATUS_SERVICE_URL}/stream`);
