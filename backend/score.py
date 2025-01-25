'''
Shot clock, quarter, score, time remaining

Weights:
40% - Score
30% - Quarter
20% - Time remaining 
10% - Shot clock

'''

def score(quarter, team_a_score, team_b_score, time_remaining, shot_clock):
    SCORE_WEIGHT = 0.4
    QUARTER_WEIGHT = 0.3
    TIME_REMAINING_WEIGHT = 0.2
    SHOT_CLOCK_WEIGHT = 0.1
    
    MAX_GAP = 30
    
    difference = abs(team_a_score - team_b_score) 
    unscaled = 1-min(difference/MAX_GAP, 1)
    total = team_a_score + team_b_score
    scaling_factor = total/200
    
    score_factor = min(unscaled * scaling_factor,1)
    quarter_factor = quarter/4
    time_remaining_factor = 1 - time_remaining/720
    
    if shot_clock < 5:
        shot_clock_factor = min((1-shot_clock/5)**2 + 0.9, 1)
    else:
        shot_clock_factor = 0.333*(1-shot_clock/24)
        
    return SCORE_WEIGHT*score_factor + QUARTER_WEIGHT*quarter_factor + TIME_REMAINING_WEIGHT*time_remaining_factor + SHOT_CLOCK_WEIGHT*shot_clock_factor

    
# Example 1: Close game in the 4th quarter, low shot clock
print(score(quarter=4, team_a_score=110, team_b_score=108, time_remaining=60, shot_clock=2))

# Example 2: Moderate game in the 3rd quarter, mid shot clock
print(score(quarter=3, team_a_score=80, team_b_score=70, time_remaining=300, shot_clock=10))

# Example 3: Low-scoring blowout in the 1st quarter
print(score(quarter=1, team_a_score=20, team_b_score=5, time_remaining=600, shot_clock=20))

# Example 4: High-scoring close game in the 2nd quarter, critical shot clock
print(score(quarter=2, team_a_score=95, team_b_score=93, time_remaining=480, shot_clock=4))

# Example 5: Low-stakes game in the 2nd quarter, long shot clock
print(score(quarter=2, team_a_score=40, team_b_score=30, time_remaining=600, shot_clock=18))

 