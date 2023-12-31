import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Set up the simulation parameters
box_size = 10
num_agents = 20
speed = 0.05
noise = 0.001
radius = 2
time = 200
const = 10
social = []
for i in range(num_agents):
    social.append(np.random.rand())
# Set up the initial positions and velocities of the agents
positions = np.random.uniform(size=(num_agents, 2)) * box_size
velocities = np.random.uniform(size=(num_agents, 2)) * speed

# Define a function to update the velocities of the agents
def update_velocities(positions, velocities, radius, speed, noise):
    # Compute the distances between all pairs of agents
    distances = np.linalg.norm(positions[:, np.newaxis] - positions, axis=2)
    
    # Find the indices of the neighbors within the specified radius
    neighbors=[]
    # Find the indices of the neighbors within the specified radius
    for i in range(num_agents):
       tempneigh = np.argwhere(distances<radius*social[i])
       for j in tempneigh:
           if j[0]==i:
               neighbors.append(j)
    
    
    # Compute the average direction of the neighbors
    mean_direction = np.zeros((num_agents, 2))
    for i in range(num_agents):
        sum_direction = np.zeros(2)
        count = 0
        for j in neighbors:
            if j[0] == i:
                sum_direction += velocities[j[1]]
                count += 1
        if count > 0:
            mean_direction[i] = sum_direction / count
    
    # Add some random noise to the direction
    noise_vector = np.random.normal(size=(num_agents, 2)) * noise
    mean_direction += noise_vector
     # Normalize the direction and set the velocity of each agent
    norm = np.linalg.norm(mean_direction, axis=1)
    norm[norm == 0] = 1  # Avoid division by zero
    mean_direction /= norm[:, np.newaxis]
    for i in range(len(mean_direction)):
        if mean_direction[i][0] == 0 and mean_direction[i][1] == 0:
            velocities[i]+=noise_vector[i]
        else:
            velocities[i] = mean_direction[i] * speed + noise_vector[i]
    normv = np.linalg.norm(velocities, axis=1)
    normv[normv == 0] = 1  # Avoid division by zero
    for i in range(num_agents):
        velocities[i] = velocities[i]/normv[i] * speed
    # Normalize the direction and set the velocity of each agent
    #norm = np.linalg.norm(mean_direction, axis=1)
    #norm[norm == 0] = 1  # Avoid division by zero
    #mean_direction /= norm[:, np.newaxis]
    #for i in range(len(mean_direction)):
        #if mean_direction[i][0] == 0 and mean_direction[i][1] == 0:
            #velocities[i]=velocities[i]
        #else:
            #velocities[i] = mean_direction[i] * speed

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
fig, ax = plt.subplots()

randtime = random.randint(time/2,time)
disthist = np.zeros(num_agents)
for i in range(time):
    # Update the velocities of the agents
    velocities = update_velocities(positions, velocities, radius, speed, noise)
    
    # Update the positions of the agents


    for j in range(num_agents):
        a=10000; b=10000; c=10000; d=10000;
        if velocities[j][0]>0:
            a=(box_size-positions[j][0])/velocities[j][0]
        else:
            b=(0-positions[j][0])/velocities[j][0]

        if velocities[j][1]>0:
            c=(box_size-positions[j][1])/velocities[j][1]
        else:
            d=(0-positions[j][1])/velocities[j][1]
        weight = 0
        if a<b and a<c and a<d:
            if a<0:
                a=0
            distance = a * speed
            if i==randtime:
                disthist[j]=distance

            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise
                velocities[j][0]=-1*velocities[j][0]+veladj[0]
                velocities[j][1]+=veladj[1]
        elif b<c and b<d:
            if b<0:
                b=0
            distance = b * speed
            if i==randtime:
                disthist[j]=distance

            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise
                velocities[j][0]=-1*velocities[j][0]+veladj[0]
                velocities[j][1]+=veladj[1]
        elif c<d:
            if c<0:
                c=0
            distance = c * speed
            
            if i==randtime:
                disthist[j]=distance
            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise
                velocities[j][1]=-1*velocities[j][1]+veladj[0]
                velocities[j][0]+=veladj[1]
        else:
            if d<0:
                d=0
            distance = d * speed
            if i==randtime:
                disthist[j]=distance
            weight = math.exp(-const*distance/box_size)
            sample = [0, 1]
            randomval= random.choices(sample, weights=(weight, 1-weight), k=1)
            if randomval[0] == 0:
                veladj = np.random.normal(size=2) * noise
                velocities[j][1]=-1*velocities[j][1]+veladj[0]
                velocities[j][0]+=veladj[1]
    
    positions += velocities
            
    #positions %= box_size
    
    # Plot the agents as arrows
    ax.clear()
    cmap = plt.get_cmap('Blues')
    cols = cmap(social)
    ax.quiver(positions[:, 0], positions[:, 1], velocities[:, 0], velocities[:, 1], color=cols,
              units='xy', scale=0.1, headwidth=2)
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    plt.pause(0.01)

plt.show()
#plt.close()
#plt.hist(disthist, bins=10)
#plt.show()
