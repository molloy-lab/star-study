#!/bin/bash

python3 write_table_error.py &> table-startle-sim-tree-error.tex

python3 write_table_accuracy_and_runtime.py &> table-startle-sim-tree-accuracy-and-runtime.tex