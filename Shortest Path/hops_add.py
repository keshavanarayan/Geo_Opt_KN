from flask import Flask
import ghhops_server as hs
import rhino3dm

app = Flask(__name__)
hops = hs.Hops(app)
@hops.component(
    "/sample", 
    name="sampleComponent", 
    description="this is a sample component",
    inputs=[
        hs.HopsInteger("Input X", "X","Input X of Sample"),
        hs.HopsInteger("Input Y", "Y","Input Y of Sample"),
    ],
    outputs=[
        hs.HopsInteger("Input S", "S","Input S of Sample"),
        #hs.HopsInteger("Input M", "M","Input M of Sample"),
    ]
)



def sampleFunction(X,Y):
    add=X+Y
    #mult=X*Y
    return add  #,mult

if __name__=="__main__":
    app.run()