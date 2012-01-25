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

   filename     = args.filename
   filetype     = utils.getFileType(filename)
   template     = args.template
   templateFile = utils.getFullTemplatePath(template, filetype)

   # Do input checking (make sure that the template file exists)

   if utils.isKnownFileType(filetype):
      print "%s is known filetype" % filetype
   else:
      print "%s is not known filetype" % filetype
      sys.exit(1)

   if not utils.fileExists(templateFile):
      print "Template file \"%s\" could not be found" % template
      sys.exit(1)

   # process the template file
   preprocessor = TemplateReader()
   preprocessor.loadVariables({"file" : filename})
   preprocessor.parseTemplate(templateFile)

   # create the desired files
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
