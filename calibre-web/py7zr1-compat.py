"""Port the two callers of py7zr's removed SevenZipFile.read() to py7zr 1.x.

py7zr 1.0 dropped read()/readall(); the way to get bytes in memory is
extract(targets=..., factory=BytesIOFactory). calibre-web's CB7 cover reader
and comicapi's 7z archiver (the one calibre-web uses while comicapi is
installed) still call read(). Each replacement must match exactly once, so an
upstream change fails the image build instead of shipping a broken reader.
"""
import sys

LIMIT = "256 * 1024 * 1024"

PATCHES = {
    "/app/calibre-web/cps/comic.py": [(
        "cover_data = cf.read([name])[name].read()",
        f"factory = py7zr.io.BytesIOFactory({LIMIT}); "
        "cf.extract(targets=[name], factory=factory); "
        "cover_data = factory.get(name); cover_data.seek(0); cover_data = cover_data.read()",
    )],
    "/lsiopy/lib/python3.12/site-packages/comicapi/archivers/sevenzip.py": [(
        "data = zf.read(archive_file)[archive_file].read()",
        f"factory = py7zr.io.BytesIOFactory({LIMIT}); "
        "zf.extract(targets=[archive_file], factory=factory); "
        "data = factory.get(archive_file); data.seek(0); data = data.read()",
    ), (
        "for filename, buffer in zin.read(targets).items():\n"
        "                            zout.writef(buffer, filename)",
        f"factory = py7zr.io.BytesIOFactory({LIMIT}); "
        "zin.extract(targets=targets, factory=factory)\n"
        "                        for filename, buffer in factory.products.items():\n"
        "                            buffer.seek(0); zout.writestr(buffer.read(), filename)",
    )],
}

for path, pairs in PATCHES.items():
    text = open(path).read()
    for old, new in pairs:
        if text.count(old) != 1:
            sys.exit(f"{path}: expected exactly one {old!r}, found {text.count(old)}")
        text = text.replace(old, new)
    open(path, "w").write(text)
    print(f"patched {path}")
