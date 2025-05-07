import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


sns.set(style="whitegrid")
sns.set_palette("tab10")

# Personalizacion global con matplotlib
plt.rcParams.update({
    'axes.titlesize': 20,        # Tamaño del titulo
    'axes.titleweight': 'bold',  # Negrita en el titulo
    'xtick.labelsize': 8,        # Tamaño de los xticks
    'ytick.labelsize': 8,         # Tamaño de los yticks
    'grid.color': 'gray',         # Color de las lineas del grid
    'grid.linestyle': '--',       # Estilo de linea (puede ser '-', '--', '-.', ':')
    'grid.linewidth': 0.5,        # Grosor del grid
    'axes.grid': True,            # Asegura que el grid esté activado
    'axes.grid.axis': 'both',     # Aplica el grid a ambos ejes
    'lines.linewidth': 1.2,       # Grosor de las lineas
    'figure.figsize': (12, 6),   # Tamaño de la figura
})

def curva_corvengencia_individual(resultados, path, file_name):
    plt.figure()
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        for i, res in enumerate(resultados_ejecuciones):
            plt.plot(res["historial_de_fitnesses"], label=f"{nombre_configuracion} (Ejecucion {i+1})" if i == 0 else "", alpha=0.3)
        longitud_minima = min(len(res["historial_de_fitnesses"]) for res in resultados_ejecuciones)
        historiales_truncados = [res["historial_de_fitnesses"][:longitud_minima] for res in resultados_ejecuciones]
        historial_promedio_fitnesses = np.mean(historiales_truncados, axis=0)
        plt.plot(historial_promedio_fitnesses, label=f"Prom. {nombre_configuracion}", linewidth=2)
        plt.xlabel("Generación")
        plt.ylabel("Mejor fitness")
        plt.title("Curva de Convergencia del Mejor Fitness")
        plt.legend(loc='upper right', fontsize='small')
        plt.grid(True)
        plt.savefig(os.path.join(path, file_name, nombre_configuracion, f"curvas_convergencia.pdf"), bbox_inches='tight')
        plt.close()

def box_plot_costos(resultados, path, file_name):
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        plt.figure(figsize=(4, 6))
        costos = [res["mejor_costo"] for res in resultados_ejecuciones]
        plt.boxplot(costos, positions=[list(resultados.keys()).index(nombre_configuracion)], patch_artist=True, widths=0.5)
        plt.xlabel("Configuración")
        plt.ylabel("Mejor Costo")
        plt.title("Mejores Costos")
        plt.grid(True, axis='y')
        plt.savefig(os.path.join(path, file_name, nombre_configuracion, "boxplot_mejores_costos.pdf"), bbox_inches='tight')
        plt.close()

def guardar_resultados(resultados, path, file_name, random_seed):
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        texto = ""
        mejor_ejecucion = min(resultados_ejecuciones, key=lambda x: x["mejor_costo"])
        texto += f"\nConfiguracion: {nombre_configuracion}\n"
        texto += f"  Mejor Solucion (Instalaciones Abiertas): {mejor_ejecucion['mejor_solucion']}\n"
        texto += f"  Mejor Costo: {mejor_ejecucion['mejor_costo']:.2f}\n"
        texto += f"\nSemilla aleatoria utilizada para reproducibilidad: {random_seed}\n"

        texto += f"\nTiempo de Ejecucion: {mejor_ejecucion['tiempo_de_ejecucion']:.2f} segundos\n"

        ruta_archivo = os.path.join(path, file_name, nombre_configuracion, "mejores_soluciones.txt")
        with open(ruta_archivo, "w") as f:
            f.write(texto)

        print("Texto guardado en", ruta_archivo)


def curva_convergencia_comparacion(resultados, path, file_name, show=False, alphaa=0.3, NOMBRE=""):
    plt.figure()
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        for i, res in enumerate(resultados_ejecuciones):
            plt.plot(res["historial_de_fitnesses"], label=f"{nombre_configuracion}" if i == 0 else "", alpha=alphaa, color=sns.color_palette("tab10")[list(resultados.keys()).index(nombre_configuracion)])
        longitud_minima = min(len(res["historial_de_fitnesses"]) for res in resultados_ejecuciones)
        historiales_truncados = [res["historial_de_fitnesses"][:longitud_minima] for res in resultados_ejecuciones]
        historial_promedio_fitnesses = np.mean(historiales_truncados, axis=0)
        plt.plot(historial_promedio_fitnesses, label=f"Promedio del {[list(resultados.keys()).index(nombre_configuracion)]} algoritmo", linewidth=2, color=sns.color_palette("tab10")[list(resultados.keys()).index(nombre_configuracion)])
    plt.xlabel("Generacion")
    plt.ylabel("Mejor fitness")
    plt.title(f"Curva de Convergencia del Mejor Fitness {NOMBRE}")
    plt.legend(loc='upper right', fontsize='small')
    plt.savefig(os.path.join(path, file_name, f"{NOMBRE}-comparacion-convergencia.pdf"), bbox_inches='tight')
    if show: plt.show()
    plt.close()

def box_plot_costos_comparacion(resultados, path, file_name, show=False, NOMBRE=""):
    datos_costos = {nombre_configuracion: [res["mejor_costo"] for res in resultados_ejecuciones] for nombre_configuracion, resultados_ejecuciones in resultados.items()}
    plt.figure()
    sns.boxplot(data=pd.DataFrame(datos_costos)).set(
        xlabel="Configuración",
        ylabel="Mejor Costo",
        title=f"Comparación de Distribuciones del Mejor Costo {NOMBRE}"
    )
    plt.savefig(os.path.join(path, file_name, f"{NOMBRE}-comparacion-soluciones.pdf"), bbox_inches='tight')
    if show: plt.show()
    plt.close()



def resumen_tablas(resultados, path, file_name, num_ejecuciones, tablas_resumen, random_seed, show=False, NOMBRE=""):
    pdf_path = os.path.join(path, file_name, f"{NOMBRE}-resumenes-tablas.pdf")
    # Guardar todas las tablas en un solo PDF
    with PdfPages(pdf_path) as pdf:
        for nombre_configuracion, resumen_df in tablas_resumen.items():
            fig, ax = plt.subplots(figsize=(8, 0.3 * len(resumen_df) + 2))  # Tamaño ajustado a la cantidad de filas
            ax.axis('off')
            ax.axis('tight')

            # Crear tabla
            tabla = ax.table(cellText=resumen_df.values,
                            colLabels=resumen_df.columns,
                            loc='center',
                            cellLoc='center',
                            colColours=["#2C3E50"] * len(resumen_df.columns))  # Encabezado con color

            # Formato
            tabla.auto_set_font_size(False)
            tabla.set_fontsize(10)
            tabla.scale(.8, 2)

            # Aplicar estilos a las celdas
            for (row, col), cell in tabla.get_celld().items():
                cell.set_edgecolor('white')  # Borde negro para todas las celdas
                if row == 0:
                    cell.set_text_props(weight='bold', color='white')  # Encabezado blanco y en negrita
                    cell.set_facecolor(sns.color_palette("tab10")[list(resultados.keys()).index(nombre_configuracion)])  # Fondo del encabezado
                else:
                    cell.set_facecolor('#E0E0E0' if row % 2 == 0 else 'white')  # Alternar colores de fila

            # Título por configuración
            plt.title(f"Configuración: {nombre_configuracion}, E={num_ejecuciones}, s={random_seed}", fontsize=12, weight='bold', pad=0)
            pdf.savefig(fig, bbox_inches='tight')
            if show: plt.show()
            plt.close()