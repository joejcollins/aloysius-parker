"""Configure the monitoring."""

import prometheus_flask_exporter
from flask import app


def configure_monitoring(flask_api: app.Flask) -> None:
    """Configure the Prometheus instrumentation and root logger."""
    prometheus_flask_exporter.PrometheusMetrics(flask_api)
