from .screen import Screen

class HomeScreen(Screen):
    def draw(self):
        application = self.get_application()
    
        image_x, image_y = self.get_position_by_percent(30, 0)
        image_width = application.width - image_x
        image_height = application.height

        background_filename = application.paths.get_random_image("background")
        image = self.load_image(background_filename, (image_width, image_height))

        image.blit(image_x, image_y)
