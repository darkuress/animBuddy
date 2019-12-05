#!/usr/bin/python
# -*- coding: utf-8 -*-

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender
import maya.OpenMayaRender as OpenMayaRenderv1

#class DrawNode(OpenMaya.MPxNode):
class DrawNode(OpenMayaUI.MPxLocatorNode):
    """
    """
    print "class DrawNode pre init"
    #id = OpenMaya.MTypeId(0x8001c)
    id = OpenMaya.MTypeId(0x82307)
    drawDbClassification = "drawdb/geometry/DrawNode"
    drawRegistrantId = "DrawNodePlugin"
    
    def __init__(self):
        """
        """
        print "initializing MpxLocatorNode"
        #OpenMaya.MPxNode.__init__(self)
        OpenMayaUI.MPxLocatorNode.__init__(self)
        #test points
        self.points = [OpenMaya.MPoint([0.0, 0.0, 0.0]), 
                      OpenMaya.MPoint([0.0, 10.0, 10.0])]   
                      
    @staticmethod
    def creator():
        """
        """
        print "static: creating drawnode..."
        return DrawNode()
    
    @staticmethod
    def initialize():
        """
        """
        print "static : drawnode initialize - pass"
        pass
    
    def draw(self, view, path, style, status):
        """
        Legacy viewport draw function
        if in legacy - once on init, twice on frame change, selection, navigation
        """
        print "drawing in legacy..."
        # Getting the OpenGL Renderer 
        glRenderer  = OpenMayaRenderv1.MHardwareRenderer.theRenderer()
        # Getting all classes from the renderer
        glFT = glRenderer.glFunctionTable()
        
        view.beginGL()
        glFT.glPushAttrib(OpenMayaRenderv1.MGL_ALL_ATTRIB_BITS)
        glFT.glPushMatrix()
        glFT.glDepthRange(0, 0)
        glFT.glEnable(OpenMayaRenderv1.MGL_LINE_SMOOTH)
        glFT.glEnable(OpenMayaRenderv1.MGL_POINT_SMOOTH)
        glFT.glEnable(OpenMayaRenderv1.MGL_BLEND)
        glFT.glDisable(OpenMayaRenderv1.MGL_LIGHTING)
        glFT.glBlendFunc(OpenMayaRenderv1.MGL_SRC_ALPHA, OpenMayaRenderv1.MGL_ONE_MINUS_SRC_ALPHA)
        
        # Setting a color for Viewport draw
        color1 = OpenMaya.MColor(0.0, 1.0, 0.0, 1.0)
        color2 = OpenMaya.MColor(1.0, 1.0, 1.0, 1.0)
        
        # Draw points
        glFT.glPointSize(12.0)
        glFT.glBegin(OpenMayaRenderv1.MGL_POINTS)
        glFT.glColor4f(color1[0], color1[1], color1[2], 1)
        for point in self.points:
            glFT.glVertex3f(point[0], point[1], point[2])
        glFT.glEnd()
        
        # Draw lines
        glFT.glLineWidth(3.0)
        glFT.glBegin(OpenMayaRenderv1.MGL_LINE_STRIP)
        glFT.glColor4f(color2[0], color2[1], color2[2], 1)
        for point in self.points:
            glFT.glVertex3f(point[0], point[1], point[2])
        glFT.glEnd()
        
        # Wrap
        glFT.glDisable(OpenMayaRenderv1.MGL_BLEND)
        glFT.glDisable(OpenMayaRenderv1.MGL_LINE_SMOOTH)
        glFT.glDisable(OpenMayaRenderv1.MGL_POINT_SMOOTH)
        glFT.glEnable(OpenMayaRenderv1.MGL_LIGHTING)
        glFT.glPopMatrix()
        glFT.glPopAttrib()
        view.endGL()
        
        
        
        
        
    
