class TimeManagement:
    def __init__(self):
        self.is_first_time = True
        self.start_time = 0
        self.game_time = 0

    def update_time(self, time):
        if self.is_first_time:
            self.is_first_time = False
            self.start_time = time

        self.game_time = time - self.start_time

    def get_game_time(self):
        return self.game_time
