from __future__ import annotations
from pathlib import Path
import shutil
from typing import List

# Radice del repository (..\IFC_Thesis_BIM45D)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Cartella temporanea unificata
TEMP_DIR_NAME = "temp"
TEMP_DIR = REPO_ROOT / TEMP_DIR_NAME

# Vecchi percorsi temporanei presenti nel progetto
LEGACY_DIRS = [
    REPO_ROOT / "downloads",
    REPO_ROOT / "temp_downloads",
    REPO_ROOT / "temp-download",
    REPO_ROOT / "static",  # solo copia del file temp_model.ifc, non rimuovere la cartella
]


def ensure_temp_dir() -> Path:
    """Crea (se necessario) e restituisce la cartella temporanea unificata."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    return TEMP_DIR


def _copy_or_move(src: Path, dest: Path, must_move: bool) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if must_move:
        try:
            if dest.exists():
                dest.unlink()
        except Exception:
            pass
        shutil.move(str(src), str(dest))
    else:
        try:
            if dest.exists():
                dest.unlink()
        except Exception:
            pass
        shutil.copy2(str(src), str(dest))


def migrate_legacy_temp_dirs() -> List[str]:
    """Migra contenuti temporanei noti dai vecchi percorsi alla cartella unificata.

    Regole:
    - downloads/temp_model.ifc e temp_downloads/temp_model.ifc: spostati in temp.
    - static/temp_model.ifc: copiato in temp (si mantiene l'asset in static per compatibilità).
    - temp-download/properties/**: spostato/accorpato in temp/properties.
    - rimuove le cartelle legacy vuote (eccetto 'static').
    """
    ensure_temp_dir()
    moved: List[str] = []

    for d in LEGACY_DIRS:
        if not d.exists():
            continue

        try:
            if d.name in ("downloads", "temp_downloads"):
                src = d / "temp_model.ifc"
                if src.exists() and src.is_file():
                    _copy_or_move(src, TEMP_DIR / "temp_model.ifc", must_move=True)
                    moved.append(str(TEMP_DIR / "temp_model.ifc"))

            elif d.name == "static":
                # Non rimuovere il file originale in static per non rompere eventuali riferimenti esistenti.
                src = d / "temp_model.ifc"
                if src.exists() and src.is_file():
                    _copy_or_move(src, TEMP_DIR / "temp_model.ifc", must_move=False)
                    moved.append(str(TEMP_DIR / "temp_model.ifc"))

            elif d.name == "temp-download":
                prop = d / "properties"
                if prop.exists() and prop.is_dir():
                    dest_dir = TEMP_DIR / "properties"
                    if dest_dir.exists():
                        # Merge dei contenuti
                        for p in prop.rglob("*"):
                            if p.is_file():
                                rel = p.relative_to(prop)
                                _copy_or_move(p, dest_dir / rel, must_move=True)
                        # Rimuovi la dir originaria se svuotata
                        try:
                            shutil.rmtree(prop, ignore_errors=True)
                        except Exception:
                            pass
                    else:
                        shutil.move(str(prop), str(dest_dir))
                    moved.append(str(dest_dir))

            # Pulisci cartelle legacy se ora vuote (tranne 'static')
            if d.name in ("downloads", "temp_downloads", "temp-download"):
                try:
                    # Se non contiene più nulla, rimuovila
                    if d.exists() and not any(d.iterdir()):
                        d.rmdir()
                except Exception:
                    pass
        except Exception:
            # Non interrompere il flusso in caso di errori; prosegui con il resto.
            continue

    return moved


def purge_temp_dir() -> None:
    """Svuota completamente la cartella temporanea unificata."""
    if not TEMP_DIR.exists():
        return
    for p in TEMP_DIR.iterdir():
        try:
            if p.is_file() or p.is_symlink():
                p.unlink()
            elif p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
        except Exception:
            # Ignora errori di pulizia su singoli file
            pass


def consolidate_and_cleanup(remove_static_temp: bool = False) -> dict:
    """Consolidate all legacy temp artifacts into the unified temp/ folder and
    delete unnecessary folders/files.

    - Moves/copies legacy files using migrate_legacy_temp_dirs()
    - Removes folders: downloads/, temp_downloads/, temp-download/
    - Optionally removes static/temp_model.ifc
    """
    moved = migrate_legacy_temp_dirs()

    removed_dirs = []
    for name in ("downloads", "temp_downloads", "temp-download"):
        d = REPO_ROOT / name
        if d.exists():
            try:
                shutil.rmtree(d, ignore_errors=True)
                removed_dirs.append(str(d))
            except Exception:
                pass

    removed_files = []
    if remove_static_temp:
        sf = REPO_ROOT / "static" / "temp_model.ifc"
        if sf.exists():
            try:
                sf.unlink()
                removed_files.append(str(sf))
            except Exception:
                pass

    return {"moved": moved, "removed_dirs": removed_dirs, "removed_files": removed_files}


def _is_in_protected_dir(path: Path) -> bool:
    protected = {".venv", ".git", ".github"}
    parts = set(path.parts)
    return any(p in protected for p in parts)


def remove_caches() -> dict:
    """Remove Python cache directories and files across the repo, excluding protected dirs."""
    removed_dirs, removed_files = [], []
    try:
        for d in REPO_ROOT.rglob("__pycache__"):
            if _is_in_protected_dir(d):
                continue
            try:
                shutil.rmtree(d, ignore_errors=True)
                removed_dirs.append(str(d))
            except Exception:
                pass
        for f in REPO_ROOT.rglob("*.pyc"):
            if _is_in_protected_dir(f):
                continue
            try:
                f.unlink()
                removed_files.append(str(f))
            except Exception:
                pass
    except Exception:
        pass
    return {"removed_dirs": removed_dirs, "removed_files": removed_files}


def cleanup_all(remove_static_temp: bool = True, clean_caches: bool = True) -> dict:
    """Full cleanup: ensure temp/, consolidate legacy, optionally remove static temp and caches."""
    ensure_temp_dir()
    summary = consolidate_and_cleanup(remove_static_temp=remove_static_temp)
    cache_summary = {"removed_dirs": [], "removed_files": []}
    if clean_caches:
        cache_summary = remove_caches()
    return {"consolidation": summary, "caches": cache_summary}


if __name__ == "__main__":
    # Lightweight CLI: python -m tools.pathhelper [--remove-static-temp] [--no-clean-caches]
    import argparse
    parser = argparse.ArgumentParser(description="Consolidate temp artifacts and remove legacy folders.")
    parser.add_argument("--remove-static-temp", action="store_true", help="Also delete static/temp_model.ifc if present")
    parser.add_argument("--no-clean-caches", action="store_true", help="Do not remove __pycache__ and *.pyc")
    args = parser.parse_args()

    ensure_temp_dir()
    result = cleanup_all(remove_static_temp=args.remove_static_temp, clean_caches=not args.no_clean_caches)

    print("Cleanup summary:")
    print(f" - moved: {len(result['consolidation'].get('moved', []))}")
    print(f" - removed legacy dirs: {len(result['consolidation'].get('removed_dirs', []))}")
    print(f" - removed legacy files: {len(result['consolidation'].get('removed_files', []))}")
    print(f" - removed cache dirs: {len(result['caches'].get('removed_dirs', []))}")
    print(f" - removed cache files: {len(result['caches'].get('removed_files', []))}")
