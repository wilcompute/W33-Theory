# Part CCCCXV: Dressed Q4 Packet Logical Verifier

**Status:** verified dressed-logical obstruction for the current Q4/Bacon-Shor packet attachment.

## Result

Parts CCCCX-CCCCXIV build a native local packet route for the W33 line-star matter sector:

```text
81 line-star matter representatives
-> 81 Q4 / 4x4 Bacon-Shor packets
-> [[1296,81,4]] subsystem packet layer
-> raw line-star replacement target weight 12
```

CCCCXV checks the missing dressed subsystem question.  In the current 4x4 Bacon-Shor packet, the X-center spans even column parities.  Therefore the three-column attachment is nontrivial, but it is center-equivalent to a one-column logical representative.

```text
raw replacement weight      = 3 columns * 4 = 12
dressed subsystem weight    = 1 column  * 4 = 4
```

The generated certificate passes `12/12` checks.

## Consequence

The integrated Q4 packet layer currently proves:

```text
[[1296,81,4]]
```

It does **not** yet prove:

```text
[[1296,81,>=12]]
```

That is not a failure of the packet construction. It is the exact subsystem dressing boundary: the gauge/center freedom that makes the packet useful also allows the three-column representative to dress down to one column.

## Repair Paths

The next architecture must choose one of these explicitly:

- Add column-lock checks that forbid even-column center dressing for replacement attachments.
- Route the three base line-star edges into three independent packets before repetition or majority decoding.
- Keep the Steane/Phi6 concatenated lift as the distance-81 protection layer while Q4 packets serve as local gauge/routing hardware.

Artifacts:

- Script: `exploration/PART_CCCCXV_DRESSED_Q4_PACKET_LOGICAL_VERIFIER.py`
- Results: `PART_CCCCXV_dressed_q4_packet_logical_verifier_results.json`
- Tests: `tests/test_dressed_q4_packet_logical_verifier_ccccxv.py`
