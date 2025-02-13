from prometheus_fastapi_instrumentator import Instrumentator

def setup_monitoring(app):
    instrumentator = Instrumentator().instrument(app)
    instrumentator.expose(app, endpoint="/metrics")
