reset
load 'colors.gnuplot'
# set terminal postscript eps enhanced solid "Helvetica" 20
set terminal pdfcairo enhanced font "Helvetica,18"
# set terminal pdf enhanced dashed
# set termoption linewidth 3 font "Helvetica, 14" 
set datafile separator ","
set lmargin 8
set rmargin 2

ptpbound(x) = real(system(sprintf("./p2p_bound.py %f", x)))
lower_bound(x) = real(system(sprintf("./lower_bound.py %f", x)))
upper_bound(x) = real(system(sprintf("./upper_bound.py %f", x)))
seed_turbo_average(x) = real(system(sprintf("cat %s | python perc_interval.py /dev/stdin seed_pos turbo_time | awk -F ',' 'BEGIN{sum=0;n=0}{sum+=$2;n+=1}END{print sum/n;}'", x)))
