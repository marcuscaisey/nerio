import multiprocessing

accesslog = "-"
bind = "0.0.0.0:8000"
workers = 2 * multiprocessing.cpu_count() + 1
