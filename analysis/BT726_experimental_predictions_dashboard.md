# BT726 Experimental Predictions Dashboard

This is a repository-facing falsifier dashboard scaffold.  It intentionally separates repository claims from external experimental status.

## Dashboard policy

External status must be refreshed before any public-facing claim.  The dashboard stores:

- prediction ID,
- sector,
- observable,
- exact W33 prediction,
- numerical value where applicable,
- repository status,
- external-refresh status.

## Initial tracked predictions

| ID | Sector | Observable | Prediction | Status |
|---|---:|---|---|---|
| F1 | electroweak | weak mixing angle | sin^2(theta_W)=3/13 | refresh external status |
| F2 | QCD | strong coupling | alpha_s(mZ)=20/169 | refresh external status |
| F18 | cosmology | dark energy fraction | Omega_Lambda=9/13 | refresh external status |
| F36 | dark energy | equation of state | w0=-19/27, wa=-1/180 | near-term test |
| F37 | quantum gravity | black holes | no sub-Planck black holes | active falsifier |
| F39 | analogue gravity | Hawking spectrum | 30 percent non-thermality | active falsifier |
| TQCD | QCD | strong CP | theta_QCD=0 | precision-bound refresh |
| H39 | hierarchy | mass hierarchy | mEW/mPl=exp(-39) | convention review |

## Data artifact

The machine-readable dashboard is:

```text
 data/PART_BT726_EXPERIMENTAL_PREDICTIONS_DASHBOARD.json
```

## Boundary

This dashboard is not an experimental review by itself.  It is the infrastructure needed to make W33 falsifiers attackable and refreshable.
