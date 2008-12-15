#! /usr/bin/python
import pstats

p = pstats.Stats('/tmp/profiler.data')

print "********************* Get top 20 longest methods ************************* \n"

# to check what is taking lots of time
p.sort_stats('time').print_stats(20)

print "************************************************************************** \n"
print "************************************************************************** \n"

print "********************* Complete Stats ************************* \n"

# Total stats
p.strip_dirs().sort_stats(-1).print_stats()



