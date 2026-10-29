export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12363
cp $D/Geometry_Z6-II_sub2w*.txt $HOME/orb/nsobuild/Geometry/
for f in "$@"; do
  cd ~/orb/nsostrict; s=$(timeout 300 ./nsocheck_strict $D/$f.txt | grep ^FILE | awk '{print $4}')
  timeout 1800 ./nsoq_strict $D/$f.txt > $D/$f.nsoq 2>&1; e1=$?
  cd ~/orb/nsoverb; timeout 1800 ./nsodump_verbose $D/$f.txt > $D/$f.verbose 2>&1
  echo "$f check=$s rc=$e1 fields=$(grep -c ^FIELD $D/$f.nsoq) $(grep T_NFIELDS $D/$f.verbose)"
done
