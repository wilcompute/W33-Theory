cd /mnt/c/tmp/toe_wt/analysis/search_drivers_12373
for k in 0 1 2 3 4 5; do WANT_ALL=1 python3 newv0.py $k 6 240 > worker2_$k.log 2>&1 & done
wait; echo ALLDONE2
