set terminal postscript eps enhanced color font 'Helvetica,14'

set output  "resultsISE.eps" 
set xlabel "Time"
set ylabel "Integrated Squared Error (ISE)"
set grid ytics
set grid xtics
plot "~/.uwsim/benchmark-pathFollowing.data" using 1:2 title "" with linespoint lw 3

set output  "resultsError.eps" 
set xlabel "Time"
set ylabel "Distance to path"
set grid ytics
set grid xtics
plot "~/.uwsim/benchmark-pathFollowing.data" using 1:3 title "" with linespoint lw 3
