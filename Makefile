
WHY := why\ a\ 701\ hashtable\ is\ bad.png
OCC := distribution\ of\ hashes\ for\ English\ words.png
all: $(WHY) $(OCC)
.PHONY: all clean

$(WHY) $(OCC): histogram.csv
	./birthday.py

histogram.csv: words.txt test_hashing
	./test_hashing > histogram.csv

test_hashing: test_hashing.cc
	$(CXX) -o test_hashing test_hashing.cc

words.txt:
	wget https://raw.githubusercontent.com/dwyl/english-words/master/words.txt

clean:
	rm $(WHY) $(OCC) test_hashing words.txt histogram.csv
