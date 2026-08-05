import importlib.util,json
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1]/"tools/check_website_migration_authorization.py"
s=importlib.util.spec_from_file_location("lock",P); lock=importlib.util.module_from_spec(s); s.loader.exec_module(lock)
def put(root,data):
 p=root/"docs/index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
def test_unchanged(tmp_path):
 old=b"old\n"; put(tmp_path,old); assert lock.validate_website_index(tmp_path,expected_blob=lock.git_blob_sha(old))["authorization_used"] is False
def test_unauthorized_change(tmp_path):
 old=b"old\n"; put(tmp_path,b"new\n")
 with pytest.raises(lock.AuthorizationError): lock.validate_website_index(tmp_path,expected_blob=lock.git_blob_sha(old))
def test_authorized_archived_change(tmp_path):
 old=b"old\n"; new=b"new\n"; prev=lock.git_blob_sha(old); now=lock.git_blob_sha(new); put(tmp_path,new); a=tmp_path/"docs/archive/old.html"; a.parent.mkdir(parents=True,exist_ok=True); a.write_bytes(old); auth={"schema":lock.AUTHORIZATION_SCHEMA,"authorized":True,"authorization_phrase":lock.AUTHORIZATION_PHRASE,"approved_by":"wilcompute","reason":"test","previous_blob":prev,"new_blob":now,"archive_path":"docs/archive/old.html","archive_blob":prev}; q=tmp_path/"data/website_migration_authorization.json"; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(auth)); assert lock.validate_website_index(tmp_path,expected_blob=prev)["authorization_used"] is True
def test_wrong_archive_fails(tmp_path):
 old=b"old\n"; new=b"new\n"; prev=lock.git_blob_sha(old); now=lock.git_blob_sha(new); put(tmp_path,new); a=tmp_path/"docs/archive/old.html"; a.parent.mkdir(parents=True,exist_ok=True); a.write_bytes(b"wrong\n"); auth={"schema":lock.AUTHORIZATION_SCHEMA,"authorized":True,"authorization_phrase":lock.AUTHORIZATION_PHRASE,"approved_by":"wilcompute","reason":"test","previous_blob":prev,"new_blob":now,"archive_path":"docs/archive/old.html","archive_blob":prev}; q=tmp_path/"data/website_migration_authorization.json"; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(auth));
 with pytest.raises(lock.AuthorizationError): lock.validate_website_index(tmp_path,expected_blob=prev)
