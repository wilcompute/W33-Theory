# 12459: 6D massless spectra (both fixed tori, Wilson lines on the fixed torus off) for all 52 SM_2541 models; usage: bash run6d.sh WORKER NW
export LD_LIBRARY_PATH=$HOME/orb/libfix:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu
D=/mnt/c/tmp/toe_wt/analysis/search_drivers_12459; mkdir -p $D/s6d; cd ~/orb/nsostrict; n=0
while read b; do
  if [ $((n % $2)) -eq $1 ]; then
    for t in t3 t2; do o=$D/s6d/${b}__$t.nsoq; [ -s $o ] || timeout 3000 ./nsoq_strict $HOME/orb/newv0/${b}__$t.txt > $o 2>&1; done
    echo "$b done"
  fi; n=$((n+1))
done < $D/bases52.txt
