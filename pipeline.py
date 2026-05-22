#!/usr/bin/env python3
import json, csv, ipaddress, sys
from pathlib import Path
from datetime import datetime, timezone

# Usamos la ruta donde está el script para evitar problemas de carpetas en Windows
BASE = Path(__file__).parent.resolve()
DATA = BASE / "data.json"
OUT = BASE / "out.csv"
LOG = BASE / "run.log"
TS = lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{TS()} {msg}\n")

def main():
    if not DATA.exists():
        print("data.json no encontrado", file=sys.stderr)
        sys.exit(2)
        
    with open(DATA, "r", encoding="utf-8") as f:
        raw = json.load(f)
        
    rows=[]
    for r in raw:
        host = (r.get("host") or "").strip().lower()
        ip_raw = (r.get("ip") or "").strip()
        try:
            ip = str(ipaddress.ip_address(ip_raw))
            status = "valid"
        except Exception:
            ip = ""
            status = "invalid"
            
        rec = {"host": host, "ip": ip, "status": status, "checked_at": TS()}
        rows.append(rec)
        log(f"proc {host} ip={ip or '<invalid>'} status={status}")
        
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["host","ip","status","checked_at"])
        w.writeheader()
        w.writerows(rows)
        
    with open(BASE / "README36.txt", "w", encoding="utf-8") as r:
        texto = f"Processed {len(rows)} records, "
        texto += f"invalids={sum(1 for x in rows if x['status']=='invalid')}\n"
        r.write(texto)
        
    print(f"Done: {len(rows)} records -> {OUT.name}; log: {LOG.name}")

if __name__ == "__main__":
    main()