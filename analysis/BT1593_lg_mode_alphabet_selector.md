# BT1593 LG Mode Alphabet Selector

BT1593 chooses a concrete nine-mode recenter alphabet: `sector_id=3*x+z`, `ell=sector_id-4`, and `p=(x+2*z) mod 3`. The OAM charges are symmetric `-4..4`, each radial shell appears three times, and the existing 24-word centered selector gives `216` exact finite addresses through `address=sector_id*24+word_index`.
