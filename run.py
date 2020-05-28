import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.patches as patches
from scipy.ndimage.interpolation import rotate


class Pin:
    def __init__(self, name, x, y,gates):
        self.name = name
        self.x = x
        self.y = y
        self.gates = gates
def show_graph_with_labels(adjacency_matrix, mylabels, myposition,gr):
    fig,ax = plt.subplots(1)
    rect = patches.Rectangle((0,0),1,1,linewidth=1,edgecolor='r',facecolor='none')
    # Add the patch to the Axes
    ax.add_patch(rect)
    edges = gr.edges()
    weights = [gr[u][v]['weight'] for u,v in edges]
    nx.draw(gr, node_size=500, labels=mylabels, with_labels=True,pos=myposition, width = weights)
    sumLength = 0
    for tup in edges:
        u = tup[0]
        v = tup[1]
        posU = pos[u]
        posV = pos[v]
        weight = gr.get_edge_data(u,v)['weight']
        sumLength += weight*np.sqrt((posU[0] - posV[0])**2 + (posU[1] - posV[1])**2)
    print("Total wire length is: " + str(sumLength))
    plt.show()

initialRectangleCoordinate = (0,0)
initialRectangleHeight = 1
initialRectangleWidth = 1
labels ={0:'0', 1:'1', 2:'2', 3:'3'}

# initial unoptimized positions
position = np.array([[ .25, .5 ],
                     [ .75, .5 ],
                     [ .25, .25],
                     [ .6,  .75]])
pos = {}
for i in range(0, position.shape[0]):
    pos[i] = position[i]

matrix = np.array([ [ 0.0,  5.0,  0.0,  1.0,],
                    [ 5.0,  0.0,  1.0,  0.0,],
                    [ 0.0,  1.0,  0.0,  1.0,],
                    [ 1.0,  0.0,  1.0,  0.0,]])
aMatrix = np.copy(-matrix)
pin1 = Pin(4,0.0,0.5,{0:5, 1:10})
pin2 = Pin(5,1.0,1.0,{1:2, 3:1})
pin3 = Pin(6,1.0,0.0,{3:1, 0:10})
pins = []
pins.append(pin1)
pins.append(pin2)
pins.append(pin3)

gr = nx.Graph()
bx = np.zeros((matrix.shape[1],1))
by = np.zeros((matrix.shape[1],1))
for i in range(0, aMatrix.shape[0]):
    aMatrix[i,i] = np.sum(matrix[i], axis = 0)

for pin in pins:
    labels[pin.name] = str(pin.name)
    pos[pin.name] = np.array([ pin.x, pin.y ])
    for gate in pin.gates.keys():
        bx[gate,0] = bx[gate,0] + pin.x * pin.gates[gate]
        by[gate,0] = by[gate,0] + pin.y * pin.gates[gate]
        aMatrix[gate,gate] = aMatrix[gate,gate] + pin.gates[gate]
        gr.add_edge(pin.name,gate,weight=pin.gates[gate])
for i in range(0, matrix.shape[0]):
    for j in range(0, matrix.shape[0]):
        if(matrix[i,j] > 0):
            gr.add_edge(i,j,weight=matrix[i,j])

show_graph_with_labels(matrix,labels,pos,gr)
posX = np.linalg.solve(aMatrix,bx)
posY = np.linalg.solve(aMatrix,by)
position = np.concatenate((posX,posY),axis=1)
for i in range(0, position.shape[0]):
    pos[i] = position[i]

show_graph_with_labels(matrix,labels,pos,gr)


newPins = []
for i in range (position.shape[0]):
    name = i
    x = position[i,0]
    y = position[i,1]
    gates = {}
    for pin in pins:
        for gate in pin.gates.keys():
            if(name == gate):
                gates[pin.name] = pin.gates[name]
    newPins.append(Pin(name,x,y,gates))
for pin in newPins:
    print(pin.name,pin.x,pin.y,pin.gates)

newPosition = np.zeros((len(pins),2))

for i,pin in enumerate(pins):
    newPosition[i,0] = pin.x
    newPosition[i,1] = pin.y



bx = np.zeros((newPosition.shape[0],1))
by = np.zeros((newPosition.shape[0],1))
newAMatrix = np.zeros((newPosition.shape[0],newPosition.shape[0]))
for pin in newPins:
    # labels[pin.name] = str(pin.name)
    # pos[pin.name] = np.array([ pin.x, pin.y ])
    for gate in pin.gates.keys():
        gateNumber = gate-len(newPins)
        bx[gateNumber,0] = bx[gateNumber,0] + pin.x * pin.gates[gate]
        by[gateNumber,0] = by[gateNumber,0] + pin.y * pin.gates[gate]
        newAMatrix[gateNumber,gateNumber] = newAMatrix[gateNumber,gateNumber] + pin.gates[gate]

posX = np.linalg.solve(newAMatrix,bx)
posY = np.linalg.solve(newAMatrix,by)
newPosition = np.concatenate((posX,posY),axis=1)
print(newPosition)
for i in range(0, newPosition.shape[0]):
    if(pos[i+len(newPins)][0] == initialRectangleWidth or pos[i+len(newPins)][0] == 0):
        pos[i+len(newPins)][1] = newPosition[i][1]
    else:
        pos[i+len(newPins)][0] = newPosition[i][0]


show_graph_with_labels(matrix,labels,pos,gr)