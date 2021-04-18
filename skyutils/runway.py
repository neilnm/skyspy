class Runway:
    def __init__(self, number):
        self.number = number
        self.reverse = self.get_reverse(number)
        self.min_wind = self.get_min_wind(number)
        self.max_wind = self.get_max_wind(number)

    def get_reverse(self, number):
        if (self.number + 18) > 36:
            return self.number - 18
        else:
            return self.number + 18

    def get_min_wind(self, number):
        num = number * 10
        if (num - 90) < 0:
            return num + 270
        else:
            return num - 90

    def get_max_wind(self, number):
        num = number * 10
        if (num - 90) < 0:
            return num + 450
        else:
            return num + 90

    def is_usable(self, wind):
        return (self.min_wind <= wind <= self.max_wind or
                self.min_wind <= (wind + 360) <= self.max_wind)

    def runway_for_wind(self, wind):
        # TODO
        # if 90degree crosswind, both runways are valid.
        # currently returns the one in cfg by default.
        if self.is_usable(wind):
            return self.number
        else:
            return self.reverse
