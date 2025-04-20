import traci
import pandas as pd

traci.start(["sumo", "-c", "sumo_simulation/simulation.sumocfg"])

vehicle_data = []

for step in range(1000):
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    
    for v in vehicles:
        speed = traci.vehicle.getSpeed(v)
        pos = traci.vehicle.getPosition(v)
        vehicle_data.append([v, speed, pos])

traci.close()

df = pd.DataFrame(vehicle_data, columns=["Vehicle_ID", "Speed", "Position"])
df.to_csv("sumo_simulation/vehicle_data.csv", index=False)

