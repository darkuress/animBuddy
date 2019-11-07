import maya.cmds as cmds
import os
    
def playblast(filename = "C:/Users/jhwan/Desktop/test1.avi", stName = 'amoogae'):
    basedir = os.path.dirname(os.path.realpath(__file__))
    imagePlaneFile = os.path.join(basedir, 'logo.png')

    #check existing huds
    allHuds = cmds.headsUpDisplay(lh = True)
    allHudInfo = {}
    for hud in allHuds:
        hudInfo = {}
        if cmds.headsUpDisplay(hud, visible = True, q = True):
            if not cmds.headsUpDisplay(hud, preset = True, q = True) == 'noPreset':
                hudInfo['section'] = cmds.headsUpDisplay(hud, section = True, q = True)
                hudInfo['block']  = cmds.headsUpDisplay(hud, block = True, q = True)
                hudInfo['preset'] = cmds.headsUpDisplay(hud, preset = True, q = True)
                allHudInfo[hud] = hudInfo
    
    #remove existing hudes
    for hud in allHuds:
        cmds.headsUpDisplay(hud, rem = True)
        
    try:
        cmds.headsUpDisplay('HUDFrame', 
                            section = 8, 
                            block = 0, 
                            blockAlignment = 'center',
                            dataWidth = 40,
                            preset = 'currentFrame')
    except:
        pass

    try:
        cmds.headsUpDisplay('HUDFocalLength', 
                            section = 6, 
                            block = 0, 
                            blockAlignment = 'center',
                            dataWidth = 40,            
                            preset = 'focalLength')
    except:
        pass

    try:
        cmds.headsUpDisplay('HUDStudentName', 
                            section = 7, 
                            block = 0, 
                            blockAlignment = 'center',
                            dataWidth = 40,            
                            label = stName)
    except:
        pass        
        
    # adding logo
    currentCam = cmds.lookThru(q = True)
    imgPlane = cmds.imagePlane(camera = currentCam, fileName = imagePlaneFile)   
    
    # check for grid
    isGridOn = False
    if cmds.grid(toggle = True, q = True):
        cmds.grid(toggle = False)
        isGridOn = True
    
    cmds.playblast(filename = filename,
                   format = 'avi', 
                   sequenceTime = 0,
                   clearCache = 1,
                   viewer  = 1,
                   showOrnaments =  1,
                   fp = 4,
                   percent = 100, 
                   compression = "MS-CRAM",
                   quality = 100,
                   widthHeight = (1280, 720))   
    
 
    # back to original
    if cmds.headsUpDisplay('HUDFrame', exists = True):
        cmds.headsUpDisplay('HUDFrame', remove = True)
    if cmds.headsUpDisplay('HUDFocalLength', exists = True):
        cmds.headsUpDisplay('HUDFocalLength', remove = True)
    if cmds.headsUpDisplay('HUDStudentName', exists = True):
        cmds.headsUpDisplay('HUDStudentName', remove = True)
        
    #delete logo
    cmds.delete(imgPlane) 

    if isGridOn:
        cmds.grid(toggle = True)
    
    import pprint
    pprint.pprint(allHudInfo)
    #recover huds
    for hud in allHudInfo.keys():
        try:
            cmds.headsUpDisplay(hud, 
                                section = allHudInfo[hud]['section'], 
                                block = allHudInfo[hud]['block'], 
                                blockAlignment = 'center',           
                                preset = allHudInfo[hud]['preset']
                                )        
        except:
            cmds.headsUpDisplay(hud, 
                                section = allHudInfo[hud]['section'], 
                                block = allHudInfo[hud]['block'], 
                                blockAlignment = 'center'
                                )

    