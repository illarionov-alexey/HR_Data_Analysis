import pandas as pd

t_t_t = pd.DataFrame({
    "tick": ["X", "O", 'O'], 
    "tack": ["O", "O", 'X'], 
    "toe": ["O", "X", 'O'],
}, index=['tick', 'tack', 'toe'])

# your code here
print(t_t_t.reindex(sorted(t_t_t.columns),axis='columns').sort_index())