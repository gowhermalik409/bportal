import multiprocessing

# Bind to port (Render automatically provides PORT env)
bind = "0.0.0.0:" + str(__import__("os").environ.get("PORT", 8000))

# Workers (optimized for most small deployments)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker type
worker_class = "sync"

# Timeout (important for slow APIs)
timeout = 120

# Keep connections alive
keepalive = 5

# Logs (Render captures stdout/stderr)
accesslog = "-"
errorlog = "-"

# Auto-restart workers (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 100
