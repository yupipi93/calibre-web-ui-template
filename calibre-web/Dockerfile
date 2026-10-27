# The library itself. Built locally on top of a pinned linuxserver tag so the
# parts upstream leaves stale are current at build time:
#  - kepubify: upstream copies the v4.0.4 release binary, built with go1.17.8
#    in 2022. Same source, rebuilt here with a current Go toolchain.
#  - Python packages calibre-web pins below their security fixes, raised past
#    those pins. pip check then flags pydrive2, which is only used by Google
#    Drive sync, and that is off here (config_use_google_drive = 0).
#  - py7zr raised to 1.1.3+ (CVE-2026-23879). 1.x removed
#    SevenZipFile.read(), which cps/comic.py and comicapi's 7z archiver
#    still call, so py7zr1-compat.py ports those lines to extract() with a
#    BytesIOFactory. It fails the build if upstream changes them.
#  - python3-pip-whl / python3-setuptools-whl: wheels only `python3 -m venv`
#    uses to bootstrap pip. /lsiopy already exists, so nothing runs them.
FROM golang:1.25-alpine AS kepubify
RUN CGO_ENABLED=0 go install -trimpath -ldflags "-s -w -X main.version=v4.0.4" \
      github.com/pgaskin/kepubify/v4/cmd/kepubify@v4.0.4

FROM lscr.io/linuxserver/calibre-web:0.6.27-ls407
COPY --from=kepubify /go/bin/kepubify /usr/bin/kepubify
COPY py7zr1-compat.py /tmp/py7zr1-compat.py
RUN /lsiopy/bin/pip install --no-cache-dir --upgrade \
      "pypdf>=6.21.2,<7" \
      "cryptography>=49.0.0" \
      "pyopenssl>=26.0.0" \
      "certifi>=2026.10.19" \
      "py7zr>=1.1.3" \
 && /lsiopy/bin/python /tmp/py7zr1-compat.py \
 && apt-get purge -y python3-venv python3.12-venv python3-pip-whl python3-setuptools-whl \
 && rm -rf /var/lib/apt/lists/* /tmp/*
