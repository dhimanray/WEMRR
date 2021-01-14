#!/bin/bash

for i in {0..12}
do
	cd milestone_$i
	rm -r ANALYSIS
	rm mfpt* log.log
	python analysis.py 
	cd ..
done
