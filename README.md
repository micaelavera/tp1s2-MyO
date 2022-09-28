# Pharmacy-tp (Part 2)
Programar una función en Python, **Coctel(farmacia, remedio)**, donde farmacia será el nombre
de un archivo conteniendo un input del mismo tipo que el del [punto 1](https://github.com/micaelavera/tp-MyO), mientras que remedio será
el nombre de un archivo con un remedio adicional. **Coctel(farmacia, remedio)** deberá devolver
la solución del input del primer parámetro, seguido de una nueva solución agregándole a dicho
input el remedio del segundo archivo.    


Nota: dado que se optimizarán dos instancias (una sin y otro con el remedio adicional), el segundo
modelo debe ser _modificar_ al primero (en lugar de declarar un modelo nuevo) –esto permite que
SCIP aproveche los cálculos ya hechos para el primer modelo–.
