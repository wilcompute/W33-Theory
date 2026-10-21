cd /c/tmp/toe_round/stype
M='C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt'; RHO=0.5+0.8660254037844386j
KWL=4 timeout 6000 py -3 oneloop2.py "$M" 0.05+0.55j run 6 $RHO >> runE.log 2>&1
echo DONE >> runE.log
