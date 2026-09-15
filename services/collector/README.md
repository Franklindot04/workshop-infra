## Configuration

- `COLLECTOR_PORT` — preferred service port.
- `PORT` — compatibility fallback.
- Default — `8080`.

## Metrics

The collector exposes a minimal metrics endpoint:

```bash
curl -i http://localhost:8080/metrics
```

The endpoint currently reports whether the collector is available and returns metrics using the Prometheus text exposition format.

This is an initial monitoring endpoint. Additional operational metrics will be introduced as the monitoring data path evolves.
