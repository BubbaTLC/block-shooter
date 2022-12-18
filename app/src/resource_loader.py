import pyglet


def center_image(image: pyglet.resource.image) -> None:
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# Tell pyglet where to find the resources
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

# Load player assets
player_image: pyglet.resource.image = pyglet.resource.image("player.png")
center_image(player_image)

# Load bullet assets
bullet_image: pyglet.resource.image = pyglet.resource.image("bullet.png")
center_image(bullet_image)

# Load enemy assets
enemy_image: pyglet.resource.image = pyglet.resource.image("asteroid.png")
center_image(enemy_image)
