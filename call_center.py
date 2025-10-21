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

