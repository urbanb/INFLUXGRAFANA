# INFLUXGRAFANA

InfluxDB & Grafana Setup für Monitoring und Metriken

## 📊 Übersicht

Dieses Repository enthält:
- InfluxDB 3.0 Setup für lokale Metrik-Erfassung
- Grafana-Dashboard-Konfiguration
- Python-Scripts für automatisches Reporting

## 🚀 Schnellstart

### 1. InfluxDB starten
```bash
influxdb3 serve --node-id local --object-store memory &
```

### 2. Grafana starten
```bash
brew services start grafana
# Oder: http://localhost:3000
```

### 3. Metriken schreiben
```bash
python3 influx_metrics.py
```

## 📁 Struktur

```
INFLUXGRAFANA/
├── influx_metrics.py    # Python-Client für InfluxDB
├── grafana/             # Dashboard-JSONs
├── README.md
└── docs/                # Weitere Dokumentation
```

## 🔗 Links

- InfluxDB: http://localhost:8181
- Grafana: http://localhost:3000 (admin/admin)

---

*Erstellt mit OpenClaw*