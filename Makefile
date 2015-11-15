.PHONY: crlibm crlibm-notest msys2 clean docs test

crlibm: crlibm/crlibm_config.h
	$(MAKE) -C crlibm check install

crlibm-notest: crlibm/crlibm_config.h
	$(MAKE) -C crlibm SUBDIRS="scs_lib ." install

# Peculiarities:
# * Pretend that msys2 is a BSD-type OS.
# * Configure needs a working stdin, which is normally hijacked by appevyor.
# * Ensure SSE2 are enabled also on 32bit builds.
# * Requires the PYTHON_DLL variable set to the full path of the Python DLL
msys2: PYTHON_NAME := $(basename $(notdir $(PYTHON_DLL)))
msys2:
	(cd crlibm; exec 0</dev/null; CFLAGS='-DCRLIBM_TYPEOS_BSD' ./configure --prefix=$(abspath build/crlibm) --enable-sse2)
	exec 0</dev/null; $(MAKE) crlibm-notest
	gendef $(PYTHON_DLL)
	dlltool --dllname $(PYTHON_DLL) --def $(PYTHON_NAME).def --output-lib build/crlibm/lib/$(PYTHON_NAME).a

clean:
	-rm -rf build/ dist/ crlibm.egg-info/ crlibm.so
	$(MAKE) -C crlibm distclean

crlibm/crlibm_config.h:
	(cd crlibm; CFLAGS='-fPIC' ./configure --prefix=$(abspath build/crlibm))

docs: build/DESCRIPTION.html build/README.html

build/DESCRIPTION.html: README.rst setup.py
	./setup.py --long-description | rst2html.py > $@

build/README.html: README.rst
	rest2html < $< > $@

test:
	./setup.py test -q
