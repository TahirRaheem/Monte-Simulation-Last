import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit app title
st.title("Monte Carlo Simulation for Project Costs and Durations")

# Sidebar for user inputs
st.sidebar.header("Project Task Inputs")

# Ask user to input the number of tasks
num_tasks = st.sidebar.number_input("Enter the number of tasks in the project:", min_value=1, step=1, value=3)

# Empty list to store tasks
tasks = []

# Loop through the number of tasks to get user inputs
for i in range(num_tasks):
    st.sidebar.subheader(f"Task {i + 1}")
    
    mean_cost = st.sidebar.number_input(f"Enter mean cost for Task {i + 1}:", value=1000.0)
    std_cost = st.sidebar.number_input(f"Enter standard deviation for cost for Task {i + 1}:", value=100.0)
    
    mean_duration = st.sidebar.number_input(f"Enter mean duration for Task {i + 1} (days):", value=10.0)
    std_duration = st.sidebar.number_input(f"Enter standard deviation for duration for Task {i + 1} (days):", value=2.0)
    
    # Append each task as a tuple
    tasks.append((mean_cost, std_cost, mean_duration, std_duration))

# Number of simulations
num_simulations = st.sidebar.slider("Number of simulations:", min_value=100, max_value=5000, value=1000)

# Monte Carlo simulation button
if st.sidebar.button("Run Simulation"):
    
    # Arrays to store the total cost and duration from each simulation
    total_costs = np.zeros(num_simulations)
    total_durations = np.zeros(num_simulations)

    # Monte Carlo simulation
    for i in range(num_simulations):
        total_cost = 0
        total_duration = 0
        
        # Simulate each task's cost and duration
        for task in tasks:
            mean_cost, std_cost, mean_duration, std_duration = task
            
            # Sample from normal distribution for cost and duration
            simulated_cost = np.random.normal(mean_cost, std_cost)
            simulated_duration = np.random.normal(mean_duration, std_duration)
            
            # Accumulate total cost and duration
            total_cost += simulated_cost
            total_duration += simulated_duration
        
        # Store the total cost and duration for this simulation
        total_costs[i] = total_cost
        total_durations[i] = total_duration
    
    # Display summary statistics
    st.subheader("Simulation Results")
    st.write(f"Estimated Project Cost (Mean): {np.mean(total_costs):.2f}")
    st.write(f"Estimated Project Duration (Mean): {np.mean(total_durations):.2f} days")
    
    st.write(f"Cost 95% Confidence Interval: {np.percentile(total_costs, [2.5, 97.5])}")
    st.write(f"Duration 95% Confidence Interval: {np.percentile(total_durations, [2.5, 97.5])}")

    # Plot histograms of total costs and durations
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Total cost histogram
    ax[0].hist(total_costs, bins=30, color='skyblue', edgecolor='black')
    ax[0].set_title('Distribution of Total Project Costs')
    ax[0].set_xlabel('Total Cost')
    ax[0].set_ylabel('Frequency')

    # Total duration histogram
    ax[1].hist(total_durations, bins=30, color='lightgreen', edgecolor='black')
    ax[1].set_title('Distribution of Total Project Durations')
    ax[1].set_xlabel('Total Duration (days)')
    ax[1].set_ylabel('Frequency')

    st.pyplot(fig)

