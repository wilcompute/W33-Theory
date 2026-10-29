"""Exact divisibility checks; simplicity is a cited group theorem, not verified here."""
from analysis.w33_20261029_conwell_w33_equivariance_nogo import certificate
def test_eight_label_obstruction():
    c=certificate()
    assert c["PSp4_3_order"]==25920
    assert c["PGSp4_3_order"]==51840
    assert c["A8_order"]==20160 and c["S8_order"]==40320
    assert c["PSp4_3_cannot_embed_S8"]
    assert c["A8_cannot_embed_PGSp4_3"]
    assert c["any_W33_full_group_8_label_permutation_image_order_at_most"]==2
    assert c["surjective_full_W33_equivariant_map_40_points_to_28_pairs_with_natural_A8_action"] is False
