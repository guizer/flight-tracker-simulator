import axios, { AxiosResponse } from "axios";
import { AIRPORT_SERVICE_URL } from "../settings";
import { GetAirportsArgs, Airport } from "./type";

export interface ArticleClient {
  getAirports: (params?: GetAirportsArgs) => Promise<Airport[]>;
}

const NAMESPACE = "/airports";

export const createAirportClient = (): ArticleClient => {
  const httpClient = axios.create({
    baseURL: AIRPORT_SERVICE_URL,
  });
  return {
    getAirports: (params?: GetAirportsArgs) => {
      return httpClient
        .get<Airport[], AxiosResponse<Airport[]>, GetAirportsArgs>(NAMESPACE, {
          params,
        })
        .then((response) => response.data);
    },
  };
};
