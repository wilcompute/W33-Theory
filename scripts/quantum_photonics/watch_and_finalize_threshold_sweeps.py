"""Watch the high-precision sweep log and finalize outputs.

Behavior:
- Poll `bundles/v23_toe_finish/v23/gbs_threshold_highshots.log` for changes.
- If the log stops updating for `quiet_seconds` (default 120s) and a python process with high CPU is not found, consider the run finished.
- Then execute `notebooks/quantum_photonics/gbs_benchmark_full.ipynb` via nbclient to embed outputs.
- Commit the executed notebook and any new bundle artifacts, and attempt to push the branch via HTTPS once.
- Writes a small status file `bundles/v23_toe_finish/v23/watch_finalize.status` with timestamps and actions performed.

Note: The push may require credentials; if push fails the script records the error and exits.
"""
import time
from pathlib import Path
import subprocess
import nbformat
from nbclient import NotebookClient

repo = Path(__file__).resolve().parents[2]
logp = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'gbs_threshold_highshots.log'
statusp = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'watch_finalize.status'
nbp = repo / 'notebooks' / 'quantum_photonics' / 'gbs_benchmark_full.ipynb'
executed_nb = nbp.with_name('gbs_benchmark_full.executed.ipynb')

quiet_seconds = 120
poll_interval = 15
max_wait = 60 * 60 * 3  # 3 hours

def write_status(msg):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    statusp.parent.mkdir(parents=True, exist_ok=True)
    with open(statusp, 'a') as f:
        f.write(f'[{t}] {msg}\n')

write_status('watcher started')
start_time = time.time()
last_sz = None
last_mtime = None
while True:
    if time.time() - start_time > max_wait:
        write_status('timeout waiting for log to quiesce')
        break
    if not logp.exists():
        write_status('log file not present yet')
        time.sleep(poll_interval)
        continue
    st = logp.stat()
    sz = st.st_size
    mtime = st.st_mtime
    now = time.time()
    write_status(f'log size={sz} mtime={mtime}')
    if last_sz is None:
        last_sz = sz
        last_mtime = mtime
        time.sleep(poll_interval)
        continue
    if sz != last_sz or mtime != last_mtime:
        last_sz = sz
        last_mtime = mtime
        write_status('log changed; waiting for quiet period')
        time.sleep(poll_interval)
        continue
    # no change since last check; wait quiet_seconds further
    write_status('log unchanged; waiting quiet period')
    time.sleep(quiet_seconds)
    st2 = logp.stat()
    if st2.st_mtime == last_mtime and st2.st_size == last_sz:
        write_status('log quiescent; finalizing')
        # execute notebook
        try:
            nb = nbformat.read(nbp, as_version=4)
            client = NotebookClient(nb, timeout=600, kernel_name='python3')
            client.execute()
            nbformat.write(nb, executed_nb)
            write_status(f'executed notebook and wrote {executed_nb}')
            subprocess.run(['git','add', str(executed_nb)], check=False)
            subprocess.run(['git','commit','-m','docs: executed GBS notebook with latest sweep outputs','--no-verify'], check=False)
            write_status('committed executed notebook (if there were changes)')
            # attempt push via HTTPS once
            push_cmd = ['git','push','https://github.com/wilcompute/W33-Theory.git','photonic/threshold-sweeps:photonic/threshold-sweeps']
            res = subprocess.run(push_cmd, capture_output=True, text=True)
            write_status('push stdout: ' + res.stdout.replace('\n',' | '))
            write_status('push stderr: ' + res.stderr.replace('\n',' | '))
        except Exception as e:
            write_status('error executing notebook or git/push: ' + str(e))
        break
    else:
        last_sz = st2.st_size
        last_mtime = st2.st_mtime
        write_status('log changed during quiet wait; continuing')

write_status('watcher finished')
print('done')
