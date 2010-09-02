#! /bin/bash

# Installing C module
chmod +x lib/setup
gksudo "./lib/setup install"

# Installing PyPlanets and Py3De.py on /use/bin
# Run it using: $ PyPlanets
chmod +x lib/PyPlanets
gksudo "cp lib/PyPlanets /usr/bin/PyPlanets -u"
gksudo "cp lib/Py3De.py /usr/bin/Py3De.py -u"
gksudo "chmod +x /usr/bin/PyPlanets"
gksudo "chmod +x /usr/bin/Py3De.py"
