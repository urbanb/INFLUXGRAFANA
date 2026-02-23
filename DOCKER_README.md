# Docker Setup für Grafana + InfluxDB

## 🚀 Schnellstart

### 1. Docker starten
Stelle sicher, dass Docker Desktop läuft.

### 2. Services starten
```bash
cd /Users/sen01/.openclaw/workspace/INFLUXGRAFANA
docker-compose up -d
```

### 3. Zugriff

| Service | URL | Login |
|---------|-----|-------|
| **Grafana** | http://localhost:3000 | admin / admin |
| **InfluxDB** | http://localhost:8086 | admin / admin123 |

### 4. Dashboard ist automatisch da!

Das Dashboard `dashboard_all_fixed.json` wird automatisch in Grafana geladen.

---

## 📁 Struktur

```
INFLUXGRAFANA/
├── docker-compose.yml          # Docker Compose Konfiguration
├── grafana/
│   ├── dashboards/             # Dashboard JSONs
│   │   └── dashboard_all_fixed.json
│   └── provisioning/           # Automatische Konfiguration
│       ├── datasources/        # Datenquellen
│       └── dashboards/         # Dashboard-Provider
└── README.md
```

---

## 🐳 Docker Images

| Image | Zweck | Größe |
|-------|-------|-------|
| `influxdb:2.7` | Zeitreihen-Datenbank | ~200 MB |
| `grafana/grafana:latest` | Visualisierung | ~150 MB |

---

## 🛠️ Befehle

```bash
# Starten
docker-compose up -d

# Stoppen
docker-compose down

# Logs anzeigen
docker-compose logs -f

# Neu bauen (nach Änderungen)
docker-compose up -d --build

# Alles löschen (inkl. Daten!)
docker-compose down -v
```

---

## 📊 InfluxDB 2.x vs 3.x

Dieses Setup verwendet **InfluxDB 2.7** (nicht 3.0), weil:
- ✅ Bessere Grafana-Kompatibilität
- ✅ Eingebaute UI
- ✅ Einfachere Queries
- ✅ Keine Flight SQL nötig

---

## 🔗 Verbindung Telegraf → Docker InfluxDB

Falls du Telegraf weiterhin nutzen willst, ändere die Config:

```yaml
# In telegraf/telegraf.conf
urls = ["http://localhost:8086"]  # Bleibt gleich!
```

Telegraf sendet weiterhin an Port 8086, egal ob InfluxDB nativ oder in Docker läuft.

---

## 🛑 Deinstallation

```bash
docker-compose down -v
docker volume rm influxdb_data grafana_data
```