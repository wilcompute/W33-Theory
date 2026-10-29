export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
cd ~/orb/nsoverb
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12359
K=6
for k in $(seq 0 $((K-1))); do
  ( awk -v k=$k -v K=$K 'NR%K==k' $D/c6d_list.txt | while read -r f; do
      [ -n "$f" ] || continue
      o="$D/${f%.txt}.verbose"
      [ -s "$o" ] && grep -q T_NFIELDS "$o" && continue
      timeout 1800 ./nsodump_verbose $D/$f > "$o" 2>&1
    done ) &
done
wait
echo finished
