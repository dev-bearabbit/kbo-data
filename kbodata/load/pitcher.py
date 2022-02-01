import pandas as pd

def pitcher_output(data):
    
    result = []
    pitcher = [item["contents"]["away_pitcher"] for item in data]
    pitcher += [item["contents"]["home_pitcher"] for item in data]
    for item in pitcher:
        result += item
    
    return result

def pitcher_to_DataFrame(data):

    result = pitcher_output(data)
    result = pd.DataFrame(result)
    return result

def pitcher_to_Dict(data):
    
    result = pitcher_output(data)
    return result
