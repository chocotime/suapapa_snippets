#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All-in-one-Curve python-fu pour Gimp 2.4
# Copyright Raymond Ostertag 2007
# Licence GPL

# Version 1.0
# - initial release

# Installation : put the all-in-one-curve.py file in your $HOME/.gimp-2.n/plug-ins.
# On Linux and Mac OSX the file must be executable.
# Documentation : http://www.gimp.org/docs/python/index.html

from gimpfu import *

# i18n
#
import gettext
locale_directory = gimp.locale_directory #return a wrong path until Gimp-2.4.2 under Windows see bug 502506
gettext.install( "gimp20-template" , locale_directory, unicode=True )

# description
#
_apply_curve_help = _("Apply any curve file to image")                                
_apply_curve_description = _("All-in-one-Curve for Gimp 2.4.")+" "+_apply_curve_help

# constants
#
import os
dircurve = "~/.gimp-2.4/curves/" #default searching pathname for curves
dircurve = os.path.expanduser( dircurve )
if not os.path.exists( u''+dircurve ):
  dircurve = os.path.expanduser( "~" ) #otherwise start from user director

# curve engine
#
import curve
def _extractPoints(points):
  liRet = []
  for x, y in points:
    liRet.append(x)
    liRet.append(y)
  return liRet

def python_fu_apply_curve( 
  inImage, inLayer, curveFilename
  ):
  #print curveFilename
  #print locale_directory
  try:
    crv = curve.getCurveFrom(curveFilename)
  except curve.CurveError, e:
    pdb.gimp_message(e.msg)
    return
  iCrvL = _extractPoints(crv.getPointsOfChannel('L'))
  iCrvR = _extractPoints(crv.getPointsOfChannel('R'))
  iCrvG = _extractPoints(crv.getPointsOfChannel('G'))
  iCrvB = _extractPoints(crv.getPointsOfChannel('B'))
  if iCrvL:
    pdb.gimp_curves_spline( inLayer, HISTOGRAM_VALUE, len(iCrvL), iCrvL )
  if iCrvR:
    pdb.gimp_curves_spline( inLayer, HISTOGRAM_RED, len(iCrvR), iCrvR )
  if iCrvG:
    pdb.gimp_curves_spline( inLayer, HISTOGRAM_GREEN, len(iCrvG), iCrvG )
  if iCrvB:
    pdb.gimp_curves_spline( inLayer, HISTOGRAM_BLUE, len(iCrvB), iCrvB )

register(
  "python_fu_apply_curve",
  _apply_curve_description,
  _apply_curve_help,
  "Homin Lee (Suapapa)",
  "GPL License",
  "2008",
  _("Apply Curve"),
  "",
  [
    (PF_IMAGE, "inImage", "Input image", None),
    (PF_DRAWABLE, "inLayer", "Input drawable", None),
    (PF_FILENAME, "curveFilename", _("Curve file"), dircurve)
    #(PF_FILENAME, "pf_filename", _("File name"), ""), #str
  ],
  [],
  python_fu_apply_curve,
  #menu="<Toolbox>/Xtns/Python-Fu",
  menu="<Image>/Colors/",#+_("Photolab"),
  domain=("gimp20-template", locale_directory)  
  )

main()
