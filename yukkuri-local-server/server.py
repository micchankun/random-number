#!/usr/bin/env python3
"""Local-only AquesTalk10 bridge for the random-number web app.

Do NOT put the AquesTalk library or license key in this repository.
Set AQUESTALK_LIB to the path of the licensed AquesTalk10 Linux .so file.
The page calls this service only on 127.0.0.1:8765.
"""
import ctypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

HOST = "127.0.0.1"
PORT = 8765
LIB_PATH = os.environ.get("AQUESTALK_LIB", "")

# AquesTalk10 AQTK_VOICE: bas, spd, vol, pit, acc, lmd, fsc
class AQTK_VOICE(ctypes.Structure):
    _fields_ = [
        ("bas", ctypes.c_ubyte),
        ("spd", ctypes.c_ubyte),
        ("vol", ctypes.c_ubyte),
        ("pit", ctypes.c_ubyte),
        ("acc", ctypes.c_ubyte),
        ("lmd", ctypes.c_ubyte),
        ("fsc", ctypes.c_ubyte),
    ]

lib = None
if LIB_PATH:
    lib = ctypes.CDLL(LIB_PATH)
    lib.AquesTalk_Synthe_Utf8.argtypes = [ctypes.POINTER(AQTK_VOICE), ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
    lib.AquesTalk_Synthe_Utf8.restype = ctypes.POINTER(ctypes.c_ubyte)
    lib.AquesTalk_FreeWave.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
    lib.AquesTalk_FreeWave.restype = None

class Handler(BaseHTTPRequestHandler):
    def _headers(self, status=200, content_type="application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._headers(204)

    def do_GET(self):
        if self.path == "/health":
            self._headers()
            self.wfile.write(json.dumps({"ok": True, "engine": bool(lib)}).encode())
            return
        self._headers(404)
        self.wfile.write(b'{"ok":false}')

    def do_POST(self):
        if self.path != "/speak":
            self._headers(404)
            self.wfile.write(b'{"ok":false,"error":"not found"}')
            return
        if lib is None:
            self._headers(503)
            self.wfile.write(b'{"ok":false,"error":"AQUESTALK_LIB is not configured"}')
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            text = str(data.get("text", "")).strip()
            if not text or len(text) > 100:
                raise ValueError("text must be 1-100 characters")
            # Female voice 1 style; adjust parameters here if desired.
            voice = AQTK_VOICE(1, 100, 100, 70, 120, 130, 120)
            size = ctypes.c_int(0)
            wav = lib.AquesTalk_Synthe_Utf8(ctypes.byref(voice), text.encode("utf-8"), ctypes.byref(size))
            if not wav:
                raise RuntimeError(f"AquesTalk error: {size.value}")
            try:
                payload = ctypes.string_at(wav, size.value)
            finally:
                lib.AquesTalk_FreeWave(wav)
            self._headers(200, "audio/wav")
            self.wfile.write(payload)
        except Exception as exc:
            self._headers(400)
            self.wfile.write(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False).encode())

if __name__ == "__main__":
    print(f"AquesTalk local server: http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
