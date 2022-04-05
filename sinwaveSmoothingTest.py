import pygame
import classes as cs
import functions as fcs


display = cs.Display((300, 300), 60)
running = True

disc = cs.RotatableOject("Disc", "QuadCircleRing.png", (250, 250), (25, 25))

def weirdSinInterpolation(curr, target, smoothing):
    currWaveX = fcs.yToX_SinWave(curr)
    targetCurrDiff = target-curr
    diffWaveX = fcs.yToX_SinWave(targetCurrDiff)
    return currWaveX+(diffWaveX*smoothing)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    rotationSpeed = 0
    targetSpeed = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        targetSpeed = -1
    if keys[pygame.K_d]:
        targetSpeed = 1

    rotationSpeed = weirdSinInterpolation(rotationSpeed, targetSpeed, 1)
    disc.setAngle(disc.angle + rotationSpeed*3)
    print(targetSpeed, rotationSpeed)

    display.draw()
    
    disc.draw(display.surface)

    display.updateSurface()