# 12359: run the strict non-SUSY engine on SM_2913_v6 over the parent geometry, the regenerated parent (s=1, control) and the
# sub-orbifolds s=2 (theta^2, e5e6 fixed) and s=3 (theta^3, e3e4 fixed).
mkdir -p $HOME/orb/libfix && ln -sf $HOME/orb/sysroot/usr/lib/x86_64-linux-gnu/libgsl.so.27 $HOME/orb/libfix/libgsl.so.0
export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12359
for s in 1 2 3 2bad; do cp $D/Geometry_Z6-II_sub$s.txt $HOME/orb/nsobuild/Geometry/; done
cd ~/orb/nsostrict
for f in "$@"; do
  o="$D/${f%.txt}.nsoq"
  s=$(timeout 300 ./nsocheck_strict "$D/$f" | grep ^FILE | awk '{print $4}')
  echo "$f check=$s"
  if [ "$s" = "1" ]; then timeout 3000 ./nsoq_strict "$D/$f" > "$o" 2>&1; echo "$f done $(grep -c ^FIELD $o) fields"; fi
done
