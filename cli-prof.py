#!/usr/bin/env python
import sys
import cProfile
from iphoto.cli import main

cProfile.run('main()')
