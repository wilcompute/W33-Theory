MSYS_NO_PATHCONV=1 wsl -e bash /mnt/c/tmp/toe_wt/analysis/search_drivers_12373/spec3.sh
py -3 vet3.py > vet3.log 2>&1
py -3 vet_pairs3.py > vet_pairs3.log 2>&1
py -3 vet_loose3.py > vet_loose3.log 2>&1
echo PIPE3DONE
