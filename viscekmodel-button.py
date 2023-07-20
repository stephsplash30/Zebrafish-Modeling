import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import math

class MarkovChain:
    def __init__(self):
        self.transition_matrix = {
            'A': {'A': 0.99, 'B': 0.005, 'C': 0.005},
            'B': {'A': 0.005, 'B': 0.99, 'C': 0.005},
            'C': {'A': 0.001, 'B': 0.004, 'C': 0.995}
        }
        sampleList = ['A','B','C']
        self.current_state = random.choices(sampleList, weights=(10, 10, 10), k=1)[0]


    def next_state(self):
        transition_probabilities = self.transition_matrix[self.current_state]
        next_state = random.choices(list(transition_probabilities.keys()), list(transition_probabilities.values()))[0]
        self.current_state = next_state
        return next_state
    def get_state(self):
        return self.current_state

    def set_transition(self, matrix):
        self.transition_matrix=matrix

# Usage example
# Set up the simulation parameters
box_size = 10
num_agents = 20
speed = 0.05*np.ones([num_agents,1])
noise = 0.005*np.ones([num_agents,1])
radius = np.zeros(num_agents)
time = 1000
const = 10
mc = []
colors = []
social = []
vradius = 0.5
current_frame = 0
delt = 100
for i in range(num_agents):
    mc.append(MarkovChain())
    colors.append('red')
    social.append(0.5 * np.random.rand() + 0.5) 
    
# Set up the initial positions and velocities of the agents
positions = np.random.uniform(size=(num_agents, 2)) * box_size
velocities = np.random.uniform(size=(num_agents, 2)) * speed
# Define a function to update the velocities of the agents
def update_velocities(positions, velocities, radius, speed, noise):
    global mc
    global num_agents
    # Compute the distances between all pairs of agents
    distances = np.linalg.norm(positions[:, np.newaxis] - positions, axis=2)
    
    # Find the indices of the neighbors within the specified radius
    neighbors=[]
    # Find the indices of the neighbors within the specified radius
    for i in range(num_agents):
       tempneigh = np.argwhere(distances<(radius[i]*social[i]))
       for j in tempneigh:
           if j[0]==i:
               neighbors.append(j)
    nearby = np.argwhere(distances < vradius)
    
    # Compute the average direction of the neighbors
    mean_direction = np.zeros((num_agents, 2))
    for i in range(num_agents):
        mystate = mc[i].get_state()
        school = 0
        swim = 0
        sleep = 0
        sum_direction = np.zeros(2)
        count = 0
        for j in neighbors:
            if j[0] == i:
                weight = abs(np.dot(positions[j[1]]-positions[j[0]],velocities[j[0]]))
                #sum_direction += weight * velocities[j[1]]
                #count += weight
                sum_direction += velocities[j[1]]*speed[j[1]]*weight
                count += speed[j[1]]*weight
        for j in nearby:
            if j[0] == i:
                state = mc[j[1]].get_state()
                if state == 'A':
                    school += 1
                elif state == 'B':
                    swim += 1
                else:
                    sleep += 1
        if school != 0 and swim !=0:
            matrix = {
                'A': {'A': 1-(0.005*(1+sleep))-.005*math.pow((swim/school),1), 'B': .005*math.pow((swim/school),1), 'C': 0.005*(1+sleep)},
                'B': {'A': .005*math.pow((school/swim),1), 'B': 1-(0.005*(1+sleep))-.005*math.pow((school/swim),1), 'C': 0.005*(1+sleep)},
                'C': {'A': (1/5)*(1-0.995*(sleep/(swim+school))), 'B': (4/5)*(1-0.995*(sleep/(swim+school))), 'C': 0.995*(sleep/(swim+school))}
            }
            mc[i].set_transition(matrix)
        elif school == 0 and swim !=0:
            matrix = {
                'A': {'A': 0.895-sleep*0.005-swim*0.05, 'B': .10+swim*.05, 'C': 0.005*(1+sleep)},
                'B': {'A': .01, 'B': .99-(0.005*(1+sleep)), 'C': 0.005*(1+sleep)},
                'C': {'A': (1/5)*(1-0.995*(sleep/(swim+school))), 'B': (4/5)*(1-0.995*(sleep/(swim+school))), 'C': 0.995*(sleep/(swim+school))}
            }
            mc[i].set_transition(matrix)
        elif school != 0 and swim ==0:
            matrix = {
                'A': {'A': 0.99-(0.005*(1+sleep)), 'B':0.01, 'C': 0.005*(1+sleep)},
                'B': {'A': .10+school*.05, 'B': 0.895-sleep*0.005-school*.05, 'C': 0.005*(1+sleep)},
                'C': {'A': (1/5)*(1-0.995*(sleep/(swim+school))), 'B': (4/5)*(1-0.995*(sleep/(swim+school))), 'C': 0.995*(sleep/(swim+school))}
            }
            mc[i].set_transition(matrix)
        else:
            matrix = {
                'A': {'A': 0.995-.0005*sleep, 'B': 0.005, 'C': 0.005*sleep},
                'B': {'A': 0.005, 'B': 0.995-0.005*sleep, 'C': 0.005*sleep},
                'C': {'A': 0.002, 'B': 0.008-(0.01*sleep/num_agents), 'C': 0.99+(0.01*sleep/num_agents)}
            }
            mc[i].set_transition(matrix)
        if count > 0:
            mean_direction[i] = sum_direction / count
    
    # Add some random noise to the direction
    noise_vector = np.random.normal(size=(num_agents, 2)) * noise
    
    # Normalize the direction and set the velocity of each agent
    norm = np.linalg.norm(mean_direction, axis=1)
    norm[norm == 0] = 1  # Avoid division by zero
    mean_direction /= norm[:, np.newaxis]
    for i in range(len(mean_direction)):
        if mean_direction[i][0] == 0 and mean_direction[i][1] == 0:
            velocities[i]+=noise_vector[i]
        else:
            velocities[i] = mean_direction[i] * speed[i] + noise_vector[i]
    normv = np.linalg.norm(velocities, axis=1)
    normv[normv == 0] = 1  # Avoid division by zero
    for i in range(num_agents):
        velocities[i] = velocities[i]/normv[i] * speed[i]
    #for i in range(num_agents):
        #sum_direction = np.zeros(2)
        #count = 0
        #for j in neighbors:
            #if j[0] == i:
                #weight = abs(np.dot(positions[j[1]]-positions[j[0]],velocities[j[0]])/speed)
                #sum_direction += weight * velocities[j[1]]
                #count += weight
        #if count > 0:
            #mean_direction[i] = sum_direction / count
        #if mean_direction[i][0] == 0 and mean_direction[i][1] == 0 :
            #mean_direction[i]=positions[i]
    
    # Add some random noise to the direction
    #noise_vector = np.random.normal(size=(num_agents, 2)) * noise
    #mean_direction += noise_vector
    
    # Normalize the direction and set the velocity of each agent
    #norm = np.linalg.norm(mean_direction, axis=1)
    #norm[norm == 0] = 1  # Avoid division by zero
    #mean_direction /= norm[:, np.newaxis]
    #for i in range(len(mean_direction)):
        #if mean_direction[i][0] == 0 and mean_direction[i][1] == 0:
            #velocities[i]=velocities[i]
        #else:
            #velocities[i] = mean_direction[i] * speed
    
    return velocities
# Run the simulation and display the results
fig, (ax1,ax2,ax3) = plt.subplots(1,3)
disthist = np.zeros((time, num_agents))

def update_quiver(frame):
    global current_frame
    global box_size
    global num_agents
    global speed
    global noise
    global radius
    global const
    global mc
    global colors
    global social
    global vradius
    global positions
    global velocities
    current_frame=frame
    # Update the velocities of the agents
    



    velocities = update_velocities(positions, velocities, radius, speed, noise)
    
    # Update the positions of the agents
    #print(colors)

    for j in range(num_agents):
        current_state = mc[j].next_state()
        #print(current_state)
        if current_state == 'A':
            speed[j] = 0.05
            colors[j] = 'black'
            noise[j] = 0.005
            radius[j] = 4 * social[j]
            const = 8
        elif current_state == 'B':
            speed[j] = 0.05
            colors[j] = 'blue'
            noise[j] = 0.005
            radius[j] = 0.25 * social[j]
            const = 12
        else:
            speed[j] = 0.005
            colors[j] = 'grey'
            noise[j] = 0.0005
            radius[j] = 0
            const = 10
        a=10000; b=10000; c=10000; d=10000;
        if velocities[j][0]>0:
            a=(box_size-positions[j][0])/velocities[j][0]
        else:
            b=(0-positions[j][0])/velocities[j][0]

        if velocities[j][1]>0:
            c=(box_size-positions[j][1])/velocities[j][1]
        else:
            d=(0-positions[j][1])/velocities[j][1]
        #print(a,b,c,d)
        weight = 0
        if a<b and a<c and a<d:
            if a<0:
                a=0
            distance = a * speed[j] 
            #print(distance)
            disthist[current_frame][j]=distance

            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise[j]
                velocities[j][0]=(-1.*velocities[j,0])+veladj[0]
                velocities[j][1]+=veladj[1]
        elif b<c and b<d:
            if b<0:
                b=0

            distance = b * speed[j]
            disthist[current_frame][j]=distance

            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise[j]
                velocities[j][0]=(-1.*velocities[j,0])+veladj[0]
                velocities[j][1]+=veladj[1]
        elif c<d:
            if c<0:
                c=0
            distance = c * speed[j]
            
            disthist[current_frame][j]=distance
            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise[j]
                velocities[j][1]=(-1.*velocities[j,1])+veladj[0]
                velocities[j][0]+=veladj[1]
        else:
            if d<0:
                d=0
            distance = d * speed[j]
            disthist[current_frame][j]=distance
            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise[j]
                velocities[j][1]=(-1.*velocities[j,1])+veladj[0]
                velocities[j][0]+=veladj[1]
    
    positions += velocities
            
    #positions %= box_size
    cmap = plt.get_cmap('Blues')
    cols = cmap(social)
    # Plot the agents as arrows
    ax1.clear()
    ax1.quiver(positions[:, 0], positions[:, 1], velocities[:, 0], velocities[:, 1], color=cols,
              units='xy', scale=0.1, headwidth=10)
    ax1.set_xlim(0, box_size)
    ax1.set_ylim(0, box_size)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Position with Social')
    # Calculate the histogram using numpy
    counts, bins = np.histogram(disthist[current_frame], bins=[0,2,4,6,8,10,12])
    #print(disthist[i])
    # Convert counts to percentages
    total_data_points = len(disthist[current_frame])
    percentages = (counts / total_data_points)
    ax2.clear()
    # Plot the histogram
    ax2.bar(bins[:-1], percentages, width=np.diff(bins), align='edge')

# Add labels and title
    ax2.set_xlabel('Bins')
    ax2.set_ylabel('Percentage')
    ax2.set_title('Histogram with Y-axis as Percentage')
    ax2.set_xlim(0, box_size+4)
    ax2.set_ylim(0,1)
    ax3.clear()
    plotnormx = []
    plotnormy = []
    for k in range(num_agents):
        plotnormx.append(0.5*velocities[k,0]/speed[k])
        plotnormy.append(0.5*velocities[k,1]/speed[k])
    ax3.quiver(positions[:, 0], positions[:, 1], plotnormx, plotnormy, color=colors,
              units='xy', scale=1, headwidth=10)
    ax3.set_xlim(0, box_size)
    ax3.set_ylim(0, box_size)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_title('Position with State')
    plt.suptitle('Time = ' + str(current_frame))
    plt.draw()

update_quiver(current_frame)

# Function to handle the 'Next' button click event
def next_frame(event):
    global time
    global disthist
    global current_frame
    if current_frame-1 == time:
        time += 1
        disthist=np.append(disthist,np.zeros(num_agents))
    frame = (current_frame + 1)
    update_quiver(frame)

# Function to handle the 'Previous' button click event
def prev_frame(event):
    global current_frame
    frame = (current_frame - 1)
    update_quiver(frame)

# Create the quiver plot
def close_plot(event):
    plt.close()

def play_plot(event):
    global time
    global disthist
    global delt
    global current_frame
    if time - current_frame <= delt+1:
        size = delt-(time-current_frame)+1
        time += size
        for b in range(size):
            disthist=np.append(disthist, np.zeros(num_agents))
            print("added " + str(size))
    for a in range(delt):
        frame = (current_frame+1)
        update_quiver(frame)
        plt.pause(0.00001)

# Define the position and size of the buttons
button_next = plt.axes([0.81, 0.005, 0.1, 0.05])
button_prev = plt.axes([0.7, 0.005, 0.1, 0.05])
# Create the 'Close' button
button_close = plt.axes([0.59, 0.005, 0.1, 0.05])
button_play = plt.axes([0.48, 0.005, 0.1, 0.05])

button_close = Button(button_close, 'Close')
# Create the 'Next' and 'Previous' buttons
button_next = Button(button_next, 'Next')
button_prev = Button(button_prev, 'Previous')
button_play = Button(button_play, 'Play')
# Connect the button click events to their respective functions
button_next.on_clicked(next_frame)
button_prev.on_clicked(prev_frame)# Connect the button click event to the 'close_plot' function
button_close.on_clicked(close_plot)
button_play.on_clicked(play_plot)
plt.show()
#plt.show()
#plt.close()
#fig, ax = plt.subplots()


allbins = np.arange(0,14,0.5)
def remove_zeros(arr):
    return arr[arr != 0]
# Calculate the histogram using numpy
counts, bins = np.histogram(remove_zeros(disthist.flatten()), bins= allbins)

# Convert counts to percentages
#print(disthist.flatten())
total_data_points = len(disthist.flatten())
percentages = (counts / total_data_points)

# Plot the histogram
plt.bar(bins[:-1], percentages, width=np.diff(bins), align='edge')

# Add labels and title
plt.xlabel('Bins')
plt.ylabel('Percentage')
plt.title('Histogram with Y-axis as Percentage')
plt.xlim(0, box_size+4)
plt.show()
