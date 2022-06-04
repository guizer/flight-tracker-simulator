# flight-events-simulator
Simulation of a service receiving real time flight position events and dispatching those events to subscribers

## How it works

- Flight position events are generated and published to a RabbitMQ instance by the event producer service. :heavy_check_mark:

- Those position events are consumed by
  - The flight status service which
    1. Update the current position of the associated flight in its internal database. :heavy_check_mark:
    1. Expose the position and their updates in near real-time with server-sent events. :heavy_check_mark:
  - The flight position history service
    1. Historize the position of the associated flight in its internal database. :x:
    2. Expose the past positions of the flights in REST. :x:

- Airport data (names and coordinates) are exposed with a REST api by the airport service. :heavy_check_mark:

- Flight data (departure, arrival, aircraft...) are exposed with a REST api by the flight service. :x:

- A UI allows the visualization
  - of the current position of each aircraft on a map. :heavy_check_mark:
  - of the past position of each aircraft on a map. :x:



## Prerequisites
- Docker
- Docker compose


## Usage

Run the simulation by running
```
docker compose up
```

The UI of the simulation is available at `http://localhost:3000`.
