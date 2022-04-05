import pygame, os, time


class Display:
    def __init__(self, res, fps):
        self.res = res
        self.fps = fps if fps > 0 else None
        self.surface = pygame.display.set_mode(res)
        pygame.display.set_caption("Swerve Drive Simulator - LM")
        self.clock = pygame.time.Clock()
    
    def draw(self, bgColor=(50, 50, 50)):
        pygame.draw.rect(self.surface, bgColor, (0, 0, self.res[0], self.res[1]))

    def updateSurface(self):
        pygame.display.flip()
        if self.fps: self.clock.tick(self.fps)

# a + ((b-a) * x)
# b = input / where to end up
# a = current
# x factor to smooth by

class virtualMotor:
    def __init__(self, smoothingFactor, gearingFactor=1):
        self.power = 0  # raw motor speed
        self.speed = 0  # motor speed, reduced or increased by gearing factor
        self.smoothingFactor = smoothingFactor
        self.gearingFactor = gearingFactor
    
    def applySpeed(self, targetSpeed):
        # use LERP for a little momentum
        self.power = self.power + ((targetSpeed - self.power) * self.smoothingFactor)
        self.power = round(self.power, 3)
        if -0.03 < self.power < 0.03:
            self.power = 0
        elif -0.997 > self.power:
            self.power = -1
        elif 0.997 < self.power:
            self.power = 1
        self.applyGearingFactor()
    
    def applyGearingFactor(self):
        self.speed = self.power * self.gearingFactor

class ROTATIONS:
    def __init__(self, round=True):
        self.RING_TEETH = 90
        self.PINION_TEETH = 15
        self.RING_ROTATION_MAX = 720
        self.PINION_ROTATION_MAX = 360
        self.PINION_SPIN_MAX = 360
        self.ROUND = round

        self.resetAngles()
    
    def applyRotations(self, topRingChange, bottomRingChange):
        # math
        pinionRotationChange = (topRingChange + bottomRingChange) / 2
        pinionSpinChange = (topRingChange - bottomRingChange) * 2.5

        # setting
        self.topRing += topRingChange
        self.bottomRing += bottomRingChange
        self.pinionRotation += pinionRotationChange
        self.pinionSpin += pinionSpinChange

        self.checkOverlappingAngles()
        if self.ROUND: self.roundAngles()
    
    def checkOverlappingAngles(self):
        self.topRing %= self.RING_ROTATION_MAX
        self.bottomRing %= self.RING_ROTATION_MAX
        self.pinionRotation %= self.PINION_ROTATION_MAX
        self.pinionSpin %= self.PINION_SPIN_MAX

    def roundAngles(self):
        decimal = 1
        self.topRing = round(self.topRing, decimal)
        self.bottomRing = round(self.bottomRing, decimal)
        self.pinionRotation = round(self.pinionRotation, decimal)
        self.pinionSpin = round(self.pinionSpin, decimal)

    def resetAngles(self):
        self.topRing = 0
        self.bottomRing = 0
        self.pinionRotation = 0
        self.pinionSpin = 0
    
    def getInfo(self):
        os.system("clear")
        info = (f"Top Ring:        {self.topRing}\nBottom Ring:     {self.bottomRing}\nPinion Rotation: {self.pinionRotation}\nPinion Spin:     {self.pinionSpin}")
        return info

    def draw(self, surface): None
    def updateRPM(self): None

class RotatableOject:
    def __init__(self, name, imageName, scaledRes, pos):
        self.scaledRes = scaledRes
        self.name = name
        self.setNewOriginalImage(imageName)
        self.img = None
        self.pos = pos
        self.angledPos = None
        self.angle = 0
        # rpm stuff
        self.lastAngle = 0
        self.lastTime = time.time()
        self.rpm = 0

        self.processImage()
    
    def setNewOriginalImage(self, newImgName):
        self.originalImg = pygame.image.load(newImgName)
        self.scaledImg = pygame.transform.scale(self.originalImg, self.scaledRes)
    
    def processImage(self):
        self.img = pygame.transform.scale(self.scaledImg, self.scaledRes)
        self.img = pygame.transform.rotate(self.img, -self.angle)
        
        padd = (self.img.get_rect()[2]-self.scaledImg.get_rect()[2])/2
        self.angledPos = [self.pos[0]-padd, self.pos[1]-padd]

    def resetAngle(self):
        self.angle = 0
        self.processImage()
    
    def adjustAngle(self, degreeChange):
        self.angle += degreeChange
        self.processImage()
    
    def setAngle(self, newAngle):
        self.angle = newAngle
        self.processImage()
    
    def updateRPM(self):
        currTime = time.time()
        deltaTime = currTime - self.lastTime
        self.lastTime = currTime
        # deltaTime = 0.00000001 if deltaTime == 0 else deltaTime

        deltaAngle = self.angle - self.lastAngle
        self.lastAngle = self.angle
        self.rpm = deltaAngle / deltaTime
    
    def copyRPMData(self, referenceObject):
        self.lastAngle = referenceObject.lastAngle
        self.lastTime = referenceObject.lastTime
        self.rpm = referenceObject.rpm
    
    def draw(self, surface):
        self.processImage()
        surface.blit(self.img, self.angledPos)