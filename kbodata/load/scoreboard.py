import pandas as pd

def scoreboard_output(data):
    
    scoreboard = [item["contents"]["scoreboard"] for item in data]
    result = []
    for item in scoreboard:
        result.append(item[0])
        result.append(item[1])
    
    return result

def scoreboard_to_DataFrame(data):
    
    result = scoreboard_output(data)
    result = pd.DataFrame(result)
    return result

def scoreboard_to_Dict(data):

    result = scoreboard_output(data)
    return result
