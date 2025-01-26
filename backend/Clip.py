class Clip:
    def __init__(self, start_time, end_time, chunk, player_first, player_last):
        self.path = ""
        self.category = ""
        self.start_time = start_time
        self.end_time = end_time
        self.chunk = chunk
        self.player_first = player_first
        self.player_last = player_last
        self.excitement = 0
    
