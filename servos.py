# Servo class


class Servo(object):
    def __init__(
        self,
        servoblaster_fd,
        pin,
        position_range,
        angle_range,
    ):
        self.sb_fd = servoblaster_fd
        self.pin = str(pin)
        self.position_range = position_range
        self.angle_range = angle_range

        self._position = None
        self.reset()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        pos = int(pos)
        if pos > self.position_range[1] or pos < self.position_range[0]:
            raise Exception("%d out of range [%d, %d]" % (pos, self.position_range[0], self.position_range[1]))
        self._position = pos
        print "%s=%d%%\n" % (self.pin, self._position)
        self.sb_fd.write("%s=%d%%\n" % (self.pin, self._position))
        self.sb_fd.flush()

    @property
    def percent_position(self):
        position_percentage = (self.position - self.position_range[0] + 0.0) / (self.position_range[1] - self.position_range[0])
        return int(position_percentage * 100)

    @percent_position.setter
    def percent_position(self, percent):
        percent = percent / 100.0
        if percent > 100 or percent < 0:
            raise Exception("%d out of range [0, 100]" % (percent,))
        self.position = (self.position_range[1] - self.position_range[0]) * percent + self.position_range[0]

    @property
    def angle_position(self):
        angle = (self.angle_range[1] - self.angle_range[0]) * self.percent_position + self.angle_range[0]
        return angle

    @angle_position.setter
    def angle_position(self, angle):
        angle_percentage = (angle - self.angle_range[0] + 0.0) / (self.angle_range[1] - self.angle_range[0])
        position = (self.position_range[1] - self.position_range[0]) * angle_percentage + self.position_range[0]
        self.position = position

    def reset(self):
        self.position = (self.position_range[1] - self.position_range[0]) / 2 + self.position_range[0]

    def stop(self):
        self.sb_fd.write("%s=0\n" % (self.pin,))
        self.sb_fd.flush()
