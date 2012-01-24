.PHONY: install uninstall clean dir

install: dir
	./package.py bpg.py > tmp.py
	sudo mv tmp.py /usr/bin/bpg
	sudo chmod a+x /usr/bin/bpg

clean:
	-rm tmp.py
	-rm *.pyc
	-rm *.pyo

uninstall:
	-sudo rm /usr/bin/bpg
	-rm -rf ~/.bpg

dir: uninstall
	cp -r .bpg ~/.bpg
