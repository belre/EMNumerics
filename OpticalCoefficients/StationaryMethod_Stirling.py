import numpy as np
import matplotlib.pyplot as plt

def Integrant(w, param):
    t = 0
    if len(param) >= 1:
        t = param[0]

    g = np.log(w) - w
    return np.exp(t * g)

re_min = 0
re_max = 4
re_num = 51
im_min = -1
im_max = 1
im_num = 51

re_arr = np.linspace(re_min, re_max, re_num)
im_arr = 1j * np.linspace(im_min, im_max, im_num)

w_arr = []
for re_i in re_arr:
    w_arr.extend( (re_i + im_arr))

print(len(w_arr))

w_x, w_y = np.meshgrid(np.real(w_arr), np.imag(w_arr))
z = Integrant(w_x + 1j * w_y, [-10])

#print(w_x)
#print(w_y)

fig = plt.figure(figsize=(16,6))

fig.add_subplot( 1, 2, 1)
plt.title('Phase : z')
plt.xlabel("Real(w)")
plt.ylabel("Imag(w)")
plt.pcolormesh(w_x, w_y, np.angle(z), cmap='gray')
pp=plt.colorbar(orientation="vertical")

fig.add_subplot( 1, 2, 2)
plt.title('Absolute Value : Log(z)')
plt.xlabel("Real(w)")
plt.ylabel("Imag(w)")
plt.pcolormesh(w_x, w_y, np.log(np.abs(z)), cmap='gray')
pp=plt.colorbar(orientation="vertical")

#plt.contour(w_x, w_y, np.angle(z), colors=['black'])

plt.show()