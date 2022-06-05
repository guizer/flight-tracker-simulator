import axios, { AxiosResponse } from "axios";
import { FLIGHT_SERVICE_URL } from "../../settings";
import { GetFlightsArgs, Flight } from "./type";

export interface ArticleClient {
  getFlights: (params?: GetFlightsArgs) => Promise<Flight[]>;
}

const NAMESPACE = "/flights";

export const createFlightClient = (): ArticleClient => {
  const httpClient = axios.create({
    baseURL: FLIGHT_SERVICE_URL,
  });
  return {
    getFlights: (params?: GetFlightsArgs) => {
      return httpClient
        .get<Flight[], AxiosResponse<Flight[]>, GetFlightsArgs>(NAMESPACE, {
          params,
        })
        .then((response) => response.data);
    },
  };
};
