# BT1898 — Single-Photon Holonet Demonstrator Runbook

BT1898 turns BT1895 into an experimental runbook for the unencoded single-photon demonstrator.

## Goal

Test the finite Holonet logic without confusing the demonstrator with the GKP(D4) fault-tolerant machine.

```text
single photon = demonstrator
GKP(D4) o Steinberg = fault-tolerant machine
```

## Components

```text
heralded single-photon source
polarizing beam splitter
symmetric 3-port tritter
0/tau/2tau delay ladder
bin-synchronous electro-optic modulator
polarization rotator at arccos(-2/3)
single-photon detectors
classical controller for Witting frame schedule
```

## Run sequence

```text
1. calibrate source, dark counts, and loss baselines
2. calibrate tritter and phase settings
3. load the 40-Witting-tetrad analyzer schedule
4. run the 640 basis-local admission records
5. tag 160 diagonal contextual witness apertures
6. tag 480 off-diagonal data handshakes
7. run the 72-tick transaction body per accepted frame
8. compute witness metrics and pass/fail status
```

## Raw data columns

```text
shot_id
witting_tetrad
alice_slot
bob_slot
logical_pair_type
transaction_tick
time_bin
detector_id
polarization_setting
tritter_phase_setting
modulator_phase
click_pattern
dark_reference
loss_probe
accepted_flag
witness_class
```

## Primary witnesses

```text
contextual fraction target = 1/10
pump Chern target          = 2
accepted logical rate      = 13/40
physical frame split       = 160 diagonal witness records + 480 off-diagonal data records
```

## Pass/fail criteria

```text
schedule integrity: all 640 physical frame records attempted with correct tetrad/slot labels
admission integrity: accepted logical count matches 520/1600 within declared shot-noise interval
contextuality: corrected contextual-fraction estimate compatible with 1/10
topological pump: Chern readout compatible with 2 under the chosen protocol
guarding: dark-reference and loss-probe estimates reported separately
```

## Outputs

```text
raw shot table
calibration summary
witness summary JSON
pass/fail report
commit hash and run manifest
```

Boundary: runbook for the unencoded single-photon demonstrator only; not a GKP fault-tolerant build plan or hardware threshold claim.
