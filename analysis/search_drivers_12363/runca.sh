export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12363
cp $D/Geometry_Z6-II_win_*.txt $HOME/orb/nsobuild/Geometry/
cd ~/orb/nsoverb
K=6
for k in $(seq 0 $((K-1))); do
  ( awk -v k=$k -v K=$K 'NR%K==k' $D/ca_list.txt | while read -r f; do
      [ -n "$f" ] || continue
      [ -s "$D/$f.verbose" ] && grep -q T_NFIELDS "$D/$f.verbose" && continue
      timeout 1800 ./nsodump_verbose $D/$f.txt > $D/$f.verbose 2>&1
    done ) &
done
wait; echo finished
