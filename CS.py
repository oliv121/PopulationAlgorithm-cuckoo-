import numpy as np
from math import gamma
import matplotlib.pyplot as plt


# параболичесая фитнесс-функция с точкой глобального экстремума [0;0]
def fi(x, y):
    return -x * x - y * y


# Инициализация популяции S
def initial(s_mod):
    if s_mod == 30:
        s = dict()
        for j in range(s_mod):
            x = np.random.uniform(-20, 20)
            y = np.random.uniform(-20, 20)
            s[x] = y
        fig, ax = plt.subplots()
        ax.set_xlim(-40, 40)
        ax.set_ylim(-40, 40)
        ax.scatter(s.keys(), s.values())
        plt.show()
        return s
    # при вызове функции для добавления новго агента
    elif s_mod == 1:
        x = 10*np.random.uniform(-20, 20)
        y = 10*np.random.uniform(-20, 20)
        return x, y


# Полет Леви
def levy_flight(x, y):
    param_lambda = 1.5
    alpha = 1

    dividend = gamma(1 + param_lambda) * np.sin(np.pi * param_lambda / 2)
    divisor = gamma((1 + param_lambda) / 2) * param_lambda * np.power(2, (param_lambda - 1) / 2)
    sigma1 = np.power(dividend / divisor, 1 / param_lambda)
    sigma2 = 1
    u_vec = np.random.normal(0, sigma1, size=2)
    v_vec = np.random.normal(0, sigma2, size=2)
    step_length = u_vec / np.power(np.fabs(v_vec), 1 / param_lambda)

    x = float(x) + alpha * step_length[0]
    y = float(y) + alpha * step_length[1]

    return x, y


xc = 10 * np.random.random()
yc = 10 * np.random.random()
epsilon = 0.2
positions = {}
positions = initial(30)

# в качесве условия окончания поиска береться заданное число итераций
for i in range(30000):
    min1 = -100
    min2 = -100
    min_x1 = -100
    min_x2 = -100

    # полет кукушки
    xc, yc = levy_flight(xc, yc)

    # рандомный выбор гнезда
    si = np.random.choice(list(positions.keys()))

    # замена Xi на Xc
    if(fi(si, positions[si])) < fi(xc, yc):
        positions.pop(si)
        positions[xc] = yc

# Удаление гнезд из попопуляции и их замена
    # находим две самые худшие
    for a, b in positions.items():
        if fi(a, b) <= min1:
            min2 = min1
            min1 = fi(a, b)
            min_x2 = min_x1
            min_x1 = a
        elif fi(a, b) <= min2:
            min2 = fi(a, b)
            min_x2 = a
    # смотрим вероятность и заменяем если >0.2
    epsilon = np.random.random()
    if epsilon > 0.2:
        if min1 > 0:
            positions.pop(min_x1)
            x_new, y_new = initial(1)
            positions[x_new] = y_new
        if min2 > 0:
            positions.pop(min_x2)
            x_new, y_new = initial(1)
            positions[x_new] = y_new

figure, axes = plt.subplots()
axes.set_xlim(-40, 40)
axes.set_ylim(-40, 40)
axes.scatter(positions.keys(), positions.values())
plt.show()
