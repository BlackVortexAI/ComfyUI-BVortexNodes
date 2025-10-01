# __init__.py – parent requirements installer (robust)
import os, sys, subprocess, hashlib, importlib

REQ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "requirements.txt"))
CHECK = ("matplotlib",)  # minimal probe; erweitere bei Bedarf

def _have_all():
    for name in CHECK:
        mod = "PIL" if name.lower() in ("pillow","pil") else name
        try:
            importlib.import_module(mod)
        except Exception:
            return False
    return True

if os.path.isfile(REQ):
    h = hashlib.sha256()
    with open(REQ, "rb") as f:
        h.update(f.read())
    h.update(sys.version.encode("utf-8"))
    h.update(sys.prefix.encode("utf-8"))
    cache_dir = os.path.join(os.path.dirname(__file__), ".deps_cache")
    os.makedirs(cache_dir, exist_ok=True)
    sentinel = os.path.join(cache_dir, h.hexdigest() + ".ok")

    def _install():
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", REQ,
            "--disable-pip-version-check", "--no-input"
        ])

    try:
        if not os.path.isfile(sentinel):
            _install()
            if _have_all():
                open(sentinel, "w").close()
        else:
            # Sentinel existiert, aber Pakete fehlen -> neu installieren
            if not _have_all():
                _install()
                if _have_all():
                    open(sentinel, "w").close()
    except Exception as e:
        # Falls Installation fehlschlägt, Sentinel sicherheitshalber löschen
        try:
            if os.path.isfile(sentinel): os.remove(sentinel)
        finally:
            print(f"[{__name__}] Dependency install failed: {e}", flush=True)

# Optional für Headless:
try:
    import matplotlib
    matplotlib.use("Agg")
except Exception:
    pass