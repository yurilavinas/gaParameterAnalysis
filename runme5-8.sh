# # random set.seed
# RANDOM=1341
# # create middle gen
# nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF5.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
# nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF6.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' & 
# nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF7.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
# nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF8.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
# wait
# # random set.seed
# RANDOM=1342
# # k loop
# for i in {2..25} 
# do
# 	# repetition loop
# 	for j in {0..40} 
# 	do
		nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF5.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
		nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF6.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
		nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF7.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
		nohup python2.7 benchmarks-pseudo-adaptative/benchmarks-gamodelF8.py -params 'benchmarks-pseudo-adaptative/gaParams.txt' &
# 		wait
# 	done
# done