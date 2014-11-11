# -*- coding: utf-8 -*-
__author__ = 'wachs'

import subprocess as s
import os
import re

path = "/Users/wachs/temp/troco.c"
path_output = "/Users/wachs/temp/troco"

sub = s.Popen("gcc %s -o %s" % (path, path_output), shell=True, stdout=s.PIPE, stderr=s.PIPE)
(out, err) = sub.communicate()

print "output"
# print out

#print err

print "err"
n = 1
err2 = []

lines = err.split("\n")
ret = []

while len(lines) > 2:
    l = lines.pop(0) + "\n"
    while lines[0][0] != '/' and len(lines) > 2:
        l += lines.pop(0) + "\n"
    ret.append(l)
print ret

print [l for l in ret if (" error:" in (l.split("\n"))[0])]

folder = "/Users/wachs/temp/"

with open(folder + "troco.c") as f:
    text = f.read()



print text.replace(rep, "\nobaoba\n")