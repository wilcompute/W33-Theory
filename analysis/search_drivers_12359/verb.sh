export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
cd ~/orb/nsoverb
for s in 2 3 1; do cp /mnt/c/tmp/toe_wt/analysis/search_drivers_12359/Geometry_Z6-II_sub$s.txt Geometry/; done
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12359
for f in "$@"; do timeout 1800 ./nsodump_verbose $D/$f.txt > $D/$f.verbose 2>&1; echo "$f $?"; done
