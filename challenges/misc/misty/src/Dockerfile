FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o uploo .

#stage2
FROM alpine:latest

COPY --from=builder /app/uploo /usr/local/bin/uploo
RUN chmod +x /usr/local/bin/uploo
ENTRYPOINT ["uploo"]
CMD ["--help"]