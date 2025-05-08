"""





Son muchas funciones que generan graficas y guardan resultados de los algoritmos geneticos





"""






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







def resumen(resultados, fitness_objetivo, random_seed, path, file_name):
    tablas_resumen = {}

    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        # Extraer valores
        costos = [res["mejor_costo"] for res in resultados_ejecuciones]
        tiempos = [res["tiempo_de_ejecucion"] for res in resultados_ejecuciones]
        generaciones_optimas = [res["generacion_optima"] for res in resultados_ejecuciones if res["generacion_optima"] is not None]

        if not costos or not tiempos:
            # Saltar si no hay datos válidos
            continue

        # Métricas de costos
        mejor_costo = min(costos)
        mejor_costo_index = costos.index(mejor_costo)
        peor_costo = max(costos)
        costo_promedio = np.mean(costos)
        desviacion_estandar_costo = np.std(costos)

        # Métricas de tiempo
        tiempo_promedio = np.mean(tiempos)
        desviacion_porcentual = np.std(tiempos)
        mejor_tiempo = np.min(tiempos)

        # Métricas de error
        error = mejor_costo - fitness_objetivo
        error_relativo = (error / fitness_objetivo) if fitness_objetivo != 0 else np.inf

        # Métricas de generaciones
        if generaciones_optimas:
            
            generacion_optima_promedio = np.mean(generaciones_optimas)
            mejor_generacion = min(generaciones_optimas)
            mejor_generacion_index = generaciones_optimas.index(mejor_generacion)
            
            tablas_resumen[nombre_configuracion] = pd.DataFrame({
            "Métrica": [
                "Costo Objetivo",
                "Mejor Costo",
                "Peor Costo",
                "Costo Promedio",
                "Desviación Estándar Costo",
                "Tiempo Promedio de Ejecución",
                "Mejor Tiempo de Ejecución",
                "Desviación del Tiempo",
                "Generación Óptima Promedio",
                "Generación más Rápida",
                "Semilla más Rápida"
            ],
            "Valor": [
                f"{fitness_objetivo}",
                f"{mejor_costo}",
                f"{peor_costo:.0f}",
                f"{costo_promedio:.0f}",
                f"{desviacion_estandar_costo:.4f}",
                f"{tiempo_promedio:.6f}s",
                f"{mejor_tiempo:.6f}s",
                f"{desviacion_porcentual:.6f}",
                f"{generacion_optima_promedio:.2f}",
                f"{mejor_generacion}",
                f"{random_seed[mejor_costo_index]}"
            ]
            })

        else:

            
            tablas_resumen[nombre_configuracion] = pd.DataFrame({
            "Métrica": [
                "Costo Objetivo",
                "Mejor Costo",
                "Error",
                "Error Relativo",
                "Peor Costo",
                "Costo Promedio",
                "Desviación Estándar Costo",
                "Tiempo Promedio de Ejecución",
                "Mejor Tiempo de Ejecución",
                "Desviación del Tiempo",
                "Semilla Mejor Costo"
            ],
            "Valor": [
                f"{fitness_objetivo}",
                f"{mejor_costo}",
                f"{error:.0f}",
                f"{error_relativo:.6f}",
                f"{peor_costo:.0f}",
                f"{costo_promedio:.0f}",
                f"{desviacion_estandar_costo:.4f}",
                f"{tiempo_promedio:.6f}s",
                f"{mejor_tiempo:.6f}s",
                f"{desviacion_porcentual:.6f} %",
                f"{random_seed[mejor_costo_index]}"
            ]
            })




        # Crear carpeta si no existe
        os.makedirs(os.path.join(path, file_name, nombre_configuracion), exist_ok=True)

    # Guardar CSVs
    for nombre_configuracion, resumen_df in tablas_resumen.items():
        resumen_df.to_csv(os.path.join(path, file_name, nombre_configuracion, "resumen.csv"), index=False)

    return tablas_resumen






















def curva_corvengencia_individual(resultados, path, file_name):
    plt.figure()
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        for i, res in enumerate(resultados_ejecuciones):
            plt.plot(res["historial_de_fitnesses"], label=f"Ejecucion {i+1}", alpha=0.3)
        longitud_minima = min(len(res["historial_de_fitnesses"]) for res in resultados_ejecuciones)
        historiales_truncados = [res["historial_de_fitnesses"][:longitud_minima] for res in resultados_ejecuciones]
        historial_promedio_fitnesses = np.mean(historiales_truncados, axis=0)
        plt.plot(historial_promedio_fitnesses, label=f"Promedio", linewidth=2)
        plt.xlabel("Generación")
        plt.ylabel("Mejor fitness")
        plt.title("Curva de Convergencia del Mejor Fitness")
        plt.suptitle(f"Configuración: {nombre_configuracion}", fontsize=10, y=0.95)
        plt.legend(loc='upper right', fontsize='small')
        plt.savefig(os.path.join(path, file_name, nombre_configuracion, f"curvas_convergencia.pdf"), bbox_inches='tight')
        plt.close()

def box_plot_costos(resultados, path, file_name):
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        plt.figure(figsize=(4, 6))
        costos = [res["mejor_costo"] for res in resultados_ejecuciones]
        plt.boxplot(costos, positions=[list(resultados.keys()).index(nombre_configuracion)], patch_artist=True, widths=0.5)
        plt.xlabel(f"{nombre_configuracion}", fontsize=8)
        plt.ylabel("Mejor Costo")
        plt.xticks([])
        plt.title("Mejores Costos")
        plt.savefig(os.path.join(path, file_name, nombre_configuracion, "boxplot_mejores_costos.pdf"), bbox_inches='tight')
        plt.close()

def guardar_resultados(resultados, path, file_name, random_seed):
    for nombre_configuracion, resultados_ejecuciones in resultados.items():
        texto = ""
        mejor_ejecucion = min(resultados_ejecuciones, key=lambda x: x["mejor_costo"])
        mejor_ejecucion_index = resultados_ejecuciones.index(mejor_ejecucion)
        texto += f"\nConfiguración: {nombre_configuracion}\n"
        texto += f"  Mejor Solución: {mejor_ejecucion['mejor_solucion']}\n"
        texto += f"  Mejor Costo: {mejor_ejecucion['mejor_costo']}\n"
        texto += f"\nSemilla utilizada: {random_seed[mejor_ejecucion_index]}\n"

        texto += f"\nTiempo de Ejecución: {mejor_ejecucion['tiempo_de_ejecucion']:.5f} segundos\n"

        ruta_archivo = os.path.join(path, file_name, nombre_configuracion, "mejor-solucion.txt")
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
    if NOMBRE != "": 
        plt.savefig(os.path.join(path, file_name, f"{NOMBRE}-comparacion-convergencia.pdf"), bbox_inches='tight')
    else:
        plt.savefig(os.path.join(path, file_name, f"comparacion-convergencia.pdf"), bbox_inches='tight')
    if show: plt.show()
    plt.close()

def box_plot_costos_comparacion(resultados, path, file_name, show=False, NOMBRE=""):
    datos_costos = {nombre_configuracion: [res["mejor_costo"] for res in resultados_ejecuciones] for nombre_configuracion, resultados_ejecuciones in resultados.items()}
    df = pd.DataFrame(datos_costos)

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(data=df)
    ax.set(
        xlabel="Configuración",
        ylabel="Mejor Costo",
        title=f"Comparación de Soluciones {NOMBRE}"
    )

    # Cambiar los nombres de los xticks
    configuraciones = list(resultados.keys())
    ax.set_xticklabels(configuraciones, rotation=10, fontsize=6)
    
    
    if NOMBRE != "":
        plt.savefig(os.path.join(path, file_name, f"{NOMBRE}-comparacion-soluciones.pdf"), bbox_inches='tight')
    else:
        plt.savefig(os.path.join(path, file_name, f"comparacion-soluciones.pdf"), bbox_inches='tight')
    if show: plt.show()
    plt.close()



def resumen_tablas(resultados, path, file_name, num_ejecuciones, tablas_resumen, random_seed, show=False, NOMBRE=""):

    if NOMBRE != "":
        pdf_path = os.path.join(path, file_name, f"{NOMBRE}-resumenes-tablas.pdf")
    else:
        pdf_path = os.path.join(path, file_name, f"resumenes-tablas.pdf")
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
            plt.title(f"Configuración: {nombre_configuracion}, E={num_ejecuciones}, s={random_seed}", fontsize=12, weight='bold', pad=10)
            pdf.savefig(fig, bbox_inches='tight')
            if show: plt.show()
            plt.close()