# flight-events-simulator
Simulation of a service receiving real time flight position events and dispatching those events to subscribers

## How it works

- Flight position events are generated and published to a RabbitMQ instance by the event emitter service. :heavy_check_mark:

- Those position events are consumed by the flight position service which:
  1. Update the current position of the associated flight in its internal database. :heavy_check_mark:
  2. Historize the position of the associated flight in its internal database. :x:
  3. Expose the positions and their updates in near real-time with server-sent events. :heavy_check_mark:

- Airport data (names and coordinates) are exposed with a REST api by the airport service. :heavy_check_mark:

- A UI allows the visualization
  - of the current position of each aircraft on a map. :x:
  - of the past position of each aircraft on a map. :x:



## Prerequisites
- Docker
- Docker compose


## Usage

Run the simulation by running
```
docker compose up
```

Flight position events are streamed at the endpoint http://localhost:8001/stream. One can retrieve them with a compatible http client e.g.
```bash
curl -N --http2 -H "Accept:text/event-stream" http://localhost:8001/stream
```
