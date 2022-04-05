# ring inputs
tr = int(input("Top Rotation:    "))  # top ring
br = int(input("Bottom Rotation: "))  # bottom ring

# math
pr = (tr + br) / 2  # degrees pinion would be rotated along rings, around center of top/bottom rings 
ps = (tr-br) * 2.5  # degrees pinion would be spun around its center

# pinion outputs
print(f"\n- Calculations -\n\nPinion Rotation: {pr}\nPinion Spin:     {ps}\n")

"""
----- MEASURED -----

Top rotation:    -360
Bottom rotation:  360
Pinion rotation:  0
Pinion spin:      1800

Top rotation:    360
Bottom rotation: 360
Pinion rotation: 360
Pinion spin:     0

Top rotation:    720
Bottom rotation: 0
Pinion rotation: 360
Pinion spin:     1800

----- SCALED DOWN /360  -----

Top rotation:    -1
Bottom rotation:  1
Pinion rotation:  0
Pinion spin:      5

Top rotation:    1
Bottom rotation: 1
Pinion rotation: 1
Pinion spin:     0

Top rotation:     2
Bottom rotation:  0
Pinion rotation:  1
Pinion spin:     -5

Top rotation:    90                 | 0.25
Bottom rotation: 0                  | 0
Pinion rotation: 45                 | 0.125
Pinion spin:     -225 = -(180 + 45) | 1.625

pr = (tr + br) / 2

ps = (tr-br) * 2.5

"""