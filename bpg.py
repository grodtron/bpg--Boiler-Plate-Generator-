#!/usr/bin/python2.7

import argparse
import subprocess
import sys
import os
from preprocessor import *
from utils import *

def opts():
   """Parse command line options"""
   parser = argparse.ArgumentParser(description='Generate Boilerplate code.')
   parser.add_argument('filename', type=str, help='The name of the file to be created.')
   parser.add_argument('--template', '-t', type=str, default='main', metavar='<template name>', help='The template file to be used')
   return parser.parse_args(sys.argv[1:])

def main():
   args = opts()
   utils = Utils()
   #try:

   if utils.isKnownFileType(utils.getFileType(args.filename)):
      print "%s is known filetype" % utils.getFileType(args.filename)
   else:
      print "%s is not known filetype" % utils.getFileType(args.filename)
      sys.exit(1)

   if not utils.fileExists(args.template):
      print "Template file \"%s\" could not be found" % args.template
      sys.exit(1)

   preprocessor = TemplateReader()
   preprocessor.loadVariables({"file" : args.filename})
   preprocessor.parseTemplate(args.template)

   for f in preprocessor:
      if f.type == OutputFile.NORMAL:
         if f.name == "main":
            utils.makeFile(args.filename, f.data)
            utils.editFile(args.filename)
         else:
            utils.makeFile(f.name, f.data)
      elif f.type == OutputFile.TEMPORARY_EXECUTABLE:
         utils.makeFile("TEMPasdasdasdasdasd", f.data)
         utils.executeFile("TEMPasdasdasdasdasd")
         utils.deleteFile ("TEMPasdasdasdasdasd")

if __name__ == '__main__':
   main()
