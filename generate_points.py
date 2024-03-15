import math, random

def generate_points(a, b, p):
    x = 0
    points = []
    for x in range(0, p):
        for y in range(0, p):
            x_value = (pow(x,3) + (a*x) + b) % p
            y_value = (pow(y,2) % p)
            if x_value == y_value:
                point = (x,y)
                points.append(point)
                inverse_ypoint = -y % p
                point = (x, inverse_ypoint)
                points.append(point)
    point_set = set()
    for value in points:
        point_set.add(value)
    true_points = []
    for value in point_set:
        true_points.append(value)
    return true_points

def random_point(point_set):

    size = len(point_set)
    random_num = random.randint(0, size)
    return point_set[random_num]

def egcd(a,b):
    # TODO: implement Extended Euclidean Algorithm and return the values r,s,t, and q from the row *before* r = 0
  past_r = a
  r = b
  past_x = 1
  x = 0
  past_y = 0
  y = 1
  past_q = 0
  q = 0
  while r != 0:
    past_q = q
    q = past_r // r
    past_r, r = r, past_r - q * r
    past_x , x = x , past_x - q * x
    past_y , y = y , past_y - q * y
  return int(past_x)


def point_dbl(Random_point, Scale, a, p):
    x = Random_point[0]
    y = Random_point[1]
    top_z = (3*(pow(x,Scale)) + a) % p
    low_z = (Scale * y) % p
    top_z = top_z % p
    low_z = pow(int(low_z), -1, p)
    z = (top_z * low_z) % p
    x_r = (pow(z,2) - x - x) % p
    y_r = (z*(x - x_r) - y) % p

    point = (x_r, y_r)
    return point

def mult_point(point, scale, a, p):
    if scale % 2 == 0:
        new_point = point_dbl(point, scale, a , p)
        return new_point
    else:
        new_point = point_dbl(point, scale - 1, a, p)
        x_1 = new_point[0]
        y_1 = new_point[1]
        x = point[0]
        y = point[1]
        new_y = (y_1 - y) % p
        new_x = (x_1 - x) % p
        new_x = (pow(int(new_x), -1, p))
        z = (new_y * new_x) % p
        x_r = (pow(z,2) - x - x_1) % p
        y_r = (z*(x - x_r) - y) % p

        point = (x_r, y_r)
        return point

point_set = generate_points(9,17, 23)
order = len(point_set)
print(order)
rndm_point = random_point(point_set)
print(rndm_point)
two_p = mult_point((16,5), 4, 9, 23)
print(two_p)

