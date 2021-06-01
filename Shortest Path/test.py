        
import Rhino.Geometry as rg
import math

"""
##Assignment 2 : Keshava Narayan_SYNC

m = input mesh from previous code
s = sunvector
r = radius of circle (b/n 0 to 1)
x = multiplier ( 1 to 10)
z = height on stellated mesh on each mesh face (0 to 1)

"""

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a

a = []
for i in range(len(m.Faces)):
    normal = m.FaceNormals[i]
    rev_normal= rg.Vector3d.Negate(normal)
    a.append(rev_normal)


#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b


b = []
for i in range(len(m.Faces)):
    center = m.Faces.GetFaceCenter(i)
    b.append(center)


#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

#c = angleList
c = []
for i in range(len(m.Faces)):
    angle = rg.Vector3d.VectorAngle(a[i],s)
    c.append(angle)


#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

#d = exploded
d = []
m_new = m.Duplicate()
for i in range(len(m.Faces)):
    meshface = m_new.Faces.ExtractFaces([0])
    d.append(meshface)


#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!


e=[]
for i in range(len(m.Faces)):
    amp=rg.Vector3d.Multiply(a[i],z)
    e.append(amp)

f=[]
for i in range(len(m.Faces)):
    line=rg.Line(b[i],e[i])
    f.append(line)

g=[]
for i in range(len(m.Faces)):
    l=f[i]
    p=l.PointAt(math.cos(c[i])*-x)
    g.append(p)

h=[]
for i in range(len(m.Faces)):
    plane=rg.Plane(g[i],a[i])
    h.append(plane)

j=[]
for i in range(len(m.Faces)):
    circle=rg.Circle(h[i], r)
    c_n=circle.ToNurbsCurve()
    j.append(c_n)


k=[]
for i in range(len(m.Faces)):
    q=d[i]
    m_edge=q.GetNakedEdges()
    nurbsline=[]
    for u in range(len(m_edge)):
        m_line=m_edge[u]
        line=m_line.ToNurbsCurve()
        nurbsline.append(line)
    nurbscurve=rg.Curve.JoinCurves(nurbsline)[0]
    k.append(nurbscurve)


#paramtric transformable mesh that reacts with the sun vector and moves in height according to the vector
l=[]
for i in range(len(m.Faces)):
    list=[]
    circle=j[i]
    curve=k[i]
    list.append(circle)
    list.append(curve)
    t_p=rg.Curve.ClosestPoint(circle,rg.Curve.PointAt(curve,0),5)[1]
    rg.Curve.ChangeClosedCurveSeam(circle,t_p)
    one=rg.Brep.CreateFromLoft(list,rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, False)[0]
    l.append(one)