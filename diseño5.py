import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np



def resistencia_hipotetica(dias, resistencia_inicial):
    # Convertir la lista de días a un array de NumPy
    dias_array = np.array(dias)
    
    # Modelo hipotético para el desarrollo de resistencia con el tiempo
    return resistencia_inicial * np.exp(0.1 * dias_array)


def calcular_dosificacion(resistencia_objetivo, relacion_arena_cemento):
    # Densidades aproximadas (kg/m³)
    densidad_cemento = 1440
    densidad_agua = 1000
    densidad_piedra = 1600
    densidad_arena = 1600

    # Volumen de los materiales en m³
    volumen_cemento = resistencia_objetivo / (densidad_cemento * 1.1**28)
    volumen_agua = 0.4 * volumen_cemento
    volumen_piedra = 2.5 * volumen_cemento / relacion_arena_cemento
    volumen_arena = relacion_arena_cemento * volumen_piedra

    # Convertir volumen a masa (kg)
    masa_cemento = volumen_cemento * densidad_cemento
    masa_agua = volumen_agua * densidad_agua
    masa_piedra = volumen_piedra * densidad_piedra
    masa_arena = volumen_arena * densidad_arena

    dosificacion_ajustada = {
        'Cemento': masa_cemento,
        'Agua': masa_agua,
        'Piedra': masa_piedra,
        'Arena': masa_arena
    }

    return dosificacion_ajustada

def mostrar_resultados(resistencia_objetivo, relacion_arena_cemento):
    # Calcular la dosificación de los materiales
    dosificacion = calcular_dosificacion(resistencia_objetivo, relacion_arena_cemento)

    # Mostrar resultados
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete('1.0', tk.END)
    resultados_text.insert(tk.END, "Cantidades de materiales (kg):\n")
    for material, cantidad in dosificacion.items():
        resultados_text.insert(tk.END, f"{material}: {cantidad:.2f} kg\n")
    resultados_text.config(state=tk.DISABLED)

    # Actualizar el gráfico
    actualizar_grafico(resistencia_objetivo)

def actualizar_grafico(resistencia_objetivo):
    # Crear y mostrar el gráfico (puedes personalizar según tus necesidades)
    dias = [3, 7, 14, 28]
    
    # Resistencias reales
    resistencias = [resistencia_objetivo * (1.05 ** dia) for dia in dias]

    
    # Resistencias hipotéticas
    resistencia_inicial = 20  # Resistencia inicial hipotética en Kg/cm2
    resistencias_hipoteticas = resistencia_hipotetica(dias, resistencia_inicial)

    
    ax.clear()
    ax.plot(dias, resistencias_hipoteticas, marker='o', linestyle='-', color='g', label='Hipotético')
    ax.axhline(y=resistencia_objetivo, color='r', linestyle='--', label='Objetivo')
    ax.set_xlabel('Días')
    ax.set_ylabel('Resistencia (kg/cm²)')
    ax.set_title('Desarrollo de Resistencia con el Tiempo')
    ax.legend()

    canvas.draw_idle()


# Crear la interfaz gráfica
window = tk.Tk()
window.title("Diseño de Mezcla de Hormigón")

# Crear dos marcos (frames)
frame_izquierdo = ttk.Frame(window)
frame_izquierdo.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)

frame_derecho = ttk.Frame(window)
frame_derecho.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)

# Etiquetas y entradas en el marco izquierdo
resistencia_label = ttk.Label(frame_izquierdo, text="Resistencia Objetivo (kg/cm²):")
resistencia_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
resistencia_entry = ttk.Entry(frame_izquierdo)
resistencia_entry.grid(row=0, column=1, padx=5, pady=5)

relacion_label = ttk.Label(frame_izquierdo, text="Relación Arena/Cemento:")
relacion_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
relacion_entry = ttk.Entry(frame_izquierdo)
relacion_entry.grid(row=1, column=1, padx=5, pady=5)

# Botón para calcular dosificación y mostrar gráfico
calcular_button = ttk.Button(frame_izquierdo, text="Calcular y Mostrar Gráfico", command=lambda: mostrar_resultados(float(resistencia_entry.get()), float(relacion_entry.get())))
calcular_button.grid(row=2, column=0, columnspan=2, pady=10)

# Resultados en el marco izquierdo
resultados_text = tk.Text(frame_izquierdo, height=8, width=40, state=tk.DISABLED)
resultados_text.grid(row=3, column=0)

# Configuración del gráfico en el marco derecho
fig, ax = plt.subplots()
ax.set_xlabel('Días')
ax.set_ylabel('Resistencia (kg/cm²)')

# Agregar estas líneas
canvas = FigureCanvasTkAgg(fig, master=frame_derecho)
canvas.get_tk_widget().pack()

# Iniciar la interfaz gráfica
window.mainloop()
