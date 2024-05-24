import numpy as np

scooter, car, truck = 2000 , 4000 , 6000 #given

total = car + scooter + truck

p_scooter = scooter/total
p_car = car/total
p_truck = truck/total

p_acc_scooter , p_acc_car , p_acc_truck = 0.01, 0.03, 0.15

size = 100000

#to find no. of insured drivers simulated
sim_scooter = 0
sim_car = 0
sim_truck = 0

# Let X be a random variable representing insured users
#X = 1 -> insured scooter drivers
#X = 2 -> insured car drivers
#X = 3 -> insured truck drivers
for i in range(size):
  X = np.random.choice([1,2,3] , p = [p_scooter , p_car , p_truck])
  if X == 1:
    sim_scooter+=1
  if X == 2:
    sim_car+=1
  if X == 3:
    sim_truck+=1


#to simulate the no. of drivers involved in accident

#Let Y be a random variable representing users involved in accidents
#Y = 0 -> driver is involved in accident
#Y = 1 -> driver is not involved in accident

sim_acc_scooter , sim_acc_car , sim_acc_truck = 0,0,0

for i in range(sim_scooter):
  Y = np.random.choice([0,1] , p =[p_acc_scooter , 1-p_acc_scooter])
  if Y==0:
    sim_acc_scooter+=1

for i in range(sim_car):
  Y = np.random.choice([0,1] , p =[p_acc_car , 1-p_acc_car])
  if Y==0:
    sim_acc_car+=1

for i in range(sim_truck):
  Y = np.random.choice([0,1] , p =[p_acc_truck , 1-p_acc_truck])
  if Y==0:
    sim_acc_truck+=1

#probability that scooter driver was involved in accident 
# = simulated scooter drivers involved in accident /simulated total drivers involved in accident

sim_prob_acc_scooter = sim_acc_scooter / (sim_acc_scooter + sim_acc_car + sim_acc_truck)

#actual probability that scooter driver was involved in accident (by Bayes Theorem)
# = P(accident|scooter)P(scooter)/ (P(accident|scooter)P(scooter) + P(accident|car)P(car) + P(accident|truck)P(truck))

prob_acc_scooter = (p_scooter * p_acc_scooter) / ((p_scooter * p_acc_scooter) + (p_car * p_acc_car) + (p_truck * p_acc_truck))

print("The simulated probability is: ", sim_prob_acc_scooter)
print("The theoretical probability is : ", prob_acc_scooter)



