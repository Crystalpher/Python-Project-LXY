# Define a class about a position's CO condition
class Position:
    def __init__(self,position_name,aqi,co,co_24h):
        self.position_name = position_name
        self.aqi = aqi
        self.co = co
        self.co_24h = co_24h
    # Define a function to judge if this position is livable
    def judge_livable(self):
        if self.aqi<=75:
            return "livable"
        elif self.aqi<=300:
            return "unhealthy"
        else:
            return "dangerous"
    # Define a function to suggest which protection should be done
    def protection(self):
        if self.co<=1.0:
            return "none"
        elif self.co<=3.0:
            return "mask"
        else:
            return "indoor"
    # Define a function to judge if a position should be stayed long in
    def judge_stay(self):
        if self.co_24h<=0.5:
            return "stay"
        elif self.co_24h<=1.0:
            return "consider"
        else:
            return "leave"