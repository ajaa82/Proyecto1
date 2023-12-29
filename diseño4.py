import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calcular_dosificacion(resistencia_objetivo, relacion_arena_cemento):
    # Parámetros iniciales (puedes ajustar según tus necesidades)
    resistencia_referencia = 20  # Resistencia de referencia para una relación arena/cemento de 3:1
    dosificacion_referencia = {'cemento': 1, 'arena': 3}  # Dosificación de referencia para resistencia_referencia

    # Calcular la dosificación ajustada para la resistencia objetivo
    factor_ajuste = resistencia_objetivo / resistencia_referencia
    dosificacion_ajustada = {material: factor_ajuste * dosificacion_referencia[material]
                            for material in dosificacion_referencia}

    # Ajustar la dosificación para cumplir con la relación arena/cemento deseada
    dosificacion_ajustada['arena'] *= relacion_arena_cemento
    dosificacion_ajustada['cemento'] /= relacion_arena_cemento

    # Agregar cantidad de agua y piedra (puedes ajustar según tus necesidades)
    dosificacion_ajustada['agua'] = 0.4 * dosificacion_ajustada['cemento']
    dosificacion_ajustada['piedra'] = 2.5 * dosificacion_ajustada['cemento']

    return dosificacion_ajustada

def mostrar_resultados(resistencia_objetivo, relacion_arena_cemento):
    # Calcular la dosificación de los materiales
    dosificacion = calcular_dosificacion(resistencia_objetivo, relacion_arena_cemento)

    # Mostrar resultados
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete('1.0', tk.END)
    resultados_text.insert(tk.END, "Dosificación de materiales:\n")
    for material, cantidad in dosificacion.items():
        resultados_text.insert(tk.END, f"{material}: {cantidad:.2f} partes\n")
    resultados_text.config(state=tk.DISABLED)

    # Actualizar el gráfico
    actualizar_grafico(resistencia_objetivo)

def actualizar_grafico(resistencia_objetivo):
    # Crear y mostrar el gráfico (puedes personalizar según tus necesidades)
    dias = [3, 7, 14, 28]
    resistencias = [resistencia_objetivo * (1.1 ** dia) for dia in dias]  # Resistencia en kg/cm²

    ax.clear()
    ax.plot(dias, resistencias, marker='o', linestyle='-', color='b')
    ax.set_xlabel('Días')
    ax.set_ylabel('Resistencia (kg/cm²)')
    ax.set_title('Desarrollo de Resistencia con el Tiempo')
    canvas.draw()

# Crear la interfaz gráfica
window = tk.Tk()
window.title("Diseño de Mezcla de Hormigón")

# Crear dos marcos (frames)
frame_izquierdo = ttk.Frame(window)
frame_izquierdo.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)

frame_derecho = ttk.Frame(window)
frame_derecho.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)

# Etiquetas y entradas en el marco izquierdo
resistencia_label = ttk.Label(frame_izquierdo, text="Resistencia Diseño(kg/cm²):")
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
resultados_text.grid(row=3, column=0, columnspan=2, pady=10)

# Configuración del gráfico en el marco derecho
fig, ax = plt.subplots()
ax.set_xlabel('Días')
ax.set_ylabel('Resistencia (kg/cm²)')
ax.set_title('Desarrollo de Resistencia con el Tiempo')
canvas = FigureCanvasTkAgg(fig, master=frame_derecho)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0)


# Iniciar la interfaz gráfica
window.mainloop()