import time
import threading
import sys
import os
from datetime import datetime, timedelta

EP = 1420070400000

OUTPUT_FILE = "output/results.txt"
OUTPUT_FRESH = "output/fresh.txt"
OUTPUT_30_DAYS = "output/30_days.txt"
OUTPUT_6_MONTH = "output/6_month.txt"
OUTPUT_1_YEAR = "output/1_year.txt"

fp_count = 0
fp_lock = threading.Lock()
start_time = None

colors = {
    "purple": "\x1b[35m",
    "cyan": "\x1b[36m",
    "green": "\x1b[32m",
    "red": "\x1b[31m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "reset": "\x1b[0m",
}

banner = """
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████─██████████████─██████──────────██████──────────────────────██████████████─██████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██████████████░░██──────────────────────██░░░░░░░░░░██─██░░░░░░██─
─██████░░██████─██░░██████████─██░░██████░░██─██░░░░░░░░░░░░░░░░░░██──────────────────────██░░██████░░██─████░░████─
─────██░░██─────██░░██─────────██░░██──██░░██─██░░██████░░██████░░██──────────────────────██░░██──██░░██───██░░██───
─────██░░██─────██░░██████████─██░░██████░░██─██░░██──██░░██──██░░██────██████████████────██░░██████░░██───██░░██───
─────██░░██─────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██──██░░██──██░░██────██░░░░░░░░░░██────██░░░░░░░░░░██───██░░██───
─────██░░██─────██░░██████████─██░░██████░░██─██░░██──██████──██░░██────██████████████────██░░██████░░██───██░░██───
─────██░░██─────██░░██─────────██░░██──██░░██─██░░██──────────██░░██──────────────────────██░░██──██░░██───██░░██───
─────██░░██─────██░░██████████─██░░██──██░░██─██░░██──────────██░░██──────────────────────██░░██──██░░██─████░░████─
─────██░░██─────██░░░░░░░░░░██─██░░██──██░░██─██░░██──────────██░░██──────────────────────██░░██──██░░██─██░░░░░░██─
─────██████─────██████████████─██████──██████─██████──────────██████──────────────────────██████──██████─██████████─
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                         made by @ai.legend.
"""

def get_timestamp():
    now = time.localtime()
    return f"{now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"

def print_info(msg, thread_id=None):
    prefix = f"[T{thread_id}] " if thread_id else ""
    print(f"{colors['purple']}[{get_timestamp()}]{colors['reset']} {colors['cyan']}[ * ]{colors['reset']} {prefix}{msg}")

def print_success(msg, thread_id=None):
    prefix = f"[T{thread_id}] " if thread_id else ""
    print(f"{colors['purple']}[{get_timestamp()}]{colors['reset']} {colors['green']}[ + ]{colors['reset']} {prefix}{msg}")

def print_error(msg, thread_id=None):
    prefix = f"[T{thread_id}] " if thread_id else ""
    print(f"{colors['purple']}[{get_timestamp()}]{colors['reset']} {colors['red']}[ - ]{colors['reset']} {prefix}{msg}")

def print_other(msg, thread_id=None):
    prefix = f"[T{thread_id}] " if thread_id else ""
    print(f"{colors['purple']}[{get_timestamp()}]{colors['reset']} {colors['yellow']}[ & ]{colors['reset']} {prefix}{msg}")

def age(fingerprintinteger: int) -> dict:
    args = {}
    
    created_at_ts = ((fingerprintinteger >> 22) + EP) / 1000
    created_at_dt = datetime.utcfromtimestamp(created_at_ts)
    
    created_at_ist = created_at_dt + timedelta(hours=5, minutes=30)

    now_dt = datetime.utcnow()
    delta = now_dt - created_at_dt

    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30

    if years > 0:
        age_str = f"{years} Years {months} Months"
    elif months > 0:
        age_str = f"{months} Months {days} Days"
    else:
        age_str = f"{days} Days"

    args["age"] = age_str
    args["created_at"] = created_at_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    
    return args

write_buffer = []
buffer_lock = threading.Lock()
file_counts = {
    "OUTPUT_FRESH": 0,
    "OUTPUT_30_DAYS": 0,
    "OUTPUT_6_MONTH": 0,
    "OUTPUT_1_YEAR": 0
}
counts_lock = threading.Lock()

def flush_worker():
    while True:
        time.sleep(1)
        with buffer_lock:
            if write_buffer:
                file_groups = {}
                for output_file, result in write_buffer:
                    if output_file not in file_groups:
                        file_groups[output_file] = []
                    file_groups[output_file].append(result)
                
                for output_file, results in file_groups.items():
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write("\n".join(results) + "\n")
                
                write_buffer.clear()

def check(fingerprint: str, thread_id=None) -> dict:
    try:
        fp_numeric = fingerprint.split(".", 1)[0]
        fp_int = int(fp_numeric)
        
        info = age(fp_int)
        
        with fp_lock:
            global fp_count
            fp_count += 1
        
        age_str = info['age']
        result = fingerprint
        
        created_at_ts = ((fp_int >> 22) + EP) / 1000
        created_at_dt = datetime.utcfromtimestamp(created_at_ts)
        now_dt = datetime.utcnow()
        delta = now_dt - created_at_dt
        days = delta.days
        
        with buffer_lock:
            if days < 30:
                write_buffer.append((OUTPUT_FRESH, result))
                with counts_lock:
                    file_counts["OUTPUT_FRESH"] += 1
            elif days < 180:
                write_buffer.append((OUTPUT_30_DAYS, result))
                with counts_lock:
                    file_counts["OUTPUT_30_DAYS"] += 1
            elif days < 365: 
                write_buffer.append((OUTPUT_6_MONTH, result))
                with counts_lock:
                    file_counts["OUTPUT_6_MONTH"] += 1
            else:
                write_buffer.append((OUTPUT_1_YEAR, result))
                with counts_lock:
                    file_counts["OUTPUT_1_YEAR"] += 1
        
        fp_preview = fingerprint[-5:]
        colored_preview = f"...{colors['blue']}{fp_preview}{colors['reset']}"
        print_success(f"Checked FingerPrint [{colored_preview}] | Age: {age_str} | Created: {info['created_at']}", thread_id)
        
        return info
        
    except Exception as e:
        print_error(f"Invalid fingerprint format: {str(e)}", thread_id)
        return None

def worker(thread_id, fingerprints: list):
    print_info("Thread started", thread_id)
    
    for fingerprint in fingerprints:
        if fingerprint.strip():
            check(fingerprint.strip(), thread_id)
    
    print_info("Thread completed", thread_id)

def speed_monitor(total_fps):
    global fp_count
    last_count = 0

    while True:
        time.sleep(1)
        with fp_lock:
            current_count = fp_count

        fps = current_count - last_count
        last_count = current_count

        if current_count >= total_fps:
            break

        title_text = f"Speed {fps} fps - {current_count}/{total_fps} checked"
        os.system(f"title {title_text}")

def load(filename="input/fp.txt"):
    try:
        with open(filename, "r") as f:
            fingerprints = [line.strip() for line in f if line.strip()]
        if fingerprints:
            print_success(f"Loaded {len(fingerprints)} fingerprint(s)")
            return fingerprints
        else:
            print_error("No fingerprints found in input/fp.txt")
            return []
    except FileNotFoundError:
        print_error("input/fp.txt not found")
        return []

def main():
    global start_time

    print(f"{colors['purple']}{banner}{colors['reset']}")

    threading.Thread(target=flush_worker, daemon=True).start()
    
    fingerprints = load()
    
    if not fingerprints:
        print_info("No fingerprints file found. Enter fingerprints manually.")
        fingerprints = []
        while True:
            fp = input(f"{colors['yellow']}Enter fingerprint (or 'done' to finish): {colors['reset']}")
            if fp.lower() == "done":
                break
            if fp.strip():
                fingerprints.append(fp.strip())
        
        if not fingerprints:
            print_error("No fingerprints to check")
            return
    
    try:
        num_threads = int(input(f"{colors['yellow']}Enter number of threads: {colors['reset']}"))
        if num_threads < 1:
            num_threads = 1
    except ValueError:
        num_threads = 1
    
    print_info(f"Starting with {num_threads} thread(s) to check {len(fingerprints)} fingerprint(s)")
    
    start_time = time.time()
    
    monitor_thread = threading.Thread(target=speed_monitor, args=(len(fingerprints),), daemon=True)
    monitor_thread.start()
    
    fingerprints_per_thread = [[] for _ in range(num_threads)]
    for i, fp in enumerate(fingerprints):
        fingerprints_per_thread[i % num_threads].append(fp)
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker,
            args=(i + 1, fingerprints_per_thread[i]),
            daemon=True
        )
        threads.append(thread)
        thread.start()
    
    try:
        for thread in threads:
            thread.join()
        
        time.sleep(2)
        
        print_success(f"Fingerprint check completed! {fp_count} total checked")
        
    except KeyboardInterrupt:
        print_other("\nShutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
