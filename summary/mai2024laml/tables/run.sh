#!/bin/bash

python3 write_table_error.py &> table-laml-sim-tree-error.tex

python3 write_table_accuracy_and_runtime.py &> table-laml-sim-tree-accuracy-and-runtime.tex