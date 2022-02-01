import pandas as pd

def batter_output(data):
    
    result = []
    batter = [item["contents"]["away_batter"] for item in data]
    batter += [item["contents"]["home_batter"] for item in data]
    for item in batter:
        result += item
    
    return result

def batter_to_DataFrame(data):
    
    result = batter_output(data)
    result = pd.DataFrame(result)
    return result

def batter_to_Dict(data):
    
    result = batter_output(data)
    return result
