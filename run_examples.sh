python -m debugger trace examples/sort.py -bs 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/simple-bubble.txt

python -m debugger trace examples/sort.py -b 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/bubble.txt

python -m debugger trace examples/sort.py -m 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/merge.txt

python -m debugger trace examples/sort.py -is 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/simple-insertion.txt

python -m debugger trace examples/sort.py -i 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/insertion.txt

python -m debugger trace examples/sort.py -sh 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/shell.txt

python -m debugger trace examples/sort.py -se 4 3 2 1 0
python -m debugger view -n examples/sort.py.json > examples/selection.txt

rm examples/sort.py.json
