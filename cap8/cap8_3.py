from gameobjects.vector3 import *


A = Vector3(6, 8, 12)
B = Vector3(10, 16, 12)

print("A é: ", A)
print("B é: ", B)
print("Magnitude de A é: ", A.get_magnitude())
print("A + B é: ", A + B)
print("A - B é: ", A - B)
print(("A normalizado é: ", A.get_normalized()))
print("A * 2 é: ", A * 2)