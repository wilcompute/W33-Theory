#!/usr/bin/env python3
"""Export Holonet-UOR certificate constraints as Turtle/SHACL."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TTL = ROOT / "docs" / "holonet_uor_certificate_shapes.ttl"
DEFAULT_JSON = ROOT / "data" / "holonet_uor_shacl_export.json"


TTL = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix w33: <https://w33.local/schema/> .
@prefix u: <https://uor.foundation/u/> .
@prefix proof: <https://uor.foundation/proof/> .
@prefix trace: <https://uor.foundation/trace/> .
@prefix cert: <https://uor.foundation/cert/> .

w33:HolonetUorCertificateShape
    a sh:NodeShape ;
    sh:targetClass w33:HolonetUorCertificate ;
    sh:property [ sh:path w33:schema ; sh:minCount 1 ; sh:hasValue "w33.holonet.uor_certificate.v1" ] ;
    sh:property [ sh:path w33:status ; sh:minCount 1 ; sh:hasValue "PASS" ] ;
    sh:property [ sh:path w33:element ; sh:minCount 1 ; sh:node w33:ElementShape ] ;
    sh:property [ sh:path w33:transport_partition ; sh:minCount 1 ; sh:node w33:TransportPartitionShape ] ;
    sh:property [ sh:path w33:proof ; sh:minCount 1 ; sh:node w33:ProofShape ] ;
    sh:property [ sh:path w33:trace ; sh:minCount 1 ; sh:node w33:TraceShape ] ;
    sh:property [ sh:path w33:certificate ; sh:minCount 1 ; sh:node w33:CertificateShape ] .

w33:ElementShape
    a sh:NodeShape ;
    sh:property [ sh:path u:digestAlgorithm ; sh:minCount 1 ; sh:hasValue "sha256" ] ;
    sh:property [ sh:path u:digest ; sh:minCount 1 ; sh:pattern "^sha256:[0-9a-f]{64}$" ] ;
    sh:property [ sh:path u:length ; sh:minCount 1 ; sh:datatype xsd:integer ; sh:minInclusive 1 ] ;
    sh:property [ sh:path w33:canonicalBytesSha256 ; sh:minCount 1 ; sh:pattern "^[0-9a-f]{64}$" ] .

w33:TransportPartitionShape
    a sh:NodeShape ;
    sh:property [ sh:path w33:kind ; sh:minCount 1 ; sh:hasValue "HolonetTransportPartition" ] ;
    sh:property [ sh:path w33:complete ; sh:minCount 1 ; sh:hasValue true ] ;
    sh:property [ sh:path w33:cardinality_sum ; sh:minCount 1 ; sh:datatype xsd:integer ; sh:minInclusive 1 ] ;
    sh:property [ sh:path w33:components ; sh:minCount 1 ] .

w33:ProofShape
    a sh:NodeShape ;
    sh:property [ sh:path proof:kind ; sh:minCount 1 ; sh:hasValue "HolonetUorBridgeProof" ] ;
    sh:property [ sh:path w33:checks ; sh:minCount 1 ] ;
    sh:property [ sh:path w33:critical_identity_clock ; sh:minCount 1 ] ;
    sh:property [ sh:path w33:substrate_checksum ; sh:minCount 1 ] .

w33:TraceShape
    a sh:NodeShape ;
    sh:property [ sh:path trace:kind ; sh:minCount 1 ; sh:hasValue "HolonetComputationTrace" ] ;
    sh:property [ sh:path w33:packet_steps ; sh:minCount 1 ] ;
    sh:property [ sh:path w33:observables ; sh:minCount 1 ] .

w33:CertificateShape
    a sh:NodeShape ;
    sh:property [ sh:path cert:valid ; sh:minCount 1 ; sh:hasValue true ] ;
    sh:property [ sh:path w33:attests ; sh:minCount 1 ] ;
    sh:property [ sh:path w33:boundary ; sh:minCount 1 ] .
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ttl", default=str(DEFAULT_TTL))
    parser.add_argument("--json", default=str(DEFAULT_JSON))
    args = parser.parse_args(argv)

    ttl_path = Path(args.ttl) if Path(args.ttl).is_absolute() else ROOT / args.ttl
    json_path = Path(args.json) if Path(args.json).is_absolute() else ROOT / args.json
    ttl_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    ttl_path.write_text(TTL, encoding="utf-8")
    digest = hashlib.sha256(TTL.encode("utf-8")).hexdigest()
    report = {
        "schema": "w33.holonet.uor_shacl_export.v1",
        "status": "PASS",
        "ttl_path": str(ttl_path.relative_to(ROOT)),
        "shape_count": TTL.count("a sh:NodeShape"),
        "property_constraint_count": TTL.count("sh:property"),
        "sha256": digest,
    }
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"status: {report['status']}")
    print(f"shapes: {report['shape_count']}")
    print(f"constraints: {report['property_constraint_count']}")
    print(f"wrote: {ttl_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
