#!/usr/bin/env python3
"""Pass 1056: exact conjugacy-class fusions of both order-648 stabilizers."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

from w33_pass1054_1059_core import build_w33_bundle, cycle_partition, permutation_images


def element_key(element: Permutation, degree: int = 40) -> tuple[int, ...]:
    return tuple(permutation_images(element, degree))


def class_key(conjugacy_class: set[Permutation]) -> tuple[object, ...]:
    representative = min(conjugacy_class, key=element_key)
    return int(representative.order()), len(conjugacy_class), cycle_partition(representative, 40), element_key(representative)


def class_record(conjugacy_class: set[Permutation], group_order: int) -> dict[str, object]:
    representative = min(conjugacy_class, key=element_key)
    partition = cycle_partition(representative, 40)
    return {
        "class_size": len(conjugacy_class),
        "element_order": int(representative.order()),
        "cycle_partition": list(partition),
        "fixed_points": partition.count(1),
        "centralizer_order": group_order // len(conjugacy_class),
        "representative_images": permutation_images(representative, 40),
    }


def normal_27_profile(group: PermutationGroup) -> dict[str, object]:
    elements = sorted(group.generate_schreier_sims(), key=element_key)
    candidates = {}
    for element in elements:
        if element.is_identity or element.order() != 3:
            continue
        closure = group.normal_closure(PermutationGroup([element]))
        if closure.order() == 27:
            candidates[frozenset(closure.generate_schreier_sims())] = closure
    if len(candidates) != 1:
        raise AssertionError(f"expected one normal subgroup of order 27, found {len(candidates)}")
    normal = next(iter(candidates.values()))
    return {
        "order": int(normal.order()),
        "abelian": bool(normal.is_abelian),
        "center_order": int(normal.center().order()),
        "derived_order": int(normal.derived_subgroup().order()),
        "exponent_orders": dict(sorted(Counter(int(element.order()) for element in normal.generate_schreier_sims()).items())),
    }


def fusion_table(subgroup, ambient_classes, ambient_class_of, ambient_records):
    subgroup_classes = sorted(subgroup.conjugacy_classes(), key=class_key)
    result = []
    for index, conjugacy_class in enumerate(subgroup_classes):
        representative = min(conjugacy_class, key=element_key)
        ambient_index = ambient_class_of[representative]
        result.append({
            "subgroup_class": index,
            **class_record(conjugacy_class, int(subgroup.order())),
            "ambient_class": ambient_index,
            "ambient_class_size": ambient_records[ambient_index]["class_size"],
            "ambient_centralizer_order": ambient_records[ambient_index]["centralizer_order"],
        })
    return result


def main() -> dict[str, object]:
    bundle = build_w33_bundle()
    ambient, point, line = bundle.group, bundle.point_stabilizer, bundle.line_stabilizer
    ambient_classes = sorted(ambient.conjugacy_classes(), key=class_key)
    ambient_records = [class_record(item, int(ambient.order())) for item in ambient_classes]
    ambient_class_of = {element: index for index, conjugacy_class in enumerate(ambient_classes) for element in conjugacy_class}

    point_fusion = fusion_table(point, ambient_classes, ambient_class_of, ambient_records)
    line_fusion = fusion_table(line, ambient_classes, ambient_class_of, ambient_records)
    point_profile = normal_27_profile(point)
    line_profile = normal_27_profile(line)
    point_multiplicity = Counter(row["ambient_class"] for row in point_fusion)
    line_multiplicity = Counter(row["ambient_class"] for row in line_fusion)
    point_ambient_support = sorted(point_multiplicity)
    line_ambient_support = sorted(line_multiplicity)

    checks = {
        "ambient_order_25920": ambient.order() == 25920,
        "ambient_has_20_classes": len(ambient_classes) == 20,
        "point_stabilizer_has_24_classes": len(point_fusion) == 24,
        "line_stabilizer_has_17_classes": len(line_fusion) == 17,
        "point_fusion_covers_all_648_elements": sum(int(row["class_size"]) for row in point_fusion) == 648,
        "line_fusion_covers_all_648_elements": sum(int(row["class_size"]) for row in line_fusion) == 648,
        "point_radical_is_extraspecial_27": point_profile["abelian"] is False and point_profile["center_order"] == 3 and point_profile["derived_order"] == 3,
        "line_radical_is_elementary_abelian_27": line_profile["abelian"] is True and line_profile["center_order"] == 27 and line_profile["derived_order"] == 1,
        "fusion_maps_are_different": point_fusion != line_fusion,
        "point_and_line_ambient_supports_are_different": point_ambient_support != line_ambient_support,
        "point_center_classes_fuse_to_two_40_classes": sum(1 for row in point_fusion if row["class_size"] == 1 and row["element_order"] == 3) == 2 and all(row["ambient_class_size"] == 40 for row in point_fusion if row["class_size"] == 1 and row["element_order"] == 3),
        "line_has_no_nontrivial_singleton_class": all(row["element_order"] == 1 for row in line_fusion if row["class_size"] == 1),
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    return {
        "schema": "w33.pass1056.two_648_class_fusions.v1",
        "status": "PASS",
        "headline": "The two order-648 stabilizers have different exact class fusions into PSp(4,3). The point/Hessian class has 24 conjugacy classes and an extraspecial normal 3^(1+2), while the line/dual class has 17 classes and an elementary-abelian normal 3^3.",
        "ambient": {"group": "PSp(4,3) ~= U4(2)", "order": int(ambient.order()), "class_count": len(ambient_classes), "classes": ambient_records},
        "point_stabilizer": {"order": int(point.order()), "class_count": len(point_fusion), "normal_27": point_profile, "ambient_support": point_ambient_support, "fusion_multiplicity": {str(k): v for k, v in sorted(point_multiplicity.items())}, "fusion": point_fusion},
        "line_stabilizer": {"order": int(line.order()), "class_count": len(line_fusion), "normal_27": line_profile, "ambient_support": line_ambient_support, "fusion_multiplicity": {str(k): v for k, v in sorted(line_multiplicity.items())}, "fusion": line_fusion},
        "check_count": len(checks),
        "checks": checks,
        "scope": "Exact permutation-group class fusion in the common degree-40 ambient action. Class numbering is local to this certificate and stabilized by representative image lists, not asserted to equal ATLAS labels.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1056_two_648_class_fusions.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "point_classes": result["point_stabilizer"]["class_count"], "line_classes": result["line_stabilizer"]["class_count"], "check_count": result["check_count"]}, indent=2))
