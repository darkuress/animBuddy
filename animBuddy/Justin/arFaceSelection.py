# -*- coding: utf-8 -*-

import maya.cmds as cmds
import os

def faceControlsUI():

    #check to see if window exists
    if cmds.window ('faceControlsUI', exists = True):
        cmds.deleteUI( 'faceControlsUI')

    #create window
    window = cmds.window( 'faceControlsUI', title = 'faceControls UI', w =200, h =200, mnb = True, mxb = True, sizeable=True, resizeToFitChildren = True )

    #main layout
    mainLayout = cmds.columnLayout( w =420, h=400)
    cmds.text( label = '')
    cmds.text( label = '')
    cmds.text( label = '')
    #rowColumnLayout
    cmds.rowColumnLayout( numberOfColumns = 3, columnWidth = [(1, 140),(2, 120),(3, 120)], columnOffset = [(1, 'right', 10)] )
    cmds.separator( h = 15)
    cmds.separator( h = 15)
    cmds.separator( h = 15)

    cmds.text( label = '')
    cmds.text( label = 'faceControls', bgc = [.12,.2,.30], fn = "boldLabelFont",height= 20 )
    cmds.text( label = '')
    cmds.text( label = '')
    cmds.text( label = '')
    cmds.text( label = '')
    
    cmds.text( label = '')
    cmds.text( label = " Select character's help", fn = "boldLabelFont",height= 20 )
    cmds.text( label = "Panel first!                     ", fn = "boldLabelFont",height= 20)
    cmds.text( label = '')
    helpPanel = cmds.ls( 'helpPanel_grp', r=1 )
    cmds.optionMenu('helpPanel', changeCommand= printNewMenuItem )
    for hp in helpPanel:
        cmds.menuItem( label= hp )
    cmds.text( label = '')
    cmds.text( label = '')
    cmds.text( label = '')
    cmds.text( label = '')    
    cmds.text( label = '')
    cmds.text( label = 'level ctl')
    cmds.text( label = 'region ctl')
    cmds.text( label = '')
    cmds.optionMenu('face_level', changeCommand= printNewMenuItem )
    cmds.menuItem( label= 'mainCtl' )
    cmds.menuItem( label= 'detailCtl')
    cmds.menuItem( label= 'allCtl')

    cmds.optionMenu('face_region', changeCommand= printNewMenuItem )
    cmds.menuItem( label= 'browCtl' )
    cmds.menuItem( label= 'eyeCtl')
    cmds.menuItem( label= 'lipCtl')
    cmds.menuItem( label= 'bridgeCtl')
    cmds.text( label = '')
    cmds.button( label = 'select ctl', bgc=[.42,.5,.60], command = select_mCtl )
    cmds.button( label = 'select ctl', bgc=[.42,.5,.60], command = region_select_ctl )
    cmds.text( label = '')
    cmds.button( label = 'reset ctl', bgc=[.42,.5,.60], command = reset_mCtl )
    cmds.button( label = 'reset ctl', bgc=[.42,.5,.60], command = region_reset_ctl )
    cmds.text( label = '')
    cmds.button( label = 'set keys', bgc=[.42,.5,.60], command = setKeysOnMCtl )
    cmds.button( label = 'set keys', bgc=[.42,.5,.60], command = region_setKeysOnCtl )
    cmds.text( label = '')
    cmds.button( label = 'delete CtrlKeys', bgc=[.42,.5,.60], command = deleteMCtlKeys )
    cmds.button( label = 'delete CtrlKeys', bgc=[.42,.5,.60], command = region_deleteCtrlKeys )
    cmds.text( label = '')
    cmds.text( label = '')    
    cmds.text( label = '')
    cmds.text( label = '')

    
    cmds.showWindow(window)



def reset_mCtl(*pArgs):
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_level', query=True, value=True)
    resetCtrl( namespace + facePart)
    
def region_reset_ctl(*pArgs):
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_region', query=True, value=True)
    resetCtrl( namespace + facePart)

def setKeysOnMCtl(*pArgs):
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_level', query=True, value=True)
    setKeysOnCtl( namespace + facePart)    
def region_setKeysOnCtl(*pArgs):
    #get namespace
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_region', query=True, value=True)
    setKeysOnCtl( namespace + facePart)

def deleteMCtlKeys(*pArgs):
    #get namespace
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_level', query=True, value=True)
    deleteCtrlKeys( namespace + facePart )
def region_deleteCtrlKeys(*pArgs):
    #get namespace
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_region', query=True, value=True)
    deleteCtrlKeys( namespace + facePart )

def select_mCtl(*pArgs):
    #get namespace
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_level', query=True, value=True)
    cmds.select( namespace + facePart + "_set")

def region_select_ctl(*pArgs):
    #get namespace
    helpPanel = cmds.optionMenu('helpPanel', query=True, value=True)
    namespace = ''
    if not helpPanel == 'helpPanel_grp':
        namespace = helpPanel.split("helpPanel")[0]
    facePart = cmds.optionMenu('face_region', query=True, value=True)
    cmds.select( namespace + facePart + "_set")


def resetCtrl( facePart):
       
    ctrls = cmds.sets( facePart +'_set', q=1 )
    for ct in ctrls:

        attrs = cmds.listAttr( ct, k=1, unlocked = 1 )
        for at in attrs:
            if 'scale' in at:
                cmds.setAttr( ct+"."+at, 1 )
            elif at=='visibility':
                continue
                #cmds.setAttr( ct+"."+at, 1 )
            else:
                cmds.setAttr( ct +"."+at, 0 )

                
def setKeysOnCtl( facePart):
        
    ctrls = ctrls = cmds.sets( facePart +'_set', q=1 )
    for ct in ctrls:    
        attrs = cmds.listAttr( ct, k=1, unlocked = 1 )
        for at in attrs:
            if at=='visibility':
                continue

            else:
                cmds.setKeyframe( ct, attribute=at )

                
        
def deleteCtrlKeys( facePart):
        
    ctrls = cmds.sets( facePart +'_set', q=1 )

    for ct in ctrls:    
        attrs = cmds.listAttr( ct, k=1, unlocked = 1 )
        for at in attrs:
            
            keyCount = cmds.keyframe( ct+"."+ at, query=True, keyframeCount=True )
            if keyCount:            
                cmds.cutKey( ct+"."+at )
    
def printNewMenuItem( item ):
    print item
