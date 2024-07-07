import math
screenx=1550
screeny=810
x=0
y=1
z=2
sr=300 #screen depth

cm=[0,0,1000] #camera position
def clbrt(c):
    return[c[0]+(screenx/2),c[1]+(screeny/2)]
def unclbrt(c):
    return[(screenx/2)-c[0],(screeny/2)-c[1]]
def magnify(point,calibrated,scale_factor):
    if calibrated:
        point=unclbrt(point)
        point[0]=point[0]*scale_factor
        point[1]=point[1]*scale_factor
        return clbrt(point)
    else:
        point[0]=point[0]*scale_factor
        point[1]=point[1]*scale_factor
        return point
def project(i):
    if cm[x]-i[x] !=0:
        m=(cm[z]-i[z])/(cm[x]-i[x])
        x1=((sr-i[z])/m)+i[x]
    else:
        x1=i[x]
    if cm[y]-i[y] !=0:
        m=(cm[z]-i[z])/(cm[y]-i[y])
        y1=((sr-i[z])/m)+i[y]
    else:
        y1=i[y]
    coords=[x1,y1]
    return coords

def point_in_plane(point,plane_extreme1,plane_extreme2):
    if (plane_extreme2[0]>=point[0]>=plane_extreme1[0] or plane_extreme2[0]<=point[0]<=plane_extreme1[0]) and (plane_extreme2[1]>=point[1]>=plane_extreme1[1] or plane_extreme2[1]<=point[1]<=plane_extreme1[1]):
        return True
    else:
        return False
def point_in_rect(point,rect):
    return point_in_plane(point,rect.topleft,rect.bottomright)
def point_inside(point, vertices):
    x,y=point
    def winding_number(x, y, vertices):
        wn = 0
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            
            if y1 <= y:
                if y2>y and(x2-x1)*(y-y1)-(x-x1)*(y2-y1)>0:
                    wn+= 1
            else:
                if y2<=y and(x2-x1)*(y-y1)-(x-x1)*(y2-y1)<0:
                    wn-= 1
        return wn
    return winding_number(x, y, vertices) != 0

def calculate_circle_points(radius, num_points):
    circle_points = []
    angle_increment = 360 / num_points

    for i in range(num_points):
        angle_rad = math.radians(i * angle_increment)
        x = int(radius * math.cos(angle_rad))
        y = int(radius * math.sin(angle_rad))
        circle_points.append((x, y))

    return circle_points
def rotate_point(point,axis1,axis2,angle):
    xycorrection=angle
    x=axis1
    y=axis2
    i=point[:]
    i[x],i[y]=i[x]*math.cos(math.radians(xycorrection)) - i[y]*math.sin(math.radians(xycorrection)),i[x]*math.sin(math.radians(xycorrection)) + i[y]*math.cos(math.radians(xycorrection))
    return i

def dist(p1,p2):
    return((((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**0.5)
def geo_cent(coords):
    no=len(coords)
    x=y=z=0
    for i in coords:
        x+=i[0]
        y+=i[1]
        z+=i[2]
    return([x/no,y/no,z/no])
def dist3d(coords,coords2):
    return ((coords[0]-coords2[0])**2+(coords[1]-coords2[1])**2+(coords[2]-coords2[2])**2)**0.5
def avg_depth(plane,points_array):
    plane=plane.split(" ")
    avg=0
    for i in range(4):
        avg+=dist3d(points_array[plane[i]].coords3d,cm)
    return avg/4
def angle_between_points(point1, point2):
    angle1 = math.atan2(point1[1], point1[0])
    angle2 = math.atan2(point2[1], point2[0])
    angle_between_lines = angle2 - angle1
    angle_between_lines = (angle_between_lines + 2 * math.pi) % (2 * math.pi)
    return math.degrees(angle_between_lines)
def bulk_magnify(points_array,calibrated,scale_factor):
    magnified_vertices=[ ]
    for i in points_array:
        magnified_vertices.append(magnify(i,calibrated,scale_factor))
    return magnified_vertices
