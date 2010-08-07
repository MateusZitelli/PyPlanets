#! /bin/bash

# Installing C module
chmod +x lib/setup
gksudo "./lib/setup install"

# Installing PyPlanets on /use/bin
# Run it using: $ PyPlanets
chmod +x lib/PyPlanets
gksudo "cp lib/PyPlanets /usr/bin/PyPlanets -u"
gksudo "chmod +x /usr/bin/PyPlanets"
