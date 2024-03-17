import random

#function generates points on the curve
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

#extended euclid alg
def egcd(a,b):
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

#point doubling, 2P
def point_dbl(Random_point, Scale, a, p):
    if Random_point == None:
        exit
    else:
        x = Random_point[0]
        y = Random_point[1]
        top_z = (3*(pow(x,Scale)) + a) % p
        low_z = (Scale * y) % p
        top_z = top_z % p
        low_z = egcd(low_z, p)
        z = (top_z * low_z) % p
        x_r = (pow(z,2) - x - x) % p
        y_r = (z*(x - x_r) - y) % p

        point = (x_r, y_r)
        return point

#Point Multiplication
def mult_point(point, scale, a, p):
    if scale == 2:
        new_point = point_dbl(point, scale, a , p)
        return new_point
    else:
        while scale > 1:
            if point == None:
                break
            else:
                new_point = mult_point(point, scale - 1, a, p)
                x_1 = new_point[0]
                y_1 = new_point[1]
                x = point[0]
                y = point[1]
                new_y = (y_1 - y) % p
                new_x = (x_1 - x) % p
                new_x = egcd(new_x,p)
                z = (new_y * new_x) % p
                x_r = (pow(z,2) - x - x_1) % p
                y_r = (z*(x - x_r) - y) % p

                point = (x_r, y_r)
                return point
            
#point was hard set, but belongs to the group y^2 = x^3 + 0x + 7 % 547        
def shared_point_generator():
    a = 0
    b = 7
    p = 547
    point_set = generate_points(a,b,p)
    order = len(point_set)
    rndm_point = (520,543)
    return order, rndm_point, a, p

#Function creates and returns the shared x value between a users private key and a different public key
def calc_shared_point(user_private_key, differnt_user_public_key, a, p):
    shared_point = mult_point(differnt_user_public_key, user_private_key, a, p)
    while shared_point is None:
        shared_point = mult_point(differnt_user_public_key, user_private_key, a, p)
    return shared_point[0]

 #creates private key   
def create_private_key(order):
    private_key = random.randint(1, order)
    return private_key

#creates public key
def create_public_key(point, private_key, a, p):
    public_key = mult_point(point, private_key, a, p)
    return public_key