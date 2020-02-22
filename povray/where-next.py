from vapory import Camera, Sphere, Texture, Scene, Pigment, LightSource, Background, Finish, Material
import random
import math


def distance(a, b):
    return math.sqrt(sum([(x[0] - x[1])**2 for x in zip(a, b)]))


def main():
    lookfrom = (13 / 1.5, 2 / 1.5, -5 / 1.5)
    lookat = (0, 0, 0)
    # dist_to_focus = 10.0
    # aperture = 0.1
    step = 1
    # camera
    camera = Camera('location', lookfrom, 'look_at', lookat)

    # background
    light = LightSource((0, 20, 0), 'color', (1, 1, 1))
    bg = Background('color', (0.5, 0.7, 1.0))
    base = Sphere((0, -1000, 0), 1000,
                  Texture(Pigment('color', (0.5, 0.5, 0.5))))
    htlist = [bg, base, light]
    for a in range(-11, 11, step):
        for b in range(-11, 11, step):
            choose_mat = random.random()
            center = (a + 0.9 * random.random(),
                      0.2, b + 0.9 * random.random())
            if distance(center, (4, 0.2, 0)) < 0.9:
                continue
            if choose_mat < 0.8:
                # diffuse
                color = (random.random() * random.random(),
                         random.random() * random.random(),
                         random.random() * random.random())
                htlist.append(
                    Sphere(center, 0.2, Texture(Finish('diffuse', 1), Pigment('color', color))))
            elif choose_mat < 0.95:
                # metal
                color = (0.5 * (1 + random.random()),
                         0.5 * (1 + random.random()),
                         0.5 * (1 + random.random()))
                # p1 = 0.5 * random.random()
                htlist.append(
                    Sphere(center, 0.2, Texture(Finish('Metal'), Pigment('color', color))))
            else:
                # glass
                htlist.append(Sphere(center, 0.2, Material('M_Glass')))

    # main 3 sphere
    htlist.append(
        Sphere((0, 1, 0), 1.0, Material('M_Glass')))
    htlist.append(
        Sphere((-4, 1, 0), 1.0, Texture(Finish('diffuse', 1), Pigment('color', (0.4, 0.2, 0.2)))))
    htlist.append(Sphere((4, 1, 0), 1.0, Texture('Chrome_Texture')))
    scene = Scene(camera, objects=htlist, included=[
                  'metals.inc', 'glass.inc', 'textures.inc', 'colors.inc'])
    with open("where-next.pov", "w") as ofp:
        print(str(scene), file=ofp)
    scene.render('where-next.png', width=800, height=600,
                 antialiasing=0.1, quality=10)


if __name__ == "__main__":
    main()
