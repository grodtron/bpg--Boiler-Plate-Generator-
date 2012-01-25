#!/usr/bin/python

import os
import subprocess

#Utils needed based on this:
   #fileExists()
   #getFileType()
   #makeFile()
   #editFile()
   #executeFile()
   #deleteFile()

class Utils:
   def __init__(self):
      self.knownTypes = os.listdir(os.environ["HOME"] + "/.bpg/templates")
      self.editor = self._getEditor()

   # return the file extension without any dot
   def getFileType(self, filename):
      return os.path.splitext(filename)[1][1:]

   def isKnownFileType(self, filetype):
      return filetype in self.knownTypes

   def makeFile(self, filename, data):
      f = open(filename, 'w')
      f.write(data)
      f.close()

   def deleteFile(self, filename):
      os.remove(filename)

   def executeFile(self, filename):
      os.chmod(filename, 365) # 365 == int("555",8) == r-xr-xr-x (no write)
      return subprocess.call(os.path.abspath(filename))

   def editFile(self, filename):
      return subprocess.call([self.editor, filename])

   def fileExists(self, f):
      return os.path.exists(f)

   def programExists(self, program):
      for path in os.environ["PATH"].split(os.pathsep):
         f = os.path.join(path, program)
         if self.fileExists(f) and os.access(f, os.X_OK):
            return True
      return False

   def getFullTemplatePath(self, name, ftype):
      return os.environ["HOME"] + "/.bpg/templates/%s/%s" % (ftype, name)

   def _getEditor(self):
      editor = ""
      if os.environ.has_key("EDITOR"):
         editor = os.environ["EDITOR"]
      candidates = ("vim", "vi", "emacs", "nano", "ed")
      for ed in candidates:
         if self.programExists(ed):
            editor = ed
            break
         else:
            print "%s is not a program that exists" % ed
      return editor

def main():
   utils = Utils()
   utils.editFile("testing_deleteme.txt")

if __name__ == '__main__':
   main()
