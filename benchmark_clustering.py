import time
from src.analytics.clustering import run_kmeans

start = time.perf_counter()

run_kmeans()

end = time.perf_counter()

print(f"Execution Time: {end - start:.3f} seconds")