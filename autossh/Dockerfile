# The tunnel sidecar. Built locally so its OpenSSL and musl are current at build
# time, instead of running whatever `alpine:latest` was when it was last pulled.
FROM alpine:3.22
RUN apk upgrade --no-cache && apk add --no-cache autossh
