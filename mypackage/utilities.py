from PIL import Image
from pygame import image, transform, mixer



class ImageHandler:
    def __init__(self) -> None:
        self.__ship_1 = Image.open("../static/assets/images/spiked_ship_3_small_blue.PNG")
        self.__ship_2 = Image.open("../static/assets/images/spiked_ship_3_red.PNG")
        self.__ship_3 = Image.open("../static/assets/images/spiked_ship_3_small_green.PNG")
        self.__background = Image.open("../static/assets/images/space_2.jpg")
        self.__energy_ball = Image.open("../static/assets/images/energy_ball.png")
        self.ship_size = (50, 50)
        self.screen_size = (1000, 555)
        self.ball_size = (50, 50)


    def get_background(self):
        return transform.scale(self.pil_to_surface(self.__background), self.screen_size)

    def get_ship_1(self, degree=0):
        return transform.rotate(transform.scale(self.pil_to_surface(self.__ship_1), self.ship_size), degree)

    def get_ship_2(self, degree=0):
        return transform.rotate(transform.scale(self.pil_to_surface(self.__ship_2), self.ship_size), degree)

    def get_ship_3(self, degree=0):
        return transform.rotate(transform.scale(self.pil_to_surface(self.__ship_3), self.ship_size), degree)

    def get_energy_ball(self):
        return transform.scale(self.pil_to_surface(self.__energy_ball), self.ball_size)

    def pil_to_surface(self, pil_image):
        """Convert a PILLOW image to a Pygame surface."""
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        surface = image.fromstring(data, size, mode)
        return surface

class SFXHandler:
    def __init__(self) -> None:
        self.__energy_ball_sound = mixer.Sound("../static/assets/sfx/energy_ball_sound.wav")
        self.__ship_hit_sound = mixer.Sound("../static/assets/sfx/ship_hit_sound.wav")

    def play_energy_ball_sound(self):
        self.__energy_ball_sound.play()

    def play_ship_hit_sound(self):
        self.__ship_hit_sound.play()

