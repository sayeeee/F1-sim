import random

ideal_pit_lap = 20
pit_lap_SD = 3
laps = 50

Strategy = ["Medium", "Soft"]

cars = [
        {"name":"McLaren1", "initial_time": 90, "grid": 1, "total_time": 0, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium", "current_tyre_deg" : 0 , "overtake_%": 0.01 },
        {"name":"McLaren2","initial_time": 90, "grid": 2, "total_time": 0.2, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium", "current_tyre_deg" : 0, "overtake_%": 0.01 },
        {"name":"Ferrari1","initial_time": 90, "grid": 3, "total_time": 0.4, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium", "current_tyre_deg" : 0, "overtake_%": 0.01 },
        {"name":"Ferrari2","initial_time": 90, "grid": 4, "total_time": 0.6, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium", "current_tyre_deg" : 0, "overtake_%": 0.01 },
        {"name":"Merc1","initial_time": 90, "grid": 5, "total_time": 0.8, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium", "current_tyre_deg" : 0, "overtake_%": 0.01 },
        {"name":"Merc2","initial_time": 90, "grid": 6, "total_time": 1, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium",  "current_tyre_deg" : 0, "overtake_%": 0.01},
        {"name":"RB1","initial_time": 90, "grid": 7, "total_time": 1.2, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium",  "current_tyre_deg" : 0, "overtake_%": 0.01 },
        {"name":"RB2","initial_time": 90, "grid": 8, "total_time": 1.4, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium",  "current_tyre_deg" : 0, "overtake_%": 0.01},
    ]

positions = [
    1,2,3,4,5,6,7,8
    
]


for car in cars:
        # Generate a pit lap from a normal distribution
        raw_pit_lap = random.gauss(ideal_pit_lap, pit_lap_SD)

        # Ensure pit lap is an integer and within laps of the race
        car_pit_lap = max(1, min(laps - 1, round(raw_pit_lap)))

        car["pit_lap"] = car_pit_lap

for car in cars:
    print(f"{car['name']}: Pit Lap = {car['pit_lap']}")

compounds = [
{"name":"soft", "initial_time": 90, "tyre_deg": 0.3, "dirty_air": 0.15, "fuel_loss": 0.1},
{"name":"medium", "initial_time": 95, "tyre_deg": 0.2, "dirty_air": 0.1,"fuel_loss": 0.1},
{"name":"hard", "initial_time": 100, "tyre_deg": 0.1, "dirty_air": 0.05,"fuel_loss": 0.1}]    

def calc_lap_time( car,compounds, lap, pit_confirm):

    initial_time = compounds["initial_time"]
    tyre_deg = compounds["tyre_deg"]
    fuel_loss = compounds["fuel_loss"]
    current_tyre_deg = car["current_tyre_deg"]

    

    if pit_confirm == 0:
        lap_time = initial_time + (tyre_deg * lap) - (fuel_loss * lap) + current_tyre_deg
    else:
        lap_time = initial_time + (tyre_deg * (lap-car["pit_lap"])) - (fuel_loss * lap) + current_tyre_deg
    return lap_time

def pit_check(car, lap, compounds):
    pit_lap = car["pit_lap"]
    if lap > pit_lap:
        car["compound"] = "soft" #make this strategy[1] to soft code
        car["current_tyre_deg"] = 0
        return [compounds[0], 1]    
    else:
        return [compounds[1], 0]

def check_overtakes(cars):
    cars.sort(key=lambda car: car["total_time"])
    for i in range(len(cars)):
        current_car = cars[i]
        position = i+1
          
        current_car["position"] = position #car[1] = position

#depending on how i code this we may get multiple overtakes in 1 lap
        overtake_probability = 0
        if i > 0:
            car_in_front = cars[i-1]
            delta = current_car["total_time"] - car_in_front["total_time"]
             # add probability by laps and stuff in if statement
            if delta <= 0.1:
                current_car["current_tyre_deg"] += current_car["compound"]["dirty_air"]
                current_car["overtake_%"] = 0.4
                
            if delta <= 1: #DRS zone
             current_car["current_tyre_deg"] += current_car["compound"]["dirty_air"]
             current_car["overtake_%"] = 0.18
            elif delta > 1 and delta <= 3:
                current_car["current_tyre_deg"] += current_car["compound"]["dirty_air"]
                current_car["overtake_%"] = 0.02
            else:
               current_car["overtake_%"] = 0
            
        if current_car["overtake_%"] > 0:
            if random.random() <= overtake_probability:
                # Overtake is successful!
                print(f"OVERTAKE! {current_car['name']} ({current_car['position']}) "
                      f"overtakes {cars[i-1]['name']} ({cars[i-1]['position']})!")

                # Swap the cars in the list
                cars[i], cars[i-1] = cars[i-1], cars[i]

                # Now update their positions
                cars[i-1]["position"] = i
                cars[i]["position"] = i + 1

 
def print_race_standings():
    # Make sure to sort the cars by total_time just before printing
    # to get the final positions for the lap. The check_overtakes function
    # should ideally do this, but a final sort here is good practice.
    cars.sort(key=lambda car: car["total_time"])

    print("Race Standings:")
    for i, car in enumerate(cars):
        print(f"P{i+1}: {car['name']} - Total Time: {car['total_time']:.2f}s")
        # You could also print lap time, position, etc.


def run_sim(cars, compounds,laps, Strategy):
    for lap in range(1, laps):
        for car in cars:
            [car["compound"],pit_confirm] = pit_check(car, lap, compounds)
            car["lap_time"] = calc_lap_time( car, car["compound"], lap, pit_confirm)
            car["total_time"] += car["lap_time"] # add line of code so total time can't be lower than car ahead of it

        for i in range(len(cars)-1):
            
            if cars[i +1]["total_time"] < cars[i]["total_time"]:
                cars[i +1]["total_time"] = cars[i]["total_time"] + 0.1
               
                
        check_overtakes(cars)        
                
        print_race_standings()
            

        
        #for car in cars:
            # now comparing each cars lap time to see who is close to each other and if overtakes are possible



sim = run_sim(cars, compounds, laps, Strategy)
print(sim)