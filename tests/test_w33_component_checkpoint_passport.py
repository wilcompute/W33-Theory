#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_component_async36 as component  # noqa: E402
import w33_zero_copy_merkle36 as zerocopy  # noqa: E402
import w33_checkpoint_migration as migration  # noqa: E402
import w33_execution_passport as passport  # noqa: E402
import w33_causal_time_ledger as timeledger  # noqa: E402
import w33_magic_resource_scheduler as magic  # noqa: E402


class W33ComponentEngineeringTests(unittest.TestCase):
    def test_async_component_boundary_turns_backpressure_into_future(self):
        p = component.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["second_send_waits_on_backpressure"])
        self.assertTrue(p["checks"]["pump_wakes_pending_send"])
        self.assertTrue(p["checks"]["private_interface_type_rejected"])

    def test_merkle_subtree_delegation_is_zero_blob_and_snapshot_stable(self):
        p = zerocopy.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["publish_allocates_zero_blobs"])
        self.assertTrue(p["checks"]["delegation_allocates_zero_blobs"])
        self.assertTrue(p["checks"]["published_snapshot_is_immutable"])

    def test_full_migration_and_cross_carrier_continuation_are_not_conflated(self):
        p = migration.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["cross_carrier_full_restore_rejected"])
        self.assertTrue(p["checks"]["neutral_continuation_preserves_classical_guest"])
        self.assertTrue(p["checks"]["trace_lineage_restarts"])

    def test_execution_passport_is_fail_closed_across_stack(self):
        p = passport.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["valid_packet_admitted"])
        self.assertTrue(p["checks"]["magic_overdraft_refused"])
        self.assertTrue(p["checks"]["equal_order_namespace_alias_refused"])

    def test_causal_time_distinguishes_state_revisit_from_history_depth(self):
        p = timeledger.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["same_semantic_state_can_have_later_time"])
        self.assertTrue(p["checks"]["branches_are_incomparable"])
        self.assertTrue(p["checks"]["discard_history_is_irreversible_cut"])

    def test_magic_is_reserved_resource_not_boolean_capability(self):
        p = magic.verify()
        self.assertEqual(p["status"], "PASS")
        self.assertTrue(p["checks"]["inventory_cannot_be_overbooked"])
        self.assertTrue(p["checks"]["ft_candidate_is_fail_closed_without_w33_adapter"])
        self.assertTrue(p["checks"]["token_double_spend_blocked"])


if __name__ == "__main__":
    unittest.main()
