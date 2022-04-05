from math import floor
import pygame, os
import classes as cs
import functions as fcs


display = cs.Display((530, 230), 60)
running = True

objects = {
    "ROTATIONS": cs.ROTATIONS(),
    "topRing": cs.RotatableOject("topRing", "QuadCircleRing.png", (100, 100), (10, 10)),
    "bottomRing": cs.RotatableOject("bottomRing", "QuadCircleRing.png", (100, 100), (10, 120)),
    "pinionGearTop": cs.RotatableOject("pinionGearTop", "QuadRect.png", (100, 100), (120, 10)),
    "pinionGearSide": cs.RotatableOject("pinionGearSide", "QuadCircle.png", (44, 44), (150, 150)),
    "topRingGhost": cs.RotatableOject("topRingGhost", "QuadCircleRing_LowOpa.png", (100, 100), (120, 10)),
    "wheel": cs.RotatableOject("Wheel", "QuadCircleTop/0.png", (70, 70), (135, 25))
}

vMotorTop = cs.virtualMotor(0.125, gearingFactor=3)
vMotorBottom = cs.virtualMotor(0.125, gearingFactor=3)

def processAngles():
    objects["topRing"].setAngle(objects["ROTATIONS"].topRing)
    objects["topRingGhost"].setAngle(objects["ROTATIONS"].topRing)
    objects["bottomRing"].setAngle(objects["ROTATIONS"].bottomRing)
    objects["pinionGearTop"].setAngle(objects["ROTATIONS"].pinionRotation)
    objects["pinionGearSide"].setAngle(objects["ROTATIONS"].pinionSpin)

    for object in objects:
        objects[object].updateRPM()

    objects["wheel"].setAngle(objects["ROTATIONS"].pinionRotation)
    objects["wheel"].copyRPMData(objects["pinionGearSide"])
    wheelRotationSnapped = int((floor(objects["ROTATIONS"].pinionSpin / 10)) * 10)
    objects["wheel"].setNewOriginalImage("QuadCircleTop/"+str(wheelRotationSnapped)+".png")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                objects["ROTATIONS"].resetAngles()
            if event.key == pygame.K_RETURN:
                print("Enter in new ring rotations here:")
                topRing = int(input("Top ring:    "))
                bottomRing = int(input("Bottom ring: "))
                objects["ROTATIONS"].resetAngles()
                objects["ROTATIONS"].applyRotations(topRing, bottomRing)
    
    """
    > get keys
      > adjust angles
    > process angles and calc pinion angles
    > set angles to image objects
    > draw
      > display
      > objects
    > update surface
    """

    # pressed keys
    keys = pygame.key.get_pressed()

    topTarget = 0
    bottomTarget = 0

    if keys[pygame.K_z]:
        topTarget = -1
        bottomTarget = -1
    elif keys[pygame.K_x]:
        topTarget = 1
        bottomTarget = 1
    else:
        if keys[pygame.K_q]:
            topTarget = -1
        if keys[pygame.K_w]:
            topTarget = 1
        
        if keys[pygame.K_a]:
            bottomTarget = -1
        if keys[pygame.K_s]:
            bottomTarget = 1
    
    vMotorTop.applySpeed(topTarget)
    vMotorBottom.applySpeed(bottomTarget)
    
    # set angles
    objects["ROTATIONS"].applyRotations(vMotorTop.speed, vMotorBottom.speed)

    # process angles
    processAngles()

    display.draw()

    for object in objects:
        objects[object].draw(display.surface)

    # print(f"\nTop Ring RPM:        {objects['topRing'].rpm}\nBottom Ring RPM:     {objects['bottomRing'].rpm}\nPinion Rotation RPM: {objects['pinionGearTop'].rpm}\nPinion Spin RPM:     {objects['pinionGearSide'].rpm}")
    print(f"{objects['ROTATIONS'].getInfo()}\nWheel RPM:       {objects['wheel'].rpm}")

    display.updateSurface()

"""
MAIN:
    variable declaring
    class/object setup
    mainloop

CLASSES:
    display
        surface
        draw
    swerveWheel
        CONSTANTS:
            topRingTeeth
            bottomRingTeeth
            pinionGearTeeth
        VARIABLES:
            topRing rotation
            bottomRing rotation
            pinionGearRotation
            wheelRotation
            wheelSpin

----------------------------------------

Display:
    single swerve wheel
        
"""