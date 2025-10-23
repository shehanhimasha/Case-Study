# ============================================================
# Simulation: Call Center Performance
#
#   This Python simulation models a call center with multiple
#   agents (servers). Calls arrive randomly and are served one
#   at a time. If all agents are busy, calls wait in queue.
# ============================================================

import random           # generating random arrivals and service times
import matplotlib.pyplot as plt  # plotting graphs
import statistics       # calculating averages

# -----------------------------
# Utility: Generate exponential times
# -----------------------------
def exponential(mean):
    
    return random.expovariate(1.0 / mean)

# -----------------------------
# Event-driven simulation
# -----------------------------
def simulate_call_center(arrival_rate, service_rate, num_agents, sim_time=1000):
    """
    Simulate a call center using an M/M/c model.
    :param arrival_rate: average number of arrivals per minute 
    :param service_rate: average number of services per minute per agent
    :param num_agents: number of agents (servers)
    :param sim_time: total simulation time (minutes)
    :return: metrics dict
    """
    # Initialize system state
    clock = 0
    queue = []
    agents_busy = 0
    next_arrival = exponential(1 / arrival_rate)
    next_departures = []

    wait_times = []
    busy_time = 0
    time_points = []
    queue_lengths = []

    while clock < sim_time:
        # Determine next event (arrival or earliest departure)
        next_departure = min(next_departures) if next_departures else float('inf')
        next_event_time = min(next_arrival, next_departure)
        dt = next_event_time - clock
        busy_time += agents_busy * dt
        clock = next_event_time

        # Record queue length
        time_points.append(clock)
        queue_lengths.append(len(queue))

        # Handle event
        if next_arrival <= next_departure:
            # ARRIVAL
            if agents_busy < num_agents:
                agents_busy += 1
                service_time = exponential(1 / service_rate)
                next_departures.append(clock + service_time)
                wait_times.append(0)
            else:
                queue.append(clock)
            next_arrival = clock + exponential(1 / arrival_rate)
        else:
            # DEPARTURE
            next_departures.remove(next_departure)
            if queue:
                arrival_time = queue.pop(0)
                wait = clock - arrival_time
                wait_times.append(wait)
                service_time = exponential(1 / service_rate)
                next_departures.append(clock + service_time)
            else:
                agents_busy -= 1

    # Compute metrics
    avg_wait = statistics.mean(wait_times) if wait_times else 0
    avg_queue_len = statistics.mean(queue_lengths)
    utilization = busy_time / (sim_time * num_agents)
    throughput = len(wait_times) / sim_time

    return {
        "agents": num_agents,
        "avg_wait": avg_wait,
        "avg_queue_len": avg_queue_len,
        "utilization": utilization,
        "throughput": throughput,
        "time_points": time_points,
        "queue_lengths": queue_lengths,
    }

# -----------------------------
# Run Simulation for 3 Scenarios
# -----------------------------
random.seed(42)  # reproducibility

scenarios = [
    {"agents": 2, "arrival_rate": 5, "service_rate": 3},
    {"agents": 3, "arrival_rate": 5, "service_rate": 3},
    {"agents": 5, "arrival_rate": 5, "service_rate": 3},
]

results = []
for s in scenarios:
    r = simulate_call_center(
        arrival_rate=s["arrival_rate"],
        service_rate=s["service_rate"],
        num_agents=s["agents"],
        sim_time=1000
    )
    results.append(r)
    print(f"--- Scenario: {s['agents']} Agents ---")
    print(f"Avg Wait Time: {r['avg_wait']:.2f} min")
    print(f"Avg Queue Length: {r['avg_queue_len']:.2f}")
    print(f"Utilization: {r['utilization']*100:.1f}%")
    print(f"Throughput: {r['throughput']:.2f} calls/min\n")

# -----------------------------
# Visualization 1: Queue Length over Time
# -----------------------------
plt.figure()
for r in results:
    plt.plot(r["time_points"], r["queue_lengths"], label=f"{r['agents']} Agents")
plt.xlabel("Time (min)")
plt.ylabel("Queue Length")
plt.title("Queue Length Over Time")
plt.legend()
plt.grid(True)
plt.show()


# -----------------------------
# Visualization 2: Average Waiting Time Comparison
# -----------------------------
plt.figure()
plt.bar(
    [r["agents"] for r in results],
    [r["avg_wait"] for r in results]
)
plt.xlabel("Number of Agents")
plt.ylabel("Average Wait Time (min)")
plt.title("Average Wait Time vs. Number of Agents")
plt.grid(True)
plt.show()


# -----------------------------
# Visualization 3: Agent Utilization Comparison
# -----------------------------
plt.figure()
plt.bar(
    [r["agents"] for r in results],
    [r["utilization"] * 100 for r in results]
)
plt.xlabel("Number of Agents")
plt.ylabel("Utilization (%)")
plt.title("Agent Utilization vs. Number of Agents")
plt.grid(True)
plt.show()


