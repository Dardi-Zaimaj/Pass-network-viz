# Bayer Leverkusen — Pass Network
## Bundesliga 2023/24 | vs Bayern Munich | First Half

Pass network analysis using StatsBomb open data to visualise 
Leverkusen's passing structure and player connections.

---

## Visualisation

![Pass Network](pass_network_leverkusen.png)

- Node size = total passes by player
- Line thickness = passes between two players
- Minimum 3 passes shown

**Key insight:** Granit Xhaka was the central hub with 36 passes, 
connecting defence and attack. Florian Wirtz positioned highest, 
acting as the creative outlet in the final third. Tella and 
Stanišić on the right were isolated wide outlets, rarely 
involved in central combinations.

---

## Tools & Data

- **Data:** StatsBomb open data (free)
- **Language:** Python 3.12
- **Libraries:** `statsbombpy`, `mplsoccer`, `matplotlib`, `pandas`

---

## How to run

```bash
pip install statsbombpy mplsoccer matplotlib pandas
python3 pass_network.py
```
