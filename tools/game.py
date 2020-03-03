import time
import amonome

# ------------------------------------------------------------------------
class Game:
# ------------------------------------------------------------------------

    # --------------------------------------------------------------------
    def __init__(self, width, height, port_a, port_b, frame_time):
        self.width = width
        self.height = height
        self.frame_time = frame_time
        self.s = amonome.Amonome(port_a, port_b)
        self.s.reset()
        self.screen = amonome.Screen(self.width, self.height)
        print("Surface on %s and %s initialized for frame time: %.3f" % (port_a, port_b, self.frame_time))

    # --------------------------------------------------------------------
    def event_process(self, e):
        print(e)

    # --------------------------------------------------------------------
    def logic_tick(self):
        print("=== TICK frame time: %.3f ===" % self.frame_time)

    # --------------------------------------------------------------------
    def game_over(self):
        print("GAME OVER")

    # --------------------------------------------------------------------
    def draw(self):
        print("draw")

    # --------------------------------------------------------------------
    def run(self):
        while True:
            res = self.logic_tick()

            self.screen.clear()
            self.draw()
            self.s.blit(self.screen)

            if res == False:
                self.game_over()
                break

            time.sleep(self.frame_time)

            e = self.s.read([amonome.GRID_EV_BDOWN])
            if e:
                self.event_process(e)


