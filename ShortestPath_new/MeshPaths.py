import networkx as nx
import rhino3dm as rg
import meshutils as mu


#create a def that converst a mesh to nx graph
def graphFromMesh(mesh):

    g = nx.Graph()
    m = mesh

    #create a node per each of the faces of the mesh
    for i in range(m.Faces.Count):

        face_center = mu.getFaceCenter(m, m.Faces[i])

        #add a node to the graph per face
        g.add_node(i, point = face_center, face = i)

        #finding the neighbors of this face
        neighbors = mu.getAdjancentFaces(mesh, i) #returns a list of face indexes which are neighbors

        for n in neighbors:
            if n > i:
                p1 = mu.getFaceCenter(m, m.Faces[i])
                p2 = mu.getFaceCenter(m, m.Faces[n]) 
                line = rg.Line(p1, p2)
                w = line.Length
                g.add_edge(i, n, weight = w, line = line)

    return g

def shortestPath(g, f1, f2):

    sp = nx.shortest_path(g, f1, f2, weight = "weight")
    
    pts = [g.nodes[i]["point"] for i in sp]
    faceInd = [g.nodes[i]["face"] for i in sp]

    return pts, faceInd, sp

def dijkstraPath(g, f1, f2):

    sp = nx.dijkstra_path(g, f1, f2, weight = "weight")
    
    pts = [g.nodes[i]["point"] for i in sp]
    faceInd = [g.nodes[i]["face"] for i in sp]

    return pts, faceInd, sp

def longestPath(g, f1, f2):

    sp = nx.dag_longest_path(g, f1, f2, weight = "weight")
    
    pts = [g.nodes[i]["point"] for i in sp]
    faceInd = [g.nodes[i]["face"] for i in sp]

    return pts, faceInd, sp

