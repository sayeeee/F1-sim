
def calc_lap_times(compounds, laps):
    initial_time = compounds["initial_time"]
    tyre_deg = compounds["tyre_deg"]
    fuel_loss = compounds["fuel_loss"]
    total_lap_times = 0
    for lap in range(1,laps):
       total_lap_times += initial_time + (tyre_deg * lap) - (fuel_loss * lap)
    return total_lap_times

def calc_lap_times_2(compounds, laps, pit_stop_lap):
    initial_time = compounds["initial_time"]
    tyre_deg = compounds["tyre_deg"]
    fuel_loss = compounds["fuel_loss"]
    total_lap_times = 0
    for lap in range(1,laps):
       total_lap_times += initial_time + (tyre_deg * lap) - (fuel_loss * (lap+pit_stop_lap))
    return total_lap_times


def optimal_strat(laps,compounds):
    best_time = float('inf')
    best_strat = None

    for i in range(1,laps):
        for j in range(len(compounds)):
            for k in range(len(compounds)):
                lap_times1 = float('inf')
                lap_times2 = float('inf')
                if j != k:
                    comp1 = compounds[j]
                    comp2 = compounds[k]
                    

                    lap_times1 = calc_lap_times(comp1, i)
                    lap_times2 = calc_lap_times_2(comp2, laps - i, i)

                    tot_lap_time = lap_times1 + lap_times2

                    if tot_lap_time < best_time:
                       best_time = tot_lap_time
                       best_strat = (i,comp1["name"], comp2["name"] )

    return best_strat


compounds = [
    {"name":"soft", "initial_time": 90, "tyre_deg": 0.3, "dirty_air": 0.15, "fuel_loss": 0.1},
    {"name":"medium", "initial_time": 95, "tyre_deg": 0.2, "dirty_air": 0.1,"fuel_loss": 0.1},
    {"name":"hard", "initial_time": 100, "tyre_deg": 0.1, "dirty_air": 0.05,"fuel_loss": 0.1}
]
# add in tyre warm up for each tyre
laps = 50

result = optimal_strat(laps, compounds)
print(result)