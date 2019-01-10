all: trendnet_teg30284_fw.py

%.py: %.ksy
	kaitai-struct-compiler -t python $<

clean:
	rm -f trendnet_teg30284_fw.py

.PHONY: all clean
