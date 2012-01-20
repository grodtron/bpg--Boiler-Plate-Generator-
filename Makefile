.PHONY: install clean dir

install: dir
	sudo cp bpg.py /usr/bin/bpg
	sudo chmod a+x /usr/bin/bpg

clean:
	sudo rm /usr/bin/bpg
	rm -rf ~/.bpg

dir: clean
	cp -r .bpg ~/.bpg
