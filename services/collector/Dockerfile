FROM golang:1.27 AS builder

WORKDIR /src

COPY services/collector/go.mod services/collector/go.sum* ./services/collector/
RUN cd services/collector && go mod download

COPY services/collector ./services/collector

RUN cd services/collector && \
    CGO_ENABLED=0 GOOS=linux go build \
    -o /out/collector ./cmd/collector


FROM gcr.io/distroless/static-debian12

COPY --from=builder /out/collector /collector

EXPOSE 8080

ENTRYPOINT ["/collector"]
