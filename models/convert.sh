#!/bin/bash

for i in $(find . -name "*.dae"); 
do 
    name="$(echo ${i} | cut -d '/' -f 3)";
    dae2egg $i $(echo ${i} | sed 's/dae/egg/g');
done

mogrify $(find . -name "*.png")
