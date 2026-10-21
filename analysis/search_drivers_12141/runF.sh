cd /c/tmp/toe_round/stype
M='C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt'; RHO=0.5+0.8660254037844386j
P='C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3\N008_F1_04_S037_T115.txt'
KWL=2 timeout 6000 py -3 oneloop2.py "$M" -0.1+0.9j run 8 $RHO >> runF.log 2>&1
timeout 9000 py -3 oneloop3.py "$P" 1.75j,2j,2j run 8 >> runF.log 2>&1
timeout 9000 py -3 oneloop3.py "$P" 2j,2j,1.75j run 8 >> runF.log 2>&1
timeout 9000 py -3 oneloop3.py "$P" 0.2+1.75j,0.2+1.75j,0.2+1.75j run 8 >> runF.log 2>&1
echo DONE >> runF.log
