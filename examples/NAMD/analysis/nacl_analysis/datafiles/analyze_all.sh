#!/bin/bash

for i in {0..5}
do
	cd milestone_$i
	rm -r ANALYSIS
	python analysis.py 
	cd ..
done
