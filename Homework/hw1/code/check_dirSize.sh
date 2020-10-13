#!/bin/bash

#First, go to directory that stores my local am129 directory
#Then use du on this directory, sort the contents by size in decreasing order
#store the 3 largest entries to dirSizes.txt, and output the entire list to screen


cd ../../../../
du moreheadowen-am129-fall2020 | sort -g -r | head -n 3 > dirSizes.txt
du moreheadowen-am129-fall2020 | sort -g -r

