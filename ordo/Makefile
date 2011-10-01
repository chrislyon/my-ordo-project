:set noexpandtab

PROG=agent.py
ts=$(shell date "+%Y%m%d_%X")
long_ts=$(shell date "+%x %X")

.PHONY: run
run: clean
	twistd -y $(PROG)

.PHONY: clean
clean:
	rm -f twistd.log twistd.pid
	find . -name '*.pyc' -exec rm {} \;


.PHONY: lint
lint:
	pylint $(PROG)

.PHONY: kill
kill:
	kill `cat twistd.pid`

.PHONY: sav
sav:
	echo sav/$(ts)_$(PROG)
	cp $(PROG) sav/$(ts)_$(PROG)

.PHONY: status
status: clean
	find . -print -exec svn add {} \;
	svn status

.PHONY: commit
commit: clean
	svn commit -m "Modif du $(long_ts)"


