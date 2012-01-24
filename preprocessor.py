#!/usr/bin/python

import re
from datetime import datetime

# A small class that describes a file to be created by BPG
class OutputFile:
   # temporary executables are files that 
   # will be created, run and then deleted
   TEMPORARY_EXECUTABLE  = 'temporary'
   # normal files will be created and then left there
   NORMAL                = 'normal'

   def __init__(self, name, ftype):
      self.name = name
      self.data = ""
      self.type = ftype

   # add a line of test to this file object
   def addLine(self, line):
      self.data += line
      if line[-1] != '\n':
         self.data += '\n'

   def __str__(self):
      return (self.name if self.name else "<No Name>") + '\n' + '\n'.join('~\t' + l for l in self.data.splitlines())

# This class reads a bpg template file and performs the processing that turns it into a list of
# OutputFiles
class TemplateReader:
   def __init__(self, templateFileName=None):

      # Dictionary of template vars - filled through a combination of a config file
      # and vars being set within the template file itself
      self.variables = {}

      # built in preprocessor functions
      self.functions = {
         "strftime" : lambda x: datetime.now().strftime(x)
      }

      self.files = []
      self.currentFile = None

      if templateFileName:
         self.parseTemplate(templateFileName)


   def loadVariables(self, variableDict, overwrite=True):
      for key in variableDict:
         if (self.variables.has_key(key) and overwrite) or not self.variables.has_key(key):
            self.variables[key] = variableDict[key]

   def parseTemplate(self, templateFileName):
      self.templateFile = open(templateFileName, 'r')
      self._parse()

   def __iter__(self):
      return iter(self.files)

   def enterFile(self, name, ftype=OutputFile.NORMAL):
      self.currentFile = OutputFile(name, ftype) 
      self.files.append(self.currentFile)
      self.inFile = True
   def exitFile(self):
      self.currentFile = None
      self.inFile = False

   def enterBlock(self):
      self.inBlock = True
   def exitBlock(self):
      self.inBlock = False

   def _parse(self):
      self.instructions = []
      self.inBlock = False
      for line in self.templateFile:
         m = re.match("^== begin block ==$", line)
         if m:
            self.enterBlock()
            continue

         m = re.match("^== end block ==$", line)
         if m:
            self.exitBlock()
            continue

         m = re.match("^== begin file (\w+) ==$", line)
         if m:
            self.enterFile(m.group(1))
            continue

         m = re.match("^== end file ==$", line)
         if m:
            inFile = False
            continue

         m = re.match("^== begin instructions ==$", line)
         if m:
            self.enterFile(None, OutputFile.TEMPORARY_EXECUTABLE)
            continue

         m = re.match("^== end instructions ==$", line)
         if m:
            self.exitFile()
            continue

         if self.inBlock:
            self._doInstruction(line)
            continue
         if self.inFile:
            self.currentFile.addLine(self._preprocess(line))
            continue

   # Instructions to be executed when within a block

   def _doInstruction(self, instruction):
      patterns = (
         ('^(\w+)\s*=\s*(\w.*\w)$', self._setvar), # match a variable assignment
      )
      for pattern in patterns:
         m = re.search(pattern[0], instruction)
         if m:
            return pattern[1](m)
         return False

   def _setvar(self, match):
      key = match.group(1)
      val = match.group(2)
      self.variables[key] = val
      return True

   # Instructions to be executed when outside a block

   def _preprocess(self, line):
      patterns = (
         ('=\$(\w+)==', self._substituteVariable),
         ('=\$(\w+)\((.*)\)==', self._substituteFunction),
      )
      for pattern in patterns:
         m = re.search(pattern[0], line)
         while m:
            line = pattern[1](m, line)
            try:
               m = re.search(pattern[0], line)
            except TypeError:
               print "caught TypeError on line 126. $line is:", line
      return line
      # execute any preprocessing instructions held on the given
      # line and return the result

   def _substituteVariable(self, match, line):
      if not self.variables.has_key(match.group(1)):
         raise Exception("Variable %s is undefined!" % match.group(1))
      return line[:match.start()] + self.variables[match.group(1)] + line[match.end():]

   def _substituteFunction(self, match, line):
      if not self.functions.has_key(match.group(1)):
         raise Exception("Function %s is undefined!" % match.group(1))
      return line[:match.start()] + self.functions[match.group(1)](match.group(2)) + line[match.end():]


def main():
   reader = TemplateReader()
   reader.loadVariables({"file":"test.py"})
   reader.parseTemplate("test.bpg")
   for f in reader:
      print f

if __name__ == '__main__':
   main()
