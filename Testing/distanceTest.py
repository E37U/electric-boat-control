from math import radians, cos, sin, asin, sqrt

lastPosition = [53.32055555555556, -1.7297222222222221]
currentPosition = [53.31861111111111, -1.6997222222222223]

radLastPosition = [radians(lastPosition[0]), radians(lastPosition[1])]
radCurrentPosition = [radians(currentPosition[0]), radians(currentPosition[1])]

dlon = radCurrentPosition[1] - radLastPosition[1]
dlat = radCurrentPosition[0] - radLastPosition[0]
a = sin(dlat / 2)**2 + cos(radLastPosition[0]) * cos(radCurrentPosition[0]) * sin(dlon / 2)**2
c = 2 * asin(sqrt(a))
r = 3956
print(c * r)
