import math


def xToY_SinWave(x, roundDecial=3):
    y = math.sin((1.57/1)*x)
    return round(y, roundDecial)

def yToX_SinWave(y, roundDecimal=3):
    y = (math.asin(y))/(1.57/1)
    return round(y, roundDecimal)

"""def xToY_SinWave(x, a=0.5, b=(2*(1.57/1)), h=0.5, k=0.5, roundDecimal=3):
    y = (a * math.sin(b*(x-h)) + k)
    return round(y, roundDecimal)

def yToX_SinWave(y, a=0.5, b=(2*(1.57/1)), h=0.5, k=0.5, roundDecimal=3):
    x = ((math.asin((y-k)/a))/b)+h
    return round(x, 3)"""