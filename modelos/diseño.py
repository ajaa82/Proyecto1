import matplotlib.pyplot as plt
import numpy as np

def resistencia_hipotetica(dias, resistencia_inicial):
    # Modelo hipotético para el desarrollo de resistencia con el tiempo
    return resistencia_inicial * np.exp(0.1 * dias)

def diseño_mezcla(resistencias_objetivo):
    # Parámetros iniciales
    dias = np.array([3, 7, 14, 28])
    resistencias_iniciales = [15, 20, 25]  # Resistencias iniciales hipotéticas en Kg/cm2 (puedes ajustar estos valores)
    
    # Configuración del gráfico
    plt.title('Desarrollo Hipotético de Resistencia del Concreto')
    plt.xlabel('Días')
    plt.ylabel('Resistencia (Kg/cm2)')
    plt.grid(True)

    # Iterar sobre diferentes resistencias iniciales
    for resistencia_inicial in resistencias_iniciales:
        # Calcular resistencias hipotéticas
        resistencias_hipoteticas = resistencia_hipotetica(dias, resistencia_inicial)

        # Graficar resultados
        plt.plot(dias, resistencias_hipoteticas, marker='o', linestyle='-', label=f'Res. Inicial: {resistencia_inicial}')

    # Graficar la resistencia objetivo como una línea punteada roja
    plt.axhline(y=resistencias_objetivo, color='r', linestyle='--', label='Objetivo')

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.show()

# Ingresar la resistencia objetivo deseada
resistencia_objetivo = float(input("Ingrese la resistencia objetivo en Kg/cm2 : "))

# Llamar a la función de diseño de mezcla
diseño_mezcla(resistencia_objetivo)
