from client.beagle.beagle_api import api as bgl

class pulse_emitter():
    driver_rate = 1.0 / 60.0
    
    def __init__(self, **kwargs):
        self.t = 0
        self.x = self.base_x = kwargs['x']
        self.y = self.base_y = kwargs['y']
        self.rate = kwargs['rate']
        self.start = kwargs['start']
        self.ramp_speed = kwargs['ramp_speed']
        self.template = kwargs['template']
        self.ramp = 0.0
        self.driver = bgl.curve_driver( curve = bgl.assets.get("emitter_paths/curve/" + kwargs["driver"]), rate = pulse_emitter.driver_rate )

    def emit(self):
        self.template(self)

    def tick(self):
        self.t = self.t + self.rate

        if(self.driver.is_finished()):
            return False

        if(self.t > self.start):
            self.driver.tick()
            p = self.driver.value()
            self.x = self.base_x + p[0]
            self.y = self.base_y + p[1]

            self.ramp = self.ramp + self.ramp_speed
            if self.ramp > 1.0:
                self.ramp = 0.0
                self.emit()

        return True
