import random

ideal_pit_lap = 20
pit_lap_SD = 3
laps = 50

cars = [
    {"name":"McLaren1", "initial_time": 90, "grid": 1, "inital_delta": 0, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"McLaren2","initial_time": 90, "grid": 2, "inital_delta": 0.2, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"Ferrari1","initial_time": 90, "grid": 3, "inital_delta": 0.4, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"Ferrari2","initial_time": 90, "grid": 4, "inital_delta": 0.6, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"Merc1","initial_time": 90, "grid": 5, "inital_delta": 0.8, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"Merc2","initial_time": 90, "grid": 6, "inital_delta": 1, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"RB1","initial_time": 90, "grid": 7, "inital_delta": 1.2, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
    {"name":"RB2","initial_time": 90, "grid": 1, "inital_delta": 1.4, "dirty_air": 0.15, "fuel_loss": 0.1, "compound": "Medium"},
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
    {"name":"hard", "initial_time": 100, "tyre_deg": 0.1, "dirty_air": 0.05,"fuel_loss": 0.1}
]    

def calc_lap_time( compounds, laps):
    
    initial_time = compounds["initial_time"]
    tyre_deg = compounds["tyre_deg"]
    fuel_loss = compounds["fuel_loss"]
    
    for lap in range(1,laps):
          lap_times = initial_time + (tyre_deg * lap) - (fuel_loss * lap)
    return lap_times

def pit_check(car, lap):
    pit_lap = car["pit_lap"]
    if lap > pit_lap:
        car["compound"] = "soft"
    return compounds[0]    




for lap in range(1, laps):
    for car in cars:
        active_compound = pit_check(car, lap)
        car["lap_time"] = calc_lap_time( active_compound, laps)

    calc_lap_time()