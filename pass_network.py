from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

# Load events
events = sb.events(match_id=3895232)

# Filter Leverkusen passes, first half, successful only
passes = events[
    (events['type'] == 'Pass') &
    (events['team'] == 'Bayer Leverkusen') &
    (events['period'] == 1) &
    (events['pass_outcome'].isna())
].copy()

# Extract coordinates
passes['x'] = passes['location'].apply(lambda loc: loc[0])
passes['y'] = passes['location'].apply(lambda loc: loc[1])
passes['end_x'] = passes['pass_end_location'].apply(lambda loc: loc[0])
passes['end_y'] = passes['pass_end_location'].apply(lambda loc: loc[1])

# Average position per player
avg_pos = passes.groupby('player')[['x', 'y']].mean()
pass_counts = passes.groupby('player').size().reset_index(name='count')

# Count passes between each pair of players
combos = passes.groupby(['player', 'pass_recipient']).size().reset_index(name='passes')
combos = combos[combos['passes'] >= 3]

# Draw pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a2e', line_color='white')
fig, ax = pitch.draw(figsize=(14, 9))
fig.patch.set_facecolor('#1a1a2e')

# Draw pass lines
for _, row in combos.iterrows():
    if row['player'] in avg_pos.index and row['pass_recipient'] in avg_pos.index:
        x_start = avg_pos.loc[row['player'], 'x']
        y_start = avg_pos.loc[row['player'], 'y']
        x_end = avg_pos.loc[row['pass_recipient'], 'x']
        y_end = avg_pos.loc[row['pass_recipient'], 'y']
        pitch.lines(x_start, y_start, x_end, y_end,
                    lw=row['passes'] * 0.8,
                    color='#a8dadc', alpha=0.6, ax=ax, zorder=2)

# Draw player nodes
for player, row in avg_pos.iterrows():
    count = pass_counts[pass_counts['player'] == player]['count'].values[0]
    pitch.scatter(row['x'], row['y'], ax=ax,
                  s=count * 25, color='#e63946',
                  edgecolors='white', linewidth=1.5, zorder=3)
    short_name = player.split()[-1]
    ax.text(row['x'], row['y'] - 4, short_name,
            color='white', fontsize=7, ha='center', zorder=4)

# Title
ax.set_title('Bayer Leverkusen — Pass Network\nvs Bayern Munich | Bundesliga 2023/24 | First Half',
             color='white', fontsize=13, fontweight='bold', pad=15)

ax.text(0.01, 0.02, 'Node size = total passes · Line thickness = passes between players · Min. 3 passes shown',
        transform=ax.transAxes, color='white', fontsize=8, alpha=0.6)

plt.tight_layout()
plt.savefig('/Users/chriszaimi/Desktop/pass_network_leverkusen.png', dpi=150, bbox_inches='tight')
plt.show()
print("Pass network saved!")