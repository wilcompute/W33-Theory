cd /c/tmp/toe_round/stype
M='C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\N004_F1_03_S002.txt'; RHO=0.5+0.8660254037844386j
KWL=3 timeout 6000 py -3 oneloop2.py "$M" 0.8j run 8 $RHO >> runA.log 2>&1
KWL=3 timeout 6000 py -3 oneloop2.py "$M" 0.6j run 8 $RHO >> runA.log 2>&1
KWL=4 timeout 6000 py -3 oneloop2.py "$M" 0.5j run 8 $RHO >> runA.log 2>&1
KWL=4 timeout 6000 py -3 oneloop2.py "$M" 0.4j run 8 $RHO >> runA.log 2>&1
KWL=2 timeout 6000 py -3 oneloop2.py "$M" 0.1+0.9j run 8 $RHO >> runA.log 2>&1
KWL=2 timeout 6000 py -3 oneloop2.py "$M" 0.2+0.9j run 8 $RHO >> runA.log 2>&1
KWL=2 timeout 6000 py -3 oneloop2.py "$M" 0.9j run 8 $RHO >> runA.log 2>&1
echo DONE >> runA.log
