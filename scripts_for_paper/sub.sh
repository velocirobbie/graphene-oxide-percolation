#!/bin/bash

for i in -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
    dir=$i
    mkdir $dir
    cp sim.py raddist_nx.py $dir
    cd $dir
    python2.7 raddist_nx.py $i &
    cd ..
done

