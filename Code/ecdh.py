#! /usr/bin/env python
# -*- coding: utf8 -*-

import copy
import math
import random

# checks if we are running from a s60 phone and modifies include path
import os
import sys
import time

if os.name == 'e32':
  sys.path.append('e:\ecc4pys60')
  
import ec
  
# $Id$
__version__   = "$Revision$"
__author__    = "Alexandre Coster"
__contact__   = "acoster at inf dot ufrgs dot br"
__copyright__ = "Copyright (C) 2008 by  Alexandre Coster"

