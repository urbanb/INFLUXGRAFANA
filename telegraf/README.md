# Telegraf Setup für OpenClaw Metrics

## 🚀 Übersicht

Telegraf sammelt automatisch Metriken und sendet sie an InfluxDB.

## 📊 Was wird erfasst

| Metrik | Quelle | Intervall |
|--------|--------|-----------|
| OpenClaw Events | HTTP API | Echtzeit |
| CPU Usage | System | 10s |
| Memory | System | 10s |
| Disk Usage | System | 10s |
| Disk I/O | System | 10s |
| Prozesse | System | 10s |

## 🔧 Konfiguration

### Dateien

```
telegraf/
├── telegraf.conf          # Hauptkonfiguration
└── metrics_sender.py      # Python-Client
```

### HTTP Endpunkt

```
POST http://localhost:8180/telegraf
Content-Type: text/plain

measurement,tag=value field=value timestamp
```

## 🚀 Starten

### Manuell
```bash
cd /Users/sen01/.openclaw/workspace/INFLUXGRAFANA
telegraf -config telegraf/telegraf.conf
```

### Als Hintergrund-Service
```bash
cd /Users/sen01/.openclaw/workspace/INFLUXGRAFANA
nohup telegraf -config telegraf/telegraf.conf > /tmp/telegraf.log 2>&1 &
```

## 🐍 Python-Usage

```python
from metrics_sender import log_tool_usage, log_message_sent, log_session_start

# Tool-Nutzung loggen
log_tool_usage("browser", success=True)

# Nachricht loggen
log_message_sent("text")

# Session start
log_session_start()
```

## 🧪 Test

```bash
cd telegraf
python3 metrics_sender.py
```

## 📈 Dashboard

Die Daten erscheinen automatisch im Grafana Dashboard unter:
http://localhost:3000

## 🛑 Stoppen

```bash
pkill -f telegraf
```

## 📋 Status prüfen

```bash
# Läuft Telegraf?
ps aux | grep telegraf

# Letzte Logs
tail -f /tmp/telegraf.log

# Metriken in InfluxDB prüfen
influxdb3 query "SELECT * FROM tool_usage ORDER BY time DESC LIMIT 5" \
  --database openclaw_metrics \
  --token $INFLUX_TOKEN
```