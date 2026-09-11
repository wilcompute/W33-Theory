"""Atomic durable guest receipt consumption and exact four-root live closure.
Reuses the transaction/fault boundaries of w33_durable_microstep_owner.
The trusted SQLite database is the authority; rollback of the database is outside scope.
"""
from dataclasses import asdict
import json
import sqlite3
from w33_durable_microstep_owner import DurableOwner as MicroOwner
import w33_redundant_guest_abi as abi
from w33_authenticated_counter_machine import Bit,BitStore,ZERO


def closure(state,memory):
    seen={};pending=[r for p in state.pairs for r in p.roots]
    while pending:
        root=pending.pop()
        if root==ZERO or root in seen:continue
        node=memory.get(root);seen[root]=node;pending.append(node.tail)
    return [asdict(seen[k]) for k in sorted(seen)]


def pack(state,memory):
    body={'schema':'w33.durable-redundant-snapshot.v1','guest':asdict(state),'nodes':closure(state,memory)}
    wire=json.dumps(body,sort_keys=True,separators=(',',':'))
    if len(wire.encode())>32_000_000:raise ValueError('snapshot budget exceeded')
    return abi.digest(body),wire


def unpack(root,wire,program):
    if len(wire.encode())>32_000_000:raise ValueError('snapshot budget exceeded')
    body=json.loads(wire)
    if abi.digest(body)!=root or set(body)!={'schema','guest','nodes'} or body['schema']!='w33.durable-redundant-snapshot.v1':raise ValueError('corrupt snapshot')
    row=body['guest'];pairs=tuple(abi.primitive.Pair(tuple(p['roots']),p['generation'],p['session'],p['history']) for p in row['pairs'])
    state=abi.Guest(**{**row,'pairs':pairs})
    if state.image!=program.image_id or len(pairs)!=2:raise ValueError('foreign guest')
    memory=BitStore(Bit(**n) for n in body['nodes'])
    if closure(state,memory)!=body['nodes']:raise ValueError('closure mismatch')
    return state,memory


class DurableGuest:
    _transaction=MicroOwner._transaction
    close=MicroOwner.close
    def __init__(self,path,program,*,fault=None):
        if str(path) in ('',':memory:'):raise ValueError('persistent path required')
        self.program=program;self.fault=fault or (lambda phase:None)
        self.db=sqlite3.connect(path,isolation_level=None,timeout=10)
        try:
            self.db.execute('PRAGMA journal_mode=DELETE');self.db.execute('PRAGMA synchronous=FULL')
            self.db.execute('BEGIN IMMEDIATE')
            self.db.execute('CREATE TABLE IF NOT EXISTS guest_config (id INTEGER PRIMARY KEY CHECK(id=1), image TEXT NOT NULL)')
            self.db.execute('CREATE TABLE IF NOT EXISTS guest_heads (pid TEXT PRIMARY KEY, root TEXT NOT NULL, wire TEXT NOT NULL)')
            row=self.db.execute('SELECT image FROM guest_config WHERE id=1').fetchone()
            if row is None:self.db.execute('INSERT INTO guest_config VALUES (1,?)',(program.image_id,))
            elif row[0]!=program.image_id:raise ValueError('wrong database program')
            self.db.execute('COMMIT')
        except BaseException:self.db.close();raise

    def install(self,pid,values):
        if not isinstance(pid,str) or not pid:raise ValueError('explicit process ID required')
        memory=BitStore();state=abi.genesis(self.program,memory,values,pid)
        root,wire=pack(state,memory)
        with self._transaction():self.db.execute('INSERT INTO guest_heads VALUES (?,?,?)',(pid,root,wire))
        return state

    def read(self,pid):
        row=self.db.execute('SELECT root,wire FROM guest_heads WHERE pid=?',(pid,)).fetchone()
        if row is None:raise KeyError(pid)
        state,memory=unpack(*row,self.program)
        expected=tuple(abi.primitive.initial(0,BitStore(),pid+':'+str(j)).session for j in range(2))
        if tuple(p.session for p in state.pairs)!=expected:raise ValueError('wrong process row')
        return state,memory

    def submit(self,pid,receipt):
        with self._transaction():
            state,memory=self.read(pid)
            after,writes,_,_=abi.verify(self.program,state,receipt)
            for node in writes:memory.put(node)
            root,wire=pack(after,memory)
            self.db.execute('UPDATE guest_heads SET root=?,wire=? WHERE pid=?',(root,wire,pid))
        return after
