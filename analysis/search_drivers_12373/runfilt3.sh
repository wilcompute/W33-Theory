cd /mnt/c/tmp/toe_wt/analysis/search_drivers_12373
for k in 0 1 2 3 4 5; do SCAN_PFX=scan3_ python3 filt.py $k 6 > filt2_$k.log 2>&1 & done
wait; echo FILT3DONE
