"""Double Pendulum simulation"""

### Sahil Islam ###
### 10/06/2020 ###

import matplotlib.pyplot as plt
import numpy as np
import pygame

'''theta1 = 0
theta2 = 0
w1 = 0
w2 = 0
t = 0'''

l1 = 1.
l2 = 1.
m1 = 3.
m2 = 3.

g = 9.80

'''def f1(theta1, theta2, w1, w2):
    rad = float(np.pi / 180.)
    nu = m2 * g * np.cos(rad * (theta1 - theta2)) * np.sin(rad * (theta2)) + m2 * l1 * np.sin(rad * (
            theta1 - theta2)) * w1 * w1 - m2 * l1 * np.cos(rad * (theta1 - theta2)) * np.sin(
        rad * (theta1 - theta2)) * w2 * w2 - m2 * g * np.sin(rad * (theta2))
    de = (m1 + m2) * l1 - m2 * l1 * np.cos(rad * (theta1 - theta2)) * np.cos(rad * (theta1 - theta2))
    fo = float(nu / de)
    return fo


def f2(theta1, theta2, w1, w2):
    rad = float(np.pi / 180.)
    ft = float(l1 / l2) * np.sin(rad * (theta1 - theta2)) * w1 * w1 - float(g / l2) * np.sin(
        rad * theta2) - float(l1 / l2) * np.cos(
        rad * (theta1 - theta2)) * f1(theta1, theta2, w1, w2)
    return ft'''


def f1(theta1, theta2, w1, w2):
    rad = float(np.pi / 180.)

    nu = -g * (2 * m1 + m2) * np.sin(rad * theta1) - m2 * g * np.sin(rad * (theta1 - 2 * theta2)) - 2 * np.sin(
        rad * (theta1 - theta2)) * m2 * (w2 * w2 * l2 + w1 * w1 * l1 * np.cos(rad * (theta1 - theta2)))
    de = l1 * (2 * m1 + m2 - m2 * np.cos(2 * rad * (theta1 - theta2)))
    return float(nu / de)


def f2(theta1, theta2, w1, w2):
    rad = float(np.pi / 180.)

    nu = 2 * np.sin(rad * (theta1 - theta2)) * (
            w1 * w1 * l1 * (m1 + m2) + g * (m1 + m2) * np.cos(rad * theta1) + w2 * w2 * l2 * m2 * np.cos(
        rad * (theta1 - theta2)))
    de = l2 * (2 * m1 + m2 - m2 * np.cos(2 * rad * (theta1 - theta2)))
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

    width = 900
    height = 650

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    clock = pygame.time.Clock()

    xo = width / 2.
    yo = height / 2.
    scale = 100

    screen = pygame.display.set_mode((width, height))
    surface = pygame.Surface((width, height))
    surface.fill(white)

    def ball(x, y, r, color):
        pygame.draw.circle(screen, color, (int(x), int(y)), int(r))

    def line(x1, y1, x2, y2):
        pygame.draw.line(screen, black, (x1, y1), (x2, y2), 2)

    def point(x, y, color):
        pygame.draw.circle(surface, color, (int(x), int(y)), 2)

    theta1s, theta2s, w1s, w2s, time = EulerLoop(theta1, theta2, w1, w2)

    for j in range(len(time)):
        screen.fill(white)
        x1 = l1 * np.sin(theta1s[j])
        y1 = -l1 * np.cos((theta1s[j]))
        x2 = x1 + l2 * np.sin(theta2s[j])
        y2 = y1 - l2 * np.cos(theta2s[j])

        point(scale * x1 + xo, scale * y1 + yo, black)
        point(scale * x2 + xo, scale * y2 + yo, red)
        screen.blit(surface, (0, 0))

        ball(scale * x1 + xo, scale * y1 + yo, 10, black)
        ball(scale * x2 + xo, scale * y2 + yo, 10, red)
        line(xo, yo, scale * x1 + xo, scale * y1 + yo)
        line(scale * x1 + xo, scale * y1 + yo, scale * x2 + xo, scale * y2 + yo)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(100)


visual(2, 10, 0, 0)

