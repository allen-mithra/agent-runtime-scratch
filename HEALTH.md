# Health

The service exposes a liveness endpoint at `/healthz`.

- **Path:** `/healthz`
- **Method:** `GET`
- **Response:** HTTP `200 OK` when the process is running.

A `200` response indicates only that the process is alive and able to serve HTTP. It does not assert that downstream dependencies (databases, queues, upstream APIs) are reachable; use a separate readiness probe for that.
