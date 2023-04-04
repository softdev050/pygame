import pygame


image_path = "images/"
IMAGES = {
    "player" : {

        "idle" : [
            pygame.image.load(image_path + "player/idle0.png"),
            pygame.image.load(image_path + "player/idle1.png"),
            pygame.image.load(image_path + "player/idle2.png"),
            pygame.image.load(image_path + "player/idle3.png"),
        ],

        "run" : [
            pygame.image.load(image_path + "player/run1.png"),
            pygame.image.load(image_path + "player/run2.png"),
            pygame.image.load(image_path + "player/run3.png"),
            pygame.image.load(image_path + "player/run4.png"),
        ],

        "punch" : [
            pygame.image.load(image_path + "player/punch0.png"),
            pygame.image.load(image_path + "player/punch1.png"),
            pygame.image.load(image_path + "player/punch2.png"),
        ],
        "fall" : [
            pygame.image.load(image_path + "player/fall1.png"),
            pygame.image.load(image_path + "player/fall2.png"),
            pygame.image.load(image_path + "player/fall3.png"),
            pygame.image.load(image_path + "player/fall4.png"),
            pygame.image.load(image_path + "player/fall5.png"),
        ],
        "jump" : [
            pygame.image.load(image_path + "player/jump0.png"),
            pygame.image.load(image_path + "player/jump1.png"),
            pygame.image.load(image_path + "player/jump2.png"),
            pygame.image.load(image_path + "player/jump3.png"),
            pygame.image.load(image_path + "player/jump4.png"),
        ],
    }
}