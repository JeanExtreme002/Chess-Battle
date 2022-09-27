from .screen import Screen
from pyglet import shapes
from pyglet import sprite
from pyglet import graphics

class HomeScreen(Screen):
    def draw(self):
        application = self.get_application()
        batch = graphics.Batch()

        background_x, background_y = self.get_pixels_by_percent(25, 0)
        background_width = application.width - background_x
        background_height = application.height

        logo_width = self.get_pixels_by_percent(10, 0)[0]
        logo_height = logo_width

        shape = shapes.Rectangle(0, 0, background_x - 2, application.height, color = (30, 30, 80), batch = batch)

        logo_filename = application.paths.get_image("home_logo.png")
        logo_image = self.load_image(logo_filename, (logo_width, logo_height))
        
        logo_sprite = sprite.Sprite(
            logo_image,
            int(background_x / 2 - logo_width / 2),
            application.height - logo_height // 2 - 100,
            batch = batch
            )
        
        background_filename = application.paths.get_random_image("background")
        background_image = self.load_image(background_filename, (background_width, background_height))

        background_image.blit(background_x, background_y)
        batch.draw()
