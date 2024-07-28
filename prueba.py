#Quiz Tech
#Autor: Elisa Mendoza
import tkinter as tk
from tkinter import messagebox

#Preguntas, respuestas y opciones del Quiz
preguntas=[["¿Que lenguaje diseñó Guido van Rossum en 1991?","Python", ['Javascript', 'Python', 'Java', 'C++']],
           ["¿Quién hizo el primer programa informático del mundo?","Ada Lovelace", ['Herman Hollerith','Tommy Flowers','Konrad Zuse','Ada Lovelace']],
           ["¿Qué compañía hizo el primer teléfono móvil del mundo?","Motorola", ['Motorola','AT&T','Nokia','Nextel']],
           ["¿En qué año se conectó la primera página web?","1990", ['1989','1990','1983', '1994']],
           ["¿Cuánto costaba un USB flash drive de 1GB en el año 2001?","$10.000", ['$300','$50','$10.000','$10']], 
           ["¿Cómo se llamó la primera consola de video-juegos?","Magnavox Odysey", ['Magnavox Odysey','Atari 2600','Sega Mastersystem','NES Nintendo']],
           ["¿Quién es considerado el padre de la computación?","Alan Turing", ['Bill Gates','Alan Turing','Steve Jobs','Steve Wozniak']],
           ["¿Cuántas víctimas de ciberataques hubo en el 2023 (solo en EEUU)?","350 millones", ['4 millones','280.000','23 millones','350 millones']],
           ["¿Por donde empiezan el 75% de los ciberataques?","Email", ['Email','WhatsApp','Llamadas telefónicas','Juegos online']],
           ["Lenguaje mas popular de programación es","Python", ['C','Javascript','Python','Java']],
           ["País con mas ataques cibernéticos en el mundo es","China", ['Rusia','China','Irán','Corea del Norte']]]

# Función para cargar partidas guardadas en el archivo y ser usadas en el programa
def cargar_partidas():
    partidas = []
    with open('partidas.txt', 'r') as file:
        for linea in file:
            jugador, puntaje, respuestas_str = linea.strip().split(';')#divide linea o frase en palabras que estén divididas con ;
            respuestas = [list(r.split(':')) for r in respuestas_str.split('|')]
            partidas.append([jugador, int(puntaje), respuestas])
    return partidas

# Función para iniciar una nueva partida
def iniciar_partida():
    global nombre_jugador, puntaje, respuestas, pregunta_actual
    nombre_jugador = nombre_entry.get()
    if not nombre_jugador:
        messagebox.showwarning("Advertencia", "Introduce tu nombre.")
        return
    #Cuando se inicia una nueva partida, se deshabilitan ciertas entradas y botones para evitar interferencias.
    nombre_entry.config(state='disabled')
    iniciar_button.config(state='disabled')
    retomar_button.config(state='disabled')
    mostrar_button.config(state='disabled')
    
    puntaje = 0
    respuestas = []
    pregunta_actual = 0
    
    mostrar_pregunta()

# Función para guardar partidas. Convierte la lista en String y lo guarda en un .txt
def guardar_partidas(partidas):
    with open('partidas.txt', 'w') as file:
        for partida in partidas:
            respuestas_str = '|'.join([f"{p}:{r}" for p, r in partida[2]])
            file.write(f"{partida[0]};{partida[1]};{respuestas_str}\n")

def mostrar_pregunta():
    global pregunta_actual#contador de preguntas
    if pregunta_actual < len(preguntas):
        pregunta_label.config(text=f"{preguntas[pregunta_actual][0]}\n-{preguntas[pregunta_actual][2][0]}\n-{preguntas[pregunta_actual][2][1]}\n-{preguntas[pregunta_actual][2][2]}\n-{preguntas[pregunta_actual][2][3]}")
        respuesta_entry.delete(0, tk.END)
    else:
        finalizar_partida()

def verificar_respuesta():
    global pregunta_actual, puntaje
    respuesta = respuesta_entry.get()
    if not respuesta:
        messagebox.showwarning("Advertencia", "Introduce una respuesta.")
        return
    
    respuestas.append((preguntas[pregunta_actual][0], respuesta))
    if respuesta.lower() == preguntas[pregunta_actual][1].lower():
        puntaje += 1
    
    pregunta_actual += 1 
    mostrar_pregunta()

def finalizar_partida():
    global nombre_jugador, puntaje, respuestas, partidas
    partida = (nombre_jugador, puntaje, respuestas)
    partidas.append(partida)
    guardar_partidas(partidas)
    
    messagebox.showinfo("Fin de la partida", f"Partida finalizada. Tu puntaje es: {puntaje}")
    
    nombre_entry.config(state='normal')
    iniciar_button.config(state='normal')
    retomar_button.config(state='normal')
    mostrar_button.config(state='normal')

# Función para retomar una jugada guardada
def retomar_partida():
    nombre_jugador = nombre_entry.get()
    if not nombre_jugador:
        messagebox.showwarning("Advertencia", "Introduce tu nombre.")
        return
    
    partidas_jugador = [p for p in partidas if p[0] == nombre_jugador]
    if not partidas_jugador:
        messagebox.showinfo("Información", "No se encontraron partidas guardadas para este jugador.")
        return

    ultima_partida = partidas_jugador[-1]
    respuestas_str = "\n".join([f"{pregunta} - Tu respuesta: {respuesta}" for pregunta, respuesta in ultima_partida[2]])
    messagebox.showinfo("Retomar partida", f"Retomando partida de {nombre_jugador}. Tu último puntaje fue: {ultima_partida[1]}\n\nRespuestas anteriores:\n{respuestas_str}")

# Función para mostrar partidas históricas
def mostrar_partidas_historicas():
    if not partidas:
        messagebox.showinfo("Información", "No hay partidas históricas.")
        return
    
    historico = ""
    for partida in partidas:
        historico += f"Jugador: {partida[0]}, Puntaje: {partida[1]}\nRespuestas:\n"
        historico += "\n".join([f"  {pregunta} - {respuesta}" for pregunta, respuesta in partida[2]])
        historico += "\n\n"
    
    messagebox.showinfo("Partidas históricas", historico)

# Programa principal
partidas = cargar_partidas()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Juego de Trivia")

tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
nombre_entry = tk.Entry(root)
nombre_entry.grid(row=0, column=1, padx=10, pady=10)

iniciar_button = tk.Button(root, text="Iniciar juego", command=iniciar_partida)
iniciar_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

retomar_button = tk.Button(root, text="Retomar jugada", command=retomar_partida)
retomar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

mostrar_button = tk.Button(root, text="Mostrar partidas históricas", command=mostrar_partidas_historicas)
mostrar_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

tk.Button(root, text="Salir", command=root.quit).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

pregunta_label = tk.Label(root, text="", wraplength=400)
pregunta_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Respuesta:").grid(row=6, column=0, padx=10, pady=10)
respuesta_entry = tk.Entry(root)
respuesta_entry.grid(row=6, column=1, padx=10, pady=10)

tk.Button(root, text="Enviar", command=verificar_respuesta).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

