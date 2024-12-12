
parser.py: python.gram
	python3 -m pegen python.gram -o parser.py
	sed -i 's/python3.8/python3/' parser.py
	chmod a+rx parser.py
