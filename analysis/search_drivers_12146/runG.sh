cd /c/tmp/toe_round/stype
M='C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt'; RHO=0.5+0.8660254037844386j
for tw in 0.52j 0.58j; do KWL=4 timeout 9000 py -3 oneloop2.py "$M" $tw run 3 $RHO >> runG.log 2>&1; done
echo DONE >> runG.log
