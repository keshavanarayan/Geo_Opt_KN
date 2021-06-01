from flask import Flask
import ghhops_server as hs
import rhino3dm as r
import random

import MeshPaths as mp
import meshutils as mu
    
# register hops app as middleware
app = Flask(__name__)
hops = hs.Hops(app)



#global variables for meshwalker component
walkerGraph = None
@hops.component(
    "/meshwalker",
    name = "meshwalker",
    inputs=[
        hs.HopsBoolean("reset","R","reset button"),
        hs.HopsMesh("Input Mesh", "M", "Mesh"),
        hs.HopsInteger("face Index 1","f1","Face index one"),
        hs.HopsInteger("face Index 2","f2","Face index two")

    ],
    outputs=[
        hs.HopsPoint("list of points","P","shortest path points", hs.HopsParamAccess.LIST),
        hs.HopsInteger("list of faces indexes","F","shortest path face indexes", hs.HopsParamAccess.LIST)
    ]
)
def meshwalker(reset, mesh, f1, f2):
    global walkerGraph

    #do something with this mesh
    if reset:
        walkerGraph = mp.graphFromMesh(mesh) #convert the mesh to a nx graph

    else:
        #use the graph to find the shortest path between two faces
        SP = mp.dijkstraPath(walkerGraph, f1, f2)
        pts = SP[0]
        faceInd = SP[1]

    return pts, faceInd


#global variables for meshstripper component
geostrips= []
geopoints = []
slen = []
geoGraph = None

@hops.component(
    "/meshstripper",
    name = "meshstripper",
    inputs=[
        hs.HopsBoolean("reset","R","reset button"),
        hs.HopsMesh("Input Mesh", "M", "Mesh"),
        #hs.HopsInteger("face Index 1","f1","Face index one"),
        #hs.HopsInteger("face Index 2","f2","Face index two")

    ],
    outputs=[
        hs.HopsPoint("list of points","P","shortest path points", hs.HopsParamAccess.LIST),
        hs.HopsInteger("list of faces indexes","F","shortest path face indexes", hs.HopsParamAccess.LIST),
        hs.HopsInteger("strip pattern","SP","pattern of strips", hs.HopsParamAccess.LIST)

    ]
)
def meshstripper(reset, mesh):
    global geoGraph
    global geostrips
    global slen
    global geopoints

    meshtype = mu.getMeshType(mesh)
    pts = []
    faceInd = []
    missed = 0
    iterations = 0

    #do something with this mesh
    if reset:
        geoGraph = mp.graphFromMesh(mesh) #convert the mesh to a nx graph
        geostrips = []
        geopoints= []
        slen = []
        
    else:   
        while len(geoGraph.edges)>0:
            iterations +=1

            nakedfaces = mu.getGraphNakedNodes(geoGraph, meshtype)

            if len(nakedfaces) > 0:
                random_naked = random.sample(nakedfaces, 2)
            else:
                random_naked = random.sample( geoGraph.nodes,2)


            try:
                #use the graph to find the shortest path between two faces
                #SP = mp.shortestPath(geoGraph, random_naked[0], random_naked[1])
                #SP = mp.longestPath(geoGraph, random_naked[0], random_naked[1])
                SP = mp.dijkstraPath(geoGraph, random_naked[0], random_naked[1])  
                #SP = mp.burnEdgesPath(geoGraph)

            except:
                missed += 1
                continue

            #SP = mp.longestPath(geoGraph, random_naked[0], random_naked[1])

            pts = SP[0]
            faceInd = SP[1]
            nodes = SP[2]

            geopoints.extend(pts)

            geostrips.extend(faceInd)
            slen.append(len(faceInd))
            geoGraph.remove_nodes_from(nodes)

        print("-- run {} times and failed {} to get path --".format(iterations, missed))

        #after the graph is deconstructed, append remaining faces to strip and and remove nodes
        if len(geoGraph.nodes) >0:
            for n in geoGraph.nodes:
                geostrips.append(geoGraph.nodes[n]["face"])
                slen.append(1)
            geoGraph.remove_nodes_from([geoGraph.nodes[i]["face"] for i in geoGraph.nodes])

    return geopoints, geostrips, slen









if __name__ == "__main__":
    app.run(debug=True)
    #app.run()