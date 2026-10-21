cd /c/tmp/toe_round/stype
M='C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt'; RHO=0.5+0.8660254037844386j
for tw in 0.55j 0.1+0.55j 0.3+0.55j 0.5+0.55j; do KWL=4 timeout 6000 py -3 oneloop2.py "$M" $tw run 8 $RHO >> runC.log 2>&1; done
echo DONE >> runC.log
