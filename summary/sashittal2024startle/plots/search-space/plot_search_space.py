import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("../../csvs/search_space_size.csv")
cells = df['cells'].unique()
characters = df['characters'].unique()
reps = df['rep'].unique()

fig, ax = plt.subplots()
for cell in cells:
    search_space_sizes = []
    for character in characters:
        search_space_sizes.append(df[(df['cells'] == cell) & (df['characters'] == character)]['search_space_size'].mean())
    ax.plot(characters, search_space_sizes, marker='o', label='cells='+str(cell))


ax.set_xlabel('Number of characters')
ax.set_ylabel('Average search space size')
ax.legend()
plt.savefig('startle-sim-search-space.pdf', format='pdf',dpi=300)