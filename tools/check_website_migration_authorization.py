#!/usr/bin/env python3
"""Fail-closed authorization gate for replacing the authoritative W33 website index."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
RESTORED_INDEX_BLOB="41a8d733f42da18282fa276f5d2fa82bac7516f6"
AUTHORIZATION_SCHEMA="w33.website_migration_authorization.v1"
AUTHORIZATION_PHRASE="I_AUTHORIZE_REPLACING_THE_AUTHORITATIVE_INDEX"
DEFAULT_AUTHORIZATION_PATH=Path("data/website_migration_authorization.json")
class AuthorizationError(RuntimeError): pass
def git_blob_sha(data:bytes)->str: return hashlib.sha1(f"blob {len(data)}\0".encode("ascii")+data).hexdigest()
def _require(condition:bool,message:str)->None:
    if not condition: raise AuthorizationError(message)
def validate_website_index(repository_root:Path,*,expected_blob:str=RESTORED_INDEX_BLOB,authorization_path:Path=DEFAULT_AUTHORIZATION_PATH)->dict[str,Any]:
    root=repository_root.resolve(); index_path=root/"docs/index.html"
    _require(index_path.is_file(),f"missing authoritative index: {index_path}")
    actual_blob=git_blob_sha(index_path.read_bytes())
    if actual_blob==expected_blob: return {"status":"PASS_RESTORED_INDEX_UNCHANGED","actual_blob":actual_blob,"expected_blob":expected_blob,"authorization_used":False}
    auth_file=root/authorization_path
    _require(auth_file.is_file(),"docs/index.html changed without data/website_migration_authorization.json")
    try: authorization=json.loads(auth_file.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise AuthorizationError(f"invalid authorization JSON: {exc}") from exc
    _require(authorization.get("schema")==AUTHORIZATION_SCHEMA,"wrong authorization schema")
    _require(authorization.get("authorized") is True,"authorization must set authorized=true")
    _require(authorization.get("authorization_phrase")==AUTHORIZATION_PHRASE,"missing exact authorization phrase")
    _require(authorization.get("approved_by")=="wilcompute","approved_by must be wilcompute")
    reason=authorization.get("reason"); _require(isinstance(reason,str) and reason.strip(),"authorization reason must be nonempty")
    _require(authorization.get("previous_blob")==expected_blob,"authorization previous_blob mismatch")
    _require(authorization.get("new_blob")==actual_blob,"authorization new_blob mismatch")
    archive_value=authorization.get("archive_path"); _require(isinstance(archive_value,str) and archive_value.strip(),"archive_path must be nonempty")
    archive_path=(root/archive_value).resolve(); _require(root==archive_path or root in archive_path.parents,"archive_path escapes repository")
    _require(archive_path.is_file(),f"authorized archive missing: {archive_value}")
    archive_blob=git_blob_sha(archive_path.read_bytes()); _require(archive_blob==expected_blob,"archive is not an exact copy of the previous authoritative index")
    _require(authorization.get("archive_blob")==archive_blob,"authorization archive_blob mismatch")
    return {"status":"PASS_EXPLICIT_INDEX_MIGRATION_AUTHORIZATION","actual_blob":actual_blob,"expected_blob":expected_blob,"authorization_used":True,"authorization_path":str(authorization_path),"archive_path":archive_value,"archive_blob":archive_blob,"approved_by":"wilcompute"}
def main()->None:
    parser=argparse.ArgumentParser(); parser.add_argument("--repository-root",type=Path,default=Path(".")); parser.add_argument("--expected-blob",default=RESTORED_INDEX_BLOB); parser.add_argument("--authorization",type=Path,default=DEFAULT_AUTHORIZATION_PATH); parser.add_argument("--json",type=Path); args=parser.parse_args()
    try: result=validate_website_index(args.repository_root,expected_blob=args.expected_blob,authorization_path=args.authorization)
    except AuthorizationError as exc: print(f"FAIL_WEBSITE_MIGRATION_AUTHORIZATION: {exc}"); raise SystemExit(1) from exc
    if args.json: args.json.parent.mkdir(parents=True,exist_ok=True); args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(result["status"],result["actual_blob"])
if __name__=="__main__": main()
