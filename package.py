#!/usr/bin/python
import sys
import re
import os

imports = []

def output(filename, toplevel=False):
   f = open(filename, 'r')
   waitForUnindented = False
   for line in f:
      m = re.match('^\s|#', line)
      if m and waitForUnindented:
         continue
      elif not m:
         waitForUnindented = False

      m = re.match('^def main', line)
      n = re.match('^if\s*__name__\s*==', line)
      if (m or n) and not toplevel:
         waitForUnindented = True
         continue

      m = re.match('from (\w*) import \*.*', line)
      if m and os.path.exists(m.group(1) + ".py"):
         output(m.group(1) + ".py")
         continue

      m = re.match('^#!', line)
      if m and not toplevel:
         continue

      sys.stdout.write(line)



def main():
   if len(sys.argv) > 1:
      output(sys.argv[1], True)
   else:
      print "provide file to package as first argument"

if __name__ == '__main__':
   main()
