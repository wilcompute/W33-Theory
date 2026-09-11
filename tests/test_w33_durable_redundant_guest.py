"""Restart, process-death, competing writers and forged-receipt controls."""
from pathlib import Path
import sys,json,subprocess,tempfile,unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from dataclasses import replace
ANALYSIS=Path(__file__).resolve().parents[1]/'analysis';sys.path.insert(0,str(ANALYSIS))
import w33_durable_redundant_guest as d
from w33_typed_universal_microvm import Program,Instruction
P=Program((Instruction('DECJZ',0,1,2),Instruction('INC',1,0),Instruction('HALT')),name='durable-transfer')
WORKER="""
import sys,os
sys.path.insert(0,sys.argv[1])
import w33_durable_redundant_guest as d
from w33_typed_universal_microvm import Program,Instruction
p=Program((Instruction('DECJZ',0,1,2),Instruction('INC',1,0),Instruction('HALT')),name='durable-transfer')
o=d.DurableGuest(sys.argv[2],p,fault=lambda s:os._exit(73) if s==sys.argv[3] else None)
s,m=o.read('p');o.submit('p',d.abi.prove(p,s,m))
"""

class Tests(unittest.TestCase):
    def test_restart_each_guest_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            for a in range(3):
                for b in range(3):
                    path=Path(tmp)/f'{a}-{b}.db';o=d.DurableGuest(path,P);o.install('p',(a,b))
                    while True:
                        s,m=o.read('p')
                        if s.halted:break
                        r=d.abi.prove(P,s,m);o.submit('p',r);o.close();o=d.DurableGuest(path,P)
                        with self.assertRaises(ValueError):o.submit('p',r)
                    self.assertEqual(tuple(d.abi.primitive.inspect(p,m)[2] for p in s.pairs),(0,a+b));o.close()

    def test_process_death_at_commit_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            for phase in ('before_commit','after_commit'):
                path=Path(tmp)/(phase+'.db');o=d.DurableGuest(path,P);before=o.install('p',(7,2));s,m=o.read('p');r=d.abi.prove(P,s,m);o.close()
                killed=subprocess.run([sys.executable,'-c',WORKER,str(ANALYSIS),str(path),phase],capture_output=True,text=True,timeout=30)
                self.assertEqual(killed.returncode,73,killed.stderr)
                o=d.DurableGuest(path,P);s,m=o.read('p')
                self.assertEqual(s.steps,0 if phase=='before_commit' else 1)
                if phase=='before_commit':self.assertEqual(s,before);o.submit('p',r)
                else:
                    with self.assertRaises(ValueError):o.submit('p',r)
                o.close()

    def test_writer_race_and_process_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'race.db';o=d.DurableGuest(path,P);o.install('p',(7,2));o.install('q',(7,2));s,m=o.read('p');r=d.abi.prove(P,s,m)
            with self.assertRaises(ValueError):o.submit('q',r)
            with self.assertRaises(ValueError):o.submit('p',replace(r,after=replace(r.after,pc=2)))
            o.close();barrier=Barrier(2)
            def run():
                owner=d.DurableGuest(path,P)
                try:
                    barrier.wait(timeout=10);owner.submit('p',r);return 'accepted'
                except ValueError:return 'rejected'
                finally:owner.close()
            with ThreadPoolExecutor(2) as pool:
                fs=[pool.submit(run) for _ in range(2)]
                self.assertEqual(sorted(f.result(timeout=20) for f in fs),['accepted','rejected'])

    def test_snapshot_corruption_and_wrong_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.db';o=d.DurableGuest(path,P);o.install('p',(7,2))
            with self.assertRaises(ValueError):d.DurableGuest(path,Program((Instruction('HALT'),),name='other'))
            root,wire=o.db.execute('SELECT root,wire FROM guest_heads').fetchone();body=json.loads(wire);body['nodes'].pop()
            o.db.execute('UPDATE guest_heads SET root=?,wire=?',(d.abi.digest(body),json.dumps(body)))
            with self.assertRaises((KeyError,ValueError)):o.read('p')
            o.close()

if __name__=='__main__':
    result=unittest.main(exit=False).result
    row=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
             boundary='SQLite process-death/restart tests, not physical power loss or external I/O exactly-once semantics.')
    (ANALYSIS/'w33_durable_redundant_guest.json').write_text(json.dumps(row,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
