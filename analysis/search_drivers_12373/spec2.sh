export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12373; mkdir -p $D/spec
cd ~/orb/nsostrict
K=6
for k in $(seq 0 $((K-1))); do
  ( awk -v k=$k -v K=$K 'NR%K==k' $D/large_safe2.txt | while read -r b; do
      cp $HOME/orb/newv0/$b.txt $D/spec/$b.txt
      [ -s $D/spec/$b.nsoq ] && tail -1 $D/spec/$b.nsoq | grep -q END && continue
      timeout 1800 ./nsoq_strict $D/spec/$b.txt > $D/spec/$b.nsoq 2>&1
    done ) &
done
wait; echo SPECDONE
