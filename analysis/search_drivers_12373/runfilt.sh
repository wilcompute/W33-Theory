cd /mnt/c/tmp/toe_wt/analysis/search_drivers_12373
for k in 0 1 2 3 4 5; do python3 filt.py $k 6 > filt_$k.log 2>&1 & done
wait; echo FILTDONE
