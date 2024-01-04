# Importación de librerías necesarias
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Función para calcular la resistencia hipotética del hormigón con el tiempo
def resistencia_hipotetica(dias, resistencia_inicial):
    # Convertir la lista de días a un array de NumPy para cálculos
    dias_array = np.array(dias)
    # Modelo de crecimiento exponencial de la resistencia
    return resistencia_inicial * np.exp(0.1 * dias_array)

# Función para calcular la dosificación de los componentes del hormigón
def calcular_dosificacion(resistencia_objetivo, relacion_agua_cemento):
    # Definir densidades de los materiales (kg/m³)
    densidad_cemento = 1440
    densidad_agua = 1000
    densidad_piedra = 1600
    densidad_arena = 1600

    # Calcular volumen necesario de cada material
    volumen_cemento = resistencia_objetivo / (densidad_cemento * 1.1**28)
    volumen_agua = relacion_agua_cemento * volumen_cemento
    volumen_piedra = 2.5 * volumen_cemento
    volumen_arena = relacion_agua_cemento * volumen_piedra

    # Convertir volumen a masa (kg) para cada material
    masa_cemento = volumen_cemento * densidad_cemento
    masa_agua = volumen_agua * densidad_agua
    masa_piedra = volumen_piedra * densidad_piedra
    masa_arena = volumen_arena * densidad_arena

    # Empaquetar los resultados en un diccionario
    dosificacion_ajustada = {
        'Cemento': masa_cemento,
        'Agua': masa_agua,
        'Piedra': masa_piedra,
        'Arena': masa_arena
    }

    return dosificacion_ajustada

# Función para mostrar resultados en la interfaz gráfica
def mostrar_resultados(resistencia_objetivo, relacion_agua_cemento):
    # Obtener la dosificación de materiales
    dosificacion = calcular_dosificacion(resistencia_objetivo, relacion_agua_cemento)

    # Configurar el área de texto para mostrar resultados
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete('1.0', tk.END)
    resultados_text.insert(tk.END, "Cantidades de materiales (kg):\n")
    for material, cantidad in dosificacion.items():
        resultados_text.insert(tk.END, f"{material}: {cantidad:.2f} kg\n")
    resultados_text.config(state=tk.DISABLED)

    # Actualizar el gráfico con los nuevos datos
    actualizar_grafico(resistencia_objetivo)

# Función para actualizar el gráfico en la interfaz
def actualizar_grafico(resistencia_objetivo):
    # Días para los cuales se mostrará la resistencia
    dias = [3, 7, 14, 28]
    # Calcular resistencias reales para los días dados
    resistencias = [resistencia_objetivo * (1.05 ** dia) for dia in dias]
    # Resistencia inicial hipotética para el cálculo
    resistencia_inicial = 20
    # Calcular resistencias hipotéticas
    resistencias_hipoteticas = resistencia_hipotetica(dias, resistencia_inicial)

    # Configuración y actualización del gráfico
    ax.clear()
    ax.plot(dias, resistencias_hipoteticas, marker='o', linestyle='-', color='g', label='Hipotético')
    ax.axhline(y=resistencia_objetivo, color='r', linestyle='--', label='Objetivo')
    ax.set_xlabel('Días')
    ax.set_ylabel('Resistencia (kg/cm²)')
    ax.set_title('Desarrollo de Resistencia con el Tiempo')
    ax.legend()

    # Redibujar el gráfico
    canvas.draw_idle()

# Configuración inicial de la ventana de la aplicación
window = tk.Tk()
window.title("Diseño de Mezcla de Hormigón")

# Creación de marcos para organizar la interfaz
frame_izquierdo = ttk.Frame(window)
frame_izquierdo.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)

frame_derecho = ttk.Frame(window)
frame_derecho.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)

# Creación de etiquetas y campos de entrada para los parámetros de diseño
resistencia_label = ttk.Label(frame_izquierdo, text="Resistencia Objetivo (kg/cm²):")
resistencia_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
resistencia_entry = ttk.Entry(frame_izquierdo)
resistencia_entry.grid(row=0, column=1, padx=5, pady=5)

relacion_label = ttk.Label(frame_izquierdo, text="Relación Agua/Cemento:")
relacion_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
relacion_entry = ttk.Entry(frame_izquierdo)
relacion_entry.grid(row=1, column=1, padx=5, pady=5)

# Botón para ejecutar el cálculo y actualizar la interfaz
calcular_button = ttk.Button(frame_izquierdo, text="Calcular y Mostrar Gráfico", command=lambda: mostrar_resultados(float(resistencia_entry.get()), float(relacion_entry.get())))
calcular_button.grid(row=2, column=0, columnspan=2, pady=10)

# Área de texto para mostrar los resultados de la dosificación
resultados_text = tk.Text(frame_izquierdo, height=8, width=40, state=tk.DISABLED)
resultados_text.grid(row=3, column=0)

# Configuración inicial del gráfico
fig, ax = plt.subplots()
ax.set_xlabel('Días')
ax.set_ylabel('Resistencia (kg/cm²)')

# Integración del gráfico en la interfaz gráfica de Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame_derecho)
canvas.get_tk_widget().pack()

# Inicio del bucle principal de la interfaz gráfica
window.mainloop()
