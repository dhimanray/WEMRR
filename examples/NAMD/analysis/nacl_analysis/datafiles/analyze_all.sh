#!/bin/bash

for i in {0..6}
do
	cd milestone_$i
	rm -r ANALYSIS
	python analysis.py 
	cd ..
done
