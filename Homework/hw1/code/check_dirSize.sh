#!/bin/bash
cd ../../../../
du moreheadowen-am129-fall2020 | sort -g -r | head -n 3 > dirSizes.txt
cat dirSizes.txt

