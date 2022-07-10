from multiprocessing import cpu_count
from config import FLASK_HOST, FLASK_PORT

bind = f"{FLASK_HOST}:{FLASK_PORT}"
workers = cpu_count() * 2 + 1
threads = workers
