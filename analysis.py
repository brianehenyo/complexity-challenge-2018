import pandas as pd
import numpy as np

expruns = pd.read_json("experiments/runs_122-1417.json", orient='records')
print(expruns)