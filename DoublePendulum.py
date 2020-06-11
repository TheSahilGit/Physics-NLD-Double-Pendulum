"""Double Pendulum simulation"""

### Sahil Islam ###
### 10/06/2020 ###

import matplotlib.pyplot as plt
import numpy as np
import pygame

l1 = 1.
l2 = 1.
m1 = 2.
m2 = 2.

g = 9.80


def f1(theta1, theta2, w1, w2):
    nu1 = -g * (2 * m1 + m2) * np.sin(theta1)
    nu2 = -m2 * g * np.sin(theta1 - 2 * theta2)
    nu3 = -2 * np.sin(theta1 - theta2) * m2
    nu4 = w2 * w2 * l2 + w1 * w1 * l1 * np.cos(theta1 - theta2)
    de = l1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2))
    nu = nu1 + nu2 + nu3 * nu4
    return float(nu / de)


def f2(theta1, theta2, w1, w2):
    nu1 = 2 * np.sin(theta1 - theta2)
    nu2 = w1 * w1 * l1 * (m1 + m2)
    nu3 = g * (m1 + m2) * np.cos(theta1)
    nu4 = w2 * w2 * l2 * m2 * np.cos(theta1 - theta2)
    de = l2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2))
    nu = nu1 * (nu2 + nu3 + nu4)
    return float(nu / de)


def EulerLoop(theta1, theta2, w1, w2):
    t = 0
    theta1s = []
    theta2s = []
    w1s = []
    w2s = []
    time = []
    step = 10000
    h = 0.01
    for i in range(step):
        w1 += h * f1(theta1, theta2, w1, w2)
        theta1 += h * w1
        w2 += h * f2(theta1, theta2, w1, w2)
        theta2 += h * w2
        t += h

        theta1s.append(theta1)
        theta2s.append(theta2)
        w1s.append(w1)
        w2s.append(w2)
        time.append(t)
    return theta1s, theta2s, w1s, w2s, time


def plotLoop1(theta1, theta2, w1, w2):
    theta1s, theta2s, w1s, w2s, time = EulerLoop(theta1, theta2, w1, w2)

    plt.subplot(2, 2, 1)
    plt.plot(time, theta1s)
    plt.title("theta1")

    plt.subplot(2, 2, 2)
    plt.plot(time, theta2s)
    plt.title("theta2")

    plt.subplot(2, 2, 3)
    plt.plot(time, w1s)
    plt.title("w1")

    plt.subplot(2, 2, 4)
    plt.plot(time, w2s)
    plt.title("w2")

    plt.show()


def plotLoop2(theta1, theta2, w1, w2):
    theta1s, theta2s, w1s, w2s, time = EulerLoop(theta1, theta2, w1, w2)

    plt.subplot(2, 2, 1)
    plt.plot(theta1s, theta2s)
    plt.title("theta1-theta2")

    plt.subplot(2, 2, 2)
    plt.plot(w1s, w2s)
    plt.title("w1-w2")

    plt.subplot(2, 2, 3)
    plt.plot(theta1s, w1s)
    plt.title("theta1-w1")

    plt.subplot(2, 2, 4)
    plt.plot(theta2s, w2s)
    plt.title("theta2-w2")

    plt.show()


def visual(theta1, theta2, w1, w2):
    pygame.init()

    width = 1200
    height = 650

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    red2 = (255, 80, 80)
    black2 = (100, 100, 100)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    clock = pygame.time.Clock()

    scale = 100
    xo = width / 2.
    yo = height / 2.

    ballSizeScale = 4

    screen = pygame.display.set_mode((width, height))
    surface = pygame.Surface((width, height))
    surface.fill(white)

    def ball(x, y, r, color):
        pygame.draw.circle(screen, color, (int(x), int(y)), int(r))

    def line(x1, y1, x2, y2):
        pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)

    def point(x, y, color):
        pygame.draw.circle(surface, color, (int(x), int(y)), 2)

    while True:
        theta1s, theta2s, w1s, w2s, time = EulerLoop(theta1, theta2, w1, w2)
        screen.fill(white)
        for j in range(len(time)):
            x1 = l1 * np.sin(theta1s[j])
            y1 = l1 * np.cos((theta1s[j]))
            x2 = x1 + l2 * np.sin(theta2s[j])
            y2 = y1 + l2 * np.cos(theta2s[j])

            point(scale * x1 + xo, scale * y1 + yo, black2)
            point(scale * x2 + xo, scale * y2 + yo, red2)
            screen.blit(surface, (0, 0))

            ball(scale * x1 + xo, scale * y1 + yo, ballSizeScale * m1,
                 black)  # Scaling the ball size(i.e radius) according to the mass.
            ball(scale * x2 + xo, scale * y2 + yo, ballSizeScale * m2, red)

            line(xo, yo, scale * x1 + xo, scale * y1 + yo)
            line(scale * x1 + xo, scale * y1 + yo, scale * x2 + xo, scale * y2 + yo)

            '''point(20 * time[j] + width / 2. - 10, 20 * theta1s[j] + height / 7. + 10, red)
            point(20 * time[j] + width / 2. - 10, 20 * theta2s[j] + height / 7. + 10, black)

            point(20 * time[j] + width / 2 - 10, 20 * w1s[j] + height - 100, red)
            point(20 * time[j] + width / 2. + 50, 20 * w2s[j] + height - 100, black)'''

            pygame.display.update()
            clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


a1 = 0
a2 = 45
rad = float(np.pi / 180.)
visual(a1 * rad, a2 * rad, 0, 0)
