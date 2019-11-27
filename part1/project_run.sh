#!/bin/bash
# file: foo.sh

python student_course.py -C 520 -S 100 -K 4 -dist piecewise
python student_course.py -C 520 -S 100 -K 4 -dist skewed
python student_course.py -C 520 -S 100 -K 4 -dist uniform
python student_course.py -C 520 -S 100 -K 4 -dist 4tier
