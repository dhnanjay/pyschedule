#! /usr/bin/env python
from pyschedule import *

# Taillards 20x5 flow-shop instance downloaded from
# http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/flowshop.dir/tai20_5.txt
# columns = jobs, rows = machines
proc ='\
54 83 15 71 77 36 53 38 27 87 76 91 14 29 12 77 32 87 68 94\n\
79  3 11 99 56 70 99 60  5 56  3 61 73 75 47 14 21 86  5 77\n\
16 89 49 15 89 45 60 23 57 64  7  1 63 41 63 47 26 75 77 40\n\
66 58 31 68 78 91 13 59 49 85 85  9 39 41 56 40 54 77 51 31\n\
58 56 20 85 53 35 53 41 69 13 86 72  8 49 47 87 58 18 68 28'

proc_table = [ [ int(x) for x in row.replace('  ',' ').strip().split(' ') ] for row in proc.split('\n') ]
n = len(proc_table[0])
m = len(proc_table)
#n = 6

S = Scenario('Taillards Flow-Shop 15x15')
T = { (i,j) : S.Task((i,j),length=proc_table[j][i]) for i in range(n) for j in range(m) }
R = { j : S.Resource(j) for j in range(m) }

S += [ T[(i,j)] < T[(i,j+1)] for i in range(n) for j in range(m-1) ]
for i in range(n) :
	for j in range(m) :
		T[(i,j)] += R[j]

solvers.pulp().solve(S,kind='CPLEX',msg=1,lp_filename=None)
plotters.gantt_matplotlib().plot(S,resource_height=100.0,show_task_labels=False,color_prec_groups=True)
