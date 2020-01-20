python -m debugger trace -f binary_search tests/search.py
python -m debugger view -n tests/search.py.json > tests/binary_search.txt

python -m debugger trace -f depth_first_search tests/search.py
python -m debugger view -n tests/search.py.json > tests/depth_first_search.txt

python -m debugger trace -f breadth_first_search tests/search.py
python -m debugger view -n tests/search.py.json > tests/breadth_first_search.txt

rm tests/search.py.json

python -m debugger trace -f unbounded_knapsack tests/knapsack.py
python -m debugger view -n tests/knapsack.py.json > tests/unbounded_knapsack.txt

python -m debugger trace -f knapsack tests/knapsack.py
python -m debugger view -n tests/knapsack.py.json > tests/knapsack.txt

rm tests/knapsack.py.json
