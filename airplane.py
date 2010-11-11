#!/usr/bin/env python
# -*- coding: utf-8 -*-

# airplane.py:
#     code base on Airplane Simulator by Toni Petri Rönkkö
#       (from http://www.uku.fi/~tronkko/airplane_gl.c)

# Copyright (c) 2008 Homin Lee <ff4500@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import wx
import sys

try:
    from wx import glcanvas
except ImportError:
    sys.stderr.write('You don\'t have wx.glcanvas\n')
    sys.exit(-1)

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except ImportError:
    sys.stderr.write('You don\'t have OpenGL\n')
    sys.exit(-1)

class DICanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self._isInited = False

        self._leftFlap = 0
        self._rightFlap = 0
	self._rudder = 0
	self._throttle = 0

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def onEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def onSize(self, event):
        size = self.size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
	    w, h = size.width, size.height
            glViewport(0, 0, w, h)
            glMatrixMode (GL_PROJECTION);
            glLoadIdentity ();
	    sizeMax = max(w, h) + 0.0
            glFrustum (-w/sizeMax, w/sizeMax, -h/sizeMax, h/sizeMax, 2.0, 50.0);
            gluLookAt (0,10,-25, 0,0,0, 0,1,0);
            glMatrixMode (GL_MODELVIEW);
        event.Skip()

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self._isInited:
            self.initGL()
            self._isInited = True
        self.onDraw()

    def initGL(self):       
        glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_STENCIL)
        size = self.size = self.GetClientSize()
        if self.GetContext():
            self.SetCurrent()
	    w, h = size.width, size.height 
            glViewport(0, 0, w, h)
            glMatrixMode (GL_PROJECTION)
            glLoadIdentity ();
	    sizeMax = max(w, h) + 0.0
            glFrustum (-w/sizeMax, w/sizeMax, -h/sizeMax, h/sizeMax, 2.0, 50.0);
            gluLookAt (0,10,-25, 0,0,0, 0,1,0);
            glMatrixMode (GL_MODELVIEW);

    def _drawAirplane(self):
        # Find out current stencil function.
	stencil = GL_ALWAYS
        #stencil = glGetIntegerv (GL_STENCIL_FUNC)

        # Describe airplane using simple concave polygons.
        # See `airplane-blueprint' for details. */
        glStencilFunc (stencil, 1, 0xf)
        glBegin (GL_POLYGON)    # nose
        glEdgeFlag (1)
        glVertex3f (0, -1, 10);
        glEdgeFlag (0)
        glVertex3f (2, 0,  4)
        glEdgeFlag (1)
        glVertex3f (-2, 0,  4)
        glEnd()

        glStencilFunc (stencil, 2, 0xf)
        glBegin (GL_POLYGON) # tail
        glEdgeFlag (1)
        glVertex3f ( 1, 0, -3)
        glVertex3f ( 3, 0, -4)
        glVertex3f ( 3, 0, -5)
        glVertex3f (-3, 0, -5)
        glVertex3f (-3, 0, -4)
        glEdgeFlag (0)
        glVertex3f (-1, 0, -3)
        glEnd ()

        glBegin (GL_POLYGON) # body 1/2
        glEdgeFlag (0)
        glVertex3f ( 2, 0, 4)
        glEdgeFlag (1)
        glVertex3f ( 2, 0, -0.5)
        glVertex3f ( 2, 0, -1)
        glEdgeFlag (0)
        glVertex3f ( 1, 0, -1)
        glEdgeFlag (1);
        glVertex3f (-1, 0, -1)
        glVertex3f (-2, 0, -1)
        glEdgeFlag (0)
        glVertex3f (-2, 0, -.5)
        glVertex3f (-2, 0,  4)
        glEnd ();

        glBegin (GL_POLYGON) # body 2/2
        glEdgeFlag (1)
        glVertex3f ( 1, 0, -1)
        glEdgeFlag (0)
        glVertex3f ( 1, 0, -3)
        glEdgeFlag (1)
        glVertex3f (-1, 0, -3)
        glEdgeFlag (0)
        glVertex3f (-1, 0, -1)
        glEnd ()

        glBegin (GL_POLYGON) #left wingtip
        glEdgeFlag (1)
        glVertex3f ( 8, 0,  1)
        glVertex3f ( 8, 0, -1)
        glVertex3f ( 5, 0, -1)
        glEdgeFlag (0)
        glVertex3f ( 5, 0, -0.5)
        glEnd ()

        glBegin (GL_POLYGON) # left wing
        glEdgeFlag (1)
        glVertex3f ( 2, 0,  4)
        glEdgeFlag (0)
        glVertex3f ( 8, 0,  1)
        glEdgeFlag (1)
        glVertex3f ( 5, 0, -0.5)
        glEdgeFlag (0)
        glVertex3f ( 2, 0, -.5)
        glEnd ()

        glBegin (GL_POLYGON); # right wingtip
        glEdgeFlag (1)
        glVertex3f (-5, 0, -0.5)
        glVertex3f (-5, 0, -1)
        glVertex3f (-8, 0, -1)
        glEdgeFlag (0)
        glVertex3f (-8, 0,  1)
        glEnd ()

        glBegin (GL_POLYGON) # right wing
        glEdgeFlag (0)
        glVertex3f (-2, 0,  4)
        glEdgeFlag (1)
        glVertex3f (-2, 0, -0.5)
        glEdgeFlag (0)
        glVertex3f (-5, 0, -.5)
        glEdgeFlag (1)
        glVertex3f (-8, 0,  1)
        glEnd ()

        # Create rotated coordinate system for left flap.
        glPushMatrix ()
        glTranslatef (2, 0, -0.5)
        glRotate (self._leftFlap, 1, 0, 0)

        glStencilFunc (stencil, 3, 0xf)
        glBegin (GL_POLYGON) # left flap
        glEdgeFlag (1)
        glVertex3f ( 3, 0,  0)
        glVertex3f ( 0, 0,  0)
        glVertex3f ( 0, 0, -1)
        glVertex3f ( 3, 0, -1)
        glEnd ()
        glPopMatrix ()

        # Create rotated coordinate system for right flap.
        glPushMatrix ()
        glTranslatef ( -2, 0, -0.5)
        glRotatef (self._rightFlap, 1, 0, 0)

        glStencilFunc (stencil, 4, 0xf)
        glBegin (GL_POLYGON); # right flap
        glEdgeFlag (1)
        glVertex3f (-3, 0,  0)
        glVertex3f ( 0, 0,  0)
        glVertex3f ( 0, 0, -1)
        glVertex3f (-3, 0, -1)
        glEnd ()
        glPopMatrix ()

        # Create coordinate system for tail wing.
        glPushMatrix ()
        glTranslatef (0, 0, -4.5)

        glStencilFunc (stencil, 5, 0xf); # tail wing
        glBegin (GL_POLYGON)
        glEdgeFlag (0)
        glVertex3f (0, 0, 0)
        glEdgeFlag (1)
        glVertex3f (0, 1, 1.5)
        glVertex3f (0, 0, 3)
        glEnd ()
        glBegin (GL_POLYGON)
        glEdgeFlag (1)
        glVertex3f (0, 0, 0)
        glEdgeFlag (0)
        glVertex3f (0, 2.5, 0)
        glEdgeFlag (1)
        glVertex3f (0, 3, 0.5)
        glEdgeFlag (0)
        glVertex3f (0, 1, 1.5)
        glEnd ()
        glBegin (GL_POLYGON)
        glEdgeFlag (1)
        glVertex3f (0, 2.5, 0)
        glVertex3f (0, 2.5, -0.5)
        glVertex3f (0, 3, -0.5)
        glEdgeFlag (0)
        glVertex3f (0, 3, 0.5)
        glEnd ()

        # Create coordinate system for rudder.
        glRotatef (self._rudder, 0, 1, 0)
        glStencilFunc (stencil, 6, 0xf)
        glBegin (GL_POLYGON); # rudder
        glEdgeFlag (1)
        glVertex3f (0, 0, 0)
        glVertex3f (0, 2.5, 0)
        glVertex3f (0, 2.5, -1)
        glVertex3f (0, 0, -1)
        glEnd ()
        glPopMatrix ()

        glStencilFunc (stencil, 7, 0xf)
        glBegin (GL_POLYGON); # cockpit right front
        glEdgeFlag (1)
        glVertex3f ( 0, -1, 10)
        glVertex3f (-2,  0,  4)
        glVertex3f ( 0,  1.5,5)
        glEnd ()
        glStencilFunc (stencil, 8, 0xf)
        glBegin (GL_POLYGON); # cockpit left front
        glEdgeFlag (1)
        glVertex3f ( 0, -1, 10)
        glVertex3f ( 0,  1.5, 5)
        glVertex3f ( 2,  0,   4)
        glEnd ()
        glStencilFunc (stencil, 9, 0xf)
        glBegin (GL_POLYGON) #cockpit left back
        glEdgeFlag (1)
        glVertex3f ( 0,  1.5, 5)
        glVertex3f ( 2,  0,   4)
        glVertex3f ( 1,  0,  -1)
        glEnd ()
        glStencilFunc (stencil, 10, 0xf)
        glBegin (GL_POLYGON); # cockpit right back
        glEdgeFlag (1)
        glVertex3f (-2,  0,   4)
        glVertex3f ( 0,  1.5, 5)
        glVertex3f (-1,  0,  -1)
        glEnd ()
        glStencilFunc (stencil, 11, 0xf)
        glBegin (GL_POLYGON); # cocpit top
        glEdgeFlag (1)
        glVertex3f ( 0,  1.5, 5)
        glEdgeFlag (0)
        glVertex3f (-1,  0,  -1)
        glEdgeFlag (1)
        glVertex3f ( 1,  0,  -1)
        glEnd ()

    def onDraw(self):
        # Clear the display before redrawing it.
        glClearColor (1.0, 1.0, 1.0, 0.0)
        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glEnable (GL_STENCIL_TEST)
        glPushMatrix ()

        # Draw airplane's interior to depth and stencil buffers.
        glEnable (GL_DEPTH_TEST)
        glColorMask (0, 0, 0, 0)
        glStencilFunc (GL_ALWAYS, 1, 1)
        glStencilOp (GL_KEEP, GL_KEEP, GL_REPLACE)
        glPolygonMode (GL_FRONT_AND_BACK, GL_FILL)
        self._drawAirplane()

        # Draw outline to color buffer where stencil buffer allows.
        glColorMask (1, 1, 1, 1);
        glEnable (GL_LINE_SMOOTH);
        glDisable (GL_DEPTH_TEST);
        glStencilFunc (GL_EQUAL, 1, 1);
        glStencilOp (GL_KEEP, GL_KEEP, GL_KEEP);
        glLineWidth (2);
        glColor3f (self._throttle, 0, 1-self._throttle);
        glPolygonMode (GL_FRONT_AND_BACK, GL_LINE);
        self._drawAirplane() 
        glPopMatrix ();
        #glutSwapBuffers ()
        self.SwapBuffers()


    def onKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        print keycode
	if keycode == wx.WXK_UP:
            glRotatef (2, 1, 0, 0)
            self._leftFlap  = -20
            self._rightFlap = -20
            self._rudder     =  0
	elif keycode == wx.WXK_DOWN:
            glRotatef (-2, 1, 0, 0)
            self._leftFlap  = 20
            self._rightFlap = 20
            self._rudder     =  0
	elif keycode == wx.WXK_LEFT:
            glRotatef (-3, 0, 0, 1)
            self._leftFlap  = 20
            self._rightFlap = -20
            self._rudder     =  0
	elif keycode == wx.WXK_RIGHT:
            glRotatef (3, 0, 0, 1)
            self._leftFlap  = -20
            self._rightFlap = 20
            self._rudder     =  0
	elif keycode == ord('A'):
            glRotatef (1, 0, 1, 1)
            self._leftFlap  = 0
            self._rightFlap = 0
            self._rudder     = -30
	elif keycode == ord('D'):
            glRotatef (-1, 0, 1, 1)
            self._leftFlap  = 0
            self._rightFlap = 0
            self._rudder     = 30
	elif keycode == ord('W'):
            if self._throttle < 1:
                self._throttle += 0.01
	elif keycode == ord('S'):
            if self._throttle > 0:
                self._throttle -= 0.01

        self.Refresh(False)

if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    frame = wx.Frame(None, -1, "Dragon Ilusion", size=(400,400))
    app.SetTopWindow(frame)
    canvas = DICanvas(frame)
    frame.Show(True)
    app.MainLoop()

