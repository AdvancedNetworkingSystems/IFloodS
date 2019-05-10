load 'generic.gnuplot'

bound_mean(x) = real(system(sprintf("./upper_bound.py %f", x))) + 0.5
bound_peak(x) = real(system(sprintf("./upper_bound.py %f", x))) + 1 

set termoption lw 3
set boxwidth 0.1 

set style fill solid

set key over
set xrange[0.5:3.5]

set ylabel "{/Symbol @^{/=35-}D} (cycles)" font ", 18" offset 1.0,0
set xlabel "Graph ID"

set xtics (1,2,3)
set output 'ifloods_mean_aoi.pdf'
plot "< cat ../ifloods_aoi.data |awk '/strategy|plain/{print}' | python perc_interval.py /dev/stdin graph mean_aoi"\
	using ($0-0.15):3:2:6:5  lc rgb C3 with candlesticks title '{/Symbol @^{/=35-}D}, SE_f' whiskerbars,\
	"< cat ../ifloods_aoi.data |awk '/strategy|turbo/{print}' | python perc_interval.py /dev/stdin graph mean_aoi"\
	using ($0+0.15):3:2:6:5  lc rgb C4 with candlesticks title '{/Symbol @^{/=35-}D}, RE_f' whiskerbars,\
	bound_mean(x) with lines lc rgb C1 title "{/Symbol g}"

unset xtics
set xtics 
set terminal pdfcairo enhanced font "Helvetica,10" size 5,1.5

set lmargin 3
set rmargin 1

set tics scale 0

set xrange[0:51]
set termoption lw 1
set boxwidth 0.25

set style fill solid
unset ylabel
 
#set ylabel "Mean AoI (cycles)" font ", 12" offset 1.0,0
set xlabel "Sender"
set output 'ifloods_mean_aoi_senders.pdf'
plot "< python3 aoi_preproc.py sender mean_aoi"\
	using ($0-0.25):4:3:7:6 lc rgb C3 with candlesticks title '{/Symbol @^{/=20-}D}, SE_f' whiskerbars,\
	"" using ($0+0.25):9:8:12:11 lc rgb C4 with candlesticks title '{/Symbol @^{/=20-}D}, RE_f' whiskerbars,\
	bound_mean(100) with lines lc rgb C1 title "{/Symbol g} "

set xlabel "Receiver"
set output 'ifloods_mean_aoi_receivers.pdf'
plot "< python3 aoi_preproc.py receiver mean_aoi"\
	using ($0-0.25):4:3:7:6 lc rgb C3 with candlesticks title '{/Symbol @^{/=20-}D}, SE_f' whiskerbars,\
	"" using ($0+0.25):9:8:12:11 lc rgb C4 with candlesticks title '{/Symbol @^{/=20-}D}, RE_f' whiskerbars,\
	bound_mean(100) with lines lc rgb C1 title "{/Symbol g}"

#set ylabel "Mean Peak AoI (cycles)" font ", 12" offset 1.0,0

set xlabel "Sender"
set output 'ifloods_mean_peak_aoi_senders.pdf'
plot "< python3 aoi_preproc.py sender mean_peak_aoi"\
	using ($0-0.25):4:3:7:6 lc rgb C2 with candlesticks title 'Mean peak AoI, plain' whiskerbars,\
	"" using ($0+0.25):9:8:12:11 lc rgb C1 with candlesticks title 'Mean peak AoI, turbo' whiskerbars,\
	bound_peak(100) with lines lc rgb C4 title "AoI stochastic bound"

set xlabel "Receiver"
set output 'ifloods_mean_peak_aoi_receivers.pdf'
plot "< python3 aoi_preproc.py receiver mean_peak_aoi"\
	using ($0-0.25):4:3:7:6 lc rgb C2 with candlesticks title 'Mean peak AoI, plain' whiskerbars,\
	"" using ($0+0.25):9:8:12:11 lc rgb C1 with candlesticks title 'Mean peak AoI, turbo' whiskerbars,\
	bound_peak(100) with lines lc rgb C4 title "AoI stochastic bound"
