#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
# Author: Huang Jiahua <jhuangjiahua@gmail.com>
# License: LGPLv3+
# Last modified:

app = 'gwrite'

import os, sys
import gettext

if os.path.isdir(os.path.dirname(sys.argv[0]) + '/../build/mo'):
    gettext.install(app, os.path.dirname(sys.argv[0]) + '/../build/mo', unicode=True)
else:
    gettext.install(app, unicode=True)

if __name__=="__main__":
	print _('')



