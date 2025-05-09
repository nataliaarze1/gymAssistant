import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import curlBicep
import polichinelas
import pushUp
import sentadilla

# Diccionario global
checks = {}

def check(repeticionesTerminadas, ejercicioID):
    if repeticionesTerminadas:
        check_img = checks.get("img")
        label = checks.get(ejercicioID)
        if check_img and label:
            label.config(image=check_img)
            label.image = check_img
            label.place_configure(x=70)  

def seleccion_ejercicio(opcion, repeticiones_entry):
    repeticiones = repeticiones_entry.get()
    if not repeticiones.isdigit():
        messagebox.showwarning("Advertencia", "Por favor ingrese el número de repeticiones.")
        return

    repeticiones = int(repeticiones)

    if opcion == 1:
        curlBicep.curlBicep(repeticiones, lambda terminadas: check(terminadas, 1))
    elif opcion == 2:
        polichinelas.polichinelas(repeticiones, lambda terminadas: check(terminadas, 2))
    elif opcion == 3:
        pushUp.pushUps(repeticiones, lambda terminadas: check(terminadas, 3))
    elif opcion == 4:
        sentadilla.sentadillas(repeticiones, lambda terminadas: check(terminadas, 4))

def menu_principal():
    ventana = tk.Tk()
    ventana.title("Seleccionar Ejercicio")
    ventana.geometry("600x400")
    ventana.config(bg="#f0f0f0")

    imagen_fondo = Image.open("fondo5.jpg")  
    imagen_fondo = imagen_fondo.resize((600, 400), Image.Resampling.LANCZOS)
    fondo = ImageTk.PhotoImage(imagen_fondo)

    label_fondo = tk.Label(ventana, image=fondo)
    label_fondo.place(relwidth=1, relheight=1)

    canvas = tk.Canvas(ventana, width=600, height=400)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=fondo)

    canvas.create_text(300, 40, text="Seleccione el ejercicio que desea realizar:",
                    font=("Arial", 14), fill="black")

    # Frame dentro del Canvas
    frame_reps = tk.Frame(canvas, bg="#fffacd")
    label_reps = tk.Label(frame_reps, text="Número de repeticiones:", font=("Arial", 12), bg="#fffacd", fg="black")
    label_reps.pack(side=tk.LEFT, padx=(50, 10))

    repeticiones_entry = tk.Entry(frame_reps, font=("Arial", 12), justify="center", background="#fffacd", width=10)
    repeticiones_entry.pack(side=tk.LEFT)

    # Posicionar el frame sobre el canvas
    canvas.create_window(300, 80, window=frame_reps)


    estilo_boton = {
    "font": ("Helvetica", 12),
    "bg": "#fffacd",
    "fg": "black",
    "activeforeground": "white",
    "width": 15
}


    # Cargar imagen del check
    check_img_raw = Image.open("check.png").convert("RGBA").resize((25, 25), Image.Resampling.LANCZOS)
    check_img = ImageTk.PhotoImage(check_img_raw)

    checks["img"] = check_img  # Guardar para usar en la función check
    ejercicios = ["1. Curl De Biceps", "2. Polichinelas", "3. Push Ups", "4. Sentadillas"]
    for i, nombre in enumerate(ejercicios, start=1):
        y_pos = 100 + (i * 40)
        tk.Button(ventana, text=nombre, command=lambda i=i: seleccion_ejercicio(i, repeticiones_entry), **estilo_boton).place(relx=0.4, y=y_pos, anchor="center", x=60)
        check_label = tk.Label(ventana, bg="#f0f0f0")
        check_label.place(relx=0.6, y=y_pos,x=600, anchor="center")
        checks[i] = check_label

    tk.Button(ventana, text="Salir", command=ventana.quit, bg="#a00", fg="white", font=("Helvetica", 12, "bold"),
              activebackground="#c00", activeforeground="white", relief="flat", width=10).place(relx=0.5, y=330, anchor="center")

    ventana.mainloop()

if __name__ == '__main__':
    menu_principal()
