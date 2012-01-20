#!/usr/bin/python2.7

import argparse
import subprocess
import sys
import os

# Handle all configuration related stuff
# for now this is just finding static templates
# eventually it could include reading config files,
# finding defaults, etc
class Config:
   def __init__(self):
      self.knownTypes = os.listdir(os.environ["HOME"] + "/.bpg/templates")
   
   def isKnownType(self, fileType):
      return fileType in self.knownTypes

   def getTemplate(self, fileType, templateName):
      templateFileName = os.environ["HOME"] + "/.bpg/templates/" + fileType + '/' + templateName
      if(os.path.exists(templateFileName)):
         print "template exists " + templateFileName
         return open(templateFileName)
      else:
         print "template does not exist " + templateFileName 
         return None

   # modified from here: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
   def getEditor(self):
      def programExists(program):
         def is_exe(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK)
         for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
               return True

         return False
      editor = ""
      if os.environ.has_key("EDITOR"):
         editor = os.environ["EDITOR"]
      candidates = ("vim", "vi", "emacs", "nano", "ed")
      for ed in candidates:
         if programExists(ed):
            editor = ed
            break
         else:
            print "%s is not a program that exists" % ed
      # cache results and don't do whole calculation next time
      # this is probably TOTALLY uneccessary, but I like self-modifying things,
      # so it's fun for me :). Probably will remove later
      self.getEditor = lambda : editor
      return self.getEditor()
      

def opts():
   """Parse command line options"""
   parser = argparse.ArgumentParser(description='Generate Boilerplate code.')
   parser.add_argument('filename', type=str, help='The name of the file to be created.')
   parser.add_argument('--template', '-t', type=str, default='main', metavar='<template name>', help='The template file to be used')
   return parser.parse_args(sys.argv[1:])

def main():
   args = opts()
   config = Config()
   #try:
   if not config.isKnownType(os.path.splitext(args.filename)[1]):
      print "the file is not of a known type"
   else:
      print "the file is of a known type"
   if os.path.isfile(args.filename):
      # ask to overwrite
      pass
   f = open(args.filename, "w")
   template = config.getTemplate(os.path.splitext(args.filename)[1], args.template)
   f.write(template.read())
   template.close()
   f.close()
   editor = config.getEditor()
   print editor
   subprocess.call("%s %s" % (editor, args.filename), shell=True)
         

   #except AttributeError:
      # do nothing...
      #pass

if __name__ == '__main__':
   main()
