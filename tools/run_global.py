"""One command for the global data (any PC with Python 3.10+, no installs):

    python tools/run_global.py

Downloads NASA FIRMS yearly global archives one by one (~7 GB in total, each deleted right after
it is counted), then builds web/data/global/frames.json and summary.json.
Already finished years (work/global/*.json) are skipped, so it can be stopped and restarted any time."""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = [("modis", y) for y in range(2000, 2026)] + [("viirs-snpp", y) for y in range(2012, 2026)]
PARALLEL = int(os.environ.get("PARALLEL", "3"))


def run(job):
    sensor, year = job
    if os.path.exists(os.path.join(HERE, "..", "work", "global", f"{sensor}_{year}.json")):
        return f"{sensor} {year}: already done"
    r = subprocess.run([sys.executable, os.path.join(HERE, "global_pipeline.py"), "aggregate", sensor, str(year)],
                       capture_output=True, text=True)
    return (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else f"{sensor} {year}: ?"


if __name__ == "__main__":
    with ThreadPoolExecutor(PARALLEL) as pool:
        for i, msg in enumerate(pool.map(run, JOBS), 1):
            print(f"[{i}/{len(JOBS)}] {msg}", flush=True)
    subprocess.run([sys.executable, os.path.join(HERE, "global_pipeline.py"), "build"], check=True)
    print("Done: web/data/global/frames.json + summary.json. Commit and push them.")
