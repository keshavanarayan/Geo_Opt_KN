import rhino3dm as rg

def makeSampleMesh(U,V):
    #creating a simple mesh from a grid of points
    mesh = rg.Mesh()
    for i in range(U):
        for j in range(V):
            p = rg.Point3d(i,j,0)
            mesh.Vertices.Add(p.X, p.Y, p.Z) 
            
    for i in range(len(mesh.Vertices)-(V)):
        if ( i % V != V -1 ):
            mesh.Faces.AddFace(i,i+1, i+V+1,i+V)

    return mesh


def avgPt(ptList):

    ptX = list(map(lambda p: p.X, ptList))
    ptY = list(map(lambda p: p.Y, ptList))
    ptZ = list(map(lambda p: p.Z, ptList))
    
    return rg.Point3d(sum(ptX)/len(ptList), sum(ptY)/len(ptList), sum(ptZ)/len(ptList))

def explodeMeshRG(mesh):
    exploded =[]
    m_copy = mesh.Duplicate()
    for i in range(len(m_copy.Faces)):
        exploded.append(m_copy.Faces.ExtractFaces([0]))
    return exploded


def explodeMesh(mesh):
    meshList = []

    for i in range(len(mesh.Faces)):

        new_mesh = rg.Mesh()

        v1 = mesh.Vertices[mesh.Faces[i][0]]
        v2 = mesh.Vertices[mesh.Faces[i][1]]
        v3 = mesh.Vertices[mesh.Faces[i][2]]

        new_mesh.Vertices.Add(v1.X, v1.Y, v1.Z)
        new_mesh.Vertices.Add(v2.X, v2.Y, v2.Z)
        new_mesh.Vertices.Add(v3.X, v3.Y, v3.Z)

        if mesh.Faces[0][-1] != mesh.Faces[0][-2]:
            v4 = mesh.Vertices[mesh.Faces[i][3]]
            new_mesh.Vertices.Add(v4.X, v4.Y, v4.Z)
            new_mesh.Faces.AddFace(0, 1, 2, 3 )
        else:
            new_mesh.Faces.AddFace(0, 1, 2)
            
        meshList.append(new_mesh)


    return meshList

def getAdjancentFaceList(mesh):
    sets = []

    for i in range(mesh.Faces.Count):
        sets.append( set(mesh.Faces[i]) )
        
    allAdj = []

    for i in range(len(sets)):
        adj = []
        for j in range(len(sets)):
            if sets[i] is not sets[j]:
                inter = sets[i].intersection( sets[j])
                if len(inter) ==2:
                    adj.append(j) 
        allAdj.append(adj)
    return allAdj      


def getAdjancentFaces(mesh, MeshFaceIndex):
    sets = []

    for i in range(mesh.Faces.Count):
        sets.append( set(mesh.Faces[i]) )
        
    adj  = []

    for i in range(len(sets)):
        if sets[MeshFaceIndex] is not sets[i]:
            inter = sets[i].intersection(sets[MeshFaceIndex])
            if len(inter) ==2:
                adj.append(i) 

    return adj    


def getFaceCenter(mesh, meshFace):
    faceVertex = []

    for i in range(len(meshFace)):
        p3f = mesh.Vertices[meshFace[i]]
        faceVertex.append(rg.Point3d(p3f.X, p3f.Y, p3f.Z))
    return avgPt(faceVertex)
        

def getVertexTopology(mesh):

    m = mesh
    topology = [ [] for i in  range(len(m.Vertices))]

    for i in range(m.Faces.Count):
        vert= list(m.Faces[i])
        
        if vert[-1] == vert[-2]: t = "tri"
        else: t = "quad"
        
        if t== "quad":
            vert.append(vert[0])
            for j in range(len(vert)-1):
                if vert[j+1] not in topology[vert[j]]:
                    topology[vert[j]].append(vert[j+1])
            vert.reverse()

            for k in range(len(vert)-1):
                if vert[k+1] not in topology[vert[k]]:
                    topology[vert[k]].append(vert[k+1])
    
        if t=="tri":
            vert.pop(-1)
            vert.append(vert[0])

            for j in range(len(vert)-1):
                if vert[j+1] not in topology[vert[j]]:
                    topology[vert[j]].append(vert[j+1])
            vert.reverse()

            for k in range(len(vert)-1):
                if vert[k+1] not in topology[vert[k]]:
                    topology[vert[k]].append(vert[k+1])
   
    return topology, t

def getNakedVertices(mesh):

    topology = getVertexTopology(mesh)
    topo = topology[0]
    t = topology[1]

    nakedPts = []
    if t == "quad":
        for i in range(len(topo)):
            if len(topo[i]) <= 3: nakedPts.append(mesh.Vertices[i])
    else:
        for i in range(len(topo)):
            if len(topo[i]) <= 4: nakedPts.append(mesh.Vertices[i])    

    return nakedPts


def getNakedVertexIndexes(mesh):
    topology = getVertexTopology(mesh)
    topo = topology[0]
    t = topology[1]

    naked = []
    if t == "quad":
        for i in range(len(topo)):
            if len(topo[i]) <= 3: naked.append(i)
    else:
        for i in range(len(topo)):
            if len(topo[i]) <= 4: naked.append(i)    

    return naked


def getGraphNakedNodes(nxgraph, meshtype="tri"):
    
    naked_nodes = []
    for n in nxgraph.nodes:
        if meshtype == "tri":
            if nxgraph.degree[n] <= 2: naked_nodes.append(n) 
        else:
            if nxgraph.degree[n] <= 3: naked_nodes.append(n) 

    return naked_nodes

def getMeshType(mesh):
    if mesh.Faces.QuadCount > 0:
        typ = "quad"
    else: typ = "tri"
    return typ

def serializeNestedList(nestedList):
    import json
    return json.dumps(nestedList)