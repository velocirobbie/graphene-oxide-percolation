# Graphene Oxide Percolation Analysis

Generate the simplest simulation with:
```
python2.7 command.py
```
`command.py` simply runs one simulation and prints a summary of the simulation, for eample:
```
Coverage   = 0.7224
Nsites     = 5
Max radius = 0.431
Corrected coverage = 0.72095
Error      = 0.00145
```
The coverage is the fraction of the squre covered by islands when a path was made from one edge to its oposite. The corrected coverage is the half way between the coverage above and the coverage on the previous step; the error is half the difference between these values.

Nsites is the number of islands, Max radius is the size of the largers island.

Two files are also written: `nodes.dat` and `path.dat`. These record respectively the location and size of the islands, and the shortest path from one edge to its opposite. These can be visually inspected using gnuplot with:
```
gnuplot> set size square; set xr [0:1]; set yr [0:1]
gnuplot> pl 'nodes.dat' w circ, 'path.dat' w l
```