import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import datetime
import os
import numpy as np
from fpdf import FPDF

# === DICCIONARIO EMOCIONAL ===
emociones_vibracionales = {
    "Iluminación": {"frecuencia": 700, "nivel": "Poder"},
    "Paz": {"frecuencia": 600, "nivel": "Poder"},
    "Alegría": {"frecuencia": 540, "nivel": "Poder"},
    "Amor": {"frecuencia": 500, "nivel": "Poder"},
    "Razón": {"frecuencia": 400, "nivel": "Poder"},
    "Aceptación": {"frecuencia": 350, "nivel": "Poder"},
    "Voluntad": {"frecuencia": 310, "nivel": "Poder"},
    "Neutralidad": {"frecuencia": 250, "nivel": "Poder"},
    "Coraje": {"frecuencia": 200, "nivel": "Poder"},
    "Orgullo": {"frecuencia": 175, "nivel": "Fuerza"},
    "Ira": {"frecuencia": 150, "nivel": "Fuerza"},
    "Deseo": {"frecuencia": 125, "nivel": "Fuerza"},
    "Miedo": {"frecuencia": 100, "nivel": "Fuerza"},
    "Aflicción": {"frecuencia": 75, "nivel": "Fuerza"},
    "Apatía": {"frecuencia": 50, "nivel": "Fuerza"},
    "Culpa": {"frecuencia": 30, "nivel": "Fuerza"},
    "Vergüenza": {"frecuencia": 20, "nivel": "Fuerza"},
}

# === RECOMENDACIONES ===
def obtener_recomendacion(estado):
    recomendaciones = {
        "Iluminación": "Continúa expandiendo tu conciencia. El silencio y la compasión son tu camino.",
        "Paz": "Medita, permanece en gratitud. Irradias paz al mundo.",
        "Alegría": "Comparte tu energía, ríe, crea arte. Tu luz inspira a otros.",
        "Amor": "Ama sin condiciones. Expresa cariño y compasión en tus relaciones.",
        "Razón": "Confía en tu lógica y mente clara. Lidera con conocimiento y ética.",
        "Aceptación": "Acepta lo que es. Perdona y fluye con la vida.",
        "Voluntad": "Organiza tus planes, actúa con determinación. Visualiza tu éxito.",
        "Neutralidad": "Suelta el control, vive con ligereza. Disfruta el presente.",
        "Coraje": "Actúa con valentía. Los cambios positivos comienzan contigo.",
        "Orgullo": "Practica la humildad. Aprende y mejora sin juzgar.",
        "Ira": "Canaliza tu energía en arte o ejercicio. Habla desde la calma.",
        "Deseo": "Reflexiona sobre tus verdaderas necesidades. Busca equilibrio.",
        "Miedo": "Confía en ti. Habla con alguien. Respira profundamente.",
        "Aflicción": "Permítete sentir. Rodéate de amor y comprensión.",
        "Apatía": "Haz algo pequeño hoy. Camina, respira, conéctate.",
        "Culpa": "Perdónate. Todos cometemos errores. Eres valioso.",
        "Vergüenza": "Eres suficiente. Habla con alguien de confianza. Sanar es posible.",
    }
    return recomendaciones.get(estado, "No hay recomendación disponible.")

# === CLASIFICAR ESTADO SEGÚN FRECUENCIA ===
def clasificar_estado(f):
    for emocion, datos in emociones_vibracionales.items():
        if f >= datos["frecuencia"]:
            return emocion
    return "Vergüenza"

# === EXPORTAR PDF ===
def exportar_pdf(nombre, edad, emocion_principal, promedio, estado_salud, recomendacion, emociones, img_path):
    # Crear gráfico de escala vibracional
    etiquetas = [
        "Iluminación", "Paz", "Alegría", "Amor", "Razón", "Aceptación",
        "Voluntad", "Neutralidad", "Coraje", "Orgullo", "Ira", "Deseo",
        "Miedo", "Aflicción", "Apatía", "Culpa", "Vergüenza"
    ]
    frecuencias = [700, 600, 540, 500, 400, 350, 310, 250, 200, 175, 150, 125, 100, 75, 50, 30, 20]

    fig, ax = plt.subplots(figsize=(4, 6))
    y_pos = np.arange(len(etiquetas))
    ax.barh(y_pos, frecuencias, align='center', color=plt.cm.plasma(np.linspace(0, 1, len(etiquetas))))
    ax.set_yticks(y_pos)
    ax.set_yticklabels(etiquetas)
    ax.invert_yaxis()
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_title('Escala Vibracional')
    plt.tight_layout()

    if not os.path.exists("exportados"):
        os.makedirs("exportados")
    scale_path = os.path.join("exportados", "escala_temp.png")
    plt.savefig(scale_path)
    plt.close()

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Informe del Estado Interior", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 10, f"Edad: {edad}", ln=True)
    pdf.cell(0, 10, f"Emociones: {', '.join(emociones)}", ln=True)
    pdf.cell(0, 10, f"Promedio vibracional: {promedio:.1f} Hz", ln=True)
    pdf.cell(0, 10, f"Estado emocional: {emocion_principal}", ln=True)
    pdf.multi_cell(0, 10, f"Salud emocional: {estado_salud}")
    pdf.multi_cell(0, 10, f"Recomendación: {recomendacion}")

    pdf.image(img_path, x=30, y=110, w=80)
    pdf.image(scale_path, x=120, y=110, w=70)

    output_pdf = os.path.join("exportados", f"Informe_{nombre}.pdf")
    pdf.output(output_pdf)
    print(f"✅ PDF generado: {output_pdf}")

# === INTERFAZ ===
ventana = tk.Tk()
ventana.title("Mapa del Estado Interior")
ventana.geometry("400x350")

tk.Label(ventana, text="Nombre:").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="Edad:").pack()
entry_edad = tk.Entry(ventana)
entry_edad.pack()

tk.Label(ventana, text="Emociones (separadas por comas):").pack()
entry_emociones = tk.Entry(ventana, width=50)
entry_emociones.pack()

# === FUNCIÓN PRINCIPAL ===
def analizar():
    nombre = entry_nombre.get().strip()
    edad = entry_edad.get().strip()
    entrada = entry_emociones.get()

    if not nombre or not edad or not entrada:
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
        return

    emociones = [e.strip().capitalize() for e in entrada.split(",")]
    frecuencias = []

    for emocion in emociones:
        if emocion in emociones_vibracionales:
            frecuencias.append(emociones_vibracionales[emocion]["frecuencia"])
        else:
            messagebox.showerror("Emoción inválida", f"Emoción no reconocida: {emocion}")
            return

    promedio = sum(frecuencias) / len(frecuencias)
    estado = clasificar_estado(promedio)
    recomendacion = obtener_recomendacion(estado)
    estado_salud = "Elevado" if promedio >= 250 else "Bajo"

    # === SILUETA Y GRADIENTE ===
    silueta = Image.open("imagenes/Silueta.png").convert("L")
    silueta = ImageOps.invert(silueta)
    silueta = silueta.point(lambda p: 255 if p > 50 else 0)
    mask = silueta.convert("L")

    colores = [
        (255, 0, 0), (255, 85, 0), (255, 153, 0), (255, 204, 0),
        (255, 255, 0), (153, 255, 0), (0, 255, 0), (0, 255, 170),
        (0, 204, 255), (0, 128, 255), (0, 0, 255), (102, 0, 255),
        (153, 0, 204), (204, 0, 204), (255, 0, 255)
    ]

    gradient = Image.new("RGB", silueta.size)
    draw = ImageDraw.Draw(gradient)
    h = silueta.height
    step = h // len(colores)

    for i, color in enumerate(colores):
        y1 = i * step
        y2 = (i + 1) * step if i < len(colores) - 1 else h
        draw.rectangle([0, y1, silueta.width, y2], fill=color)

    imagen_final = Image.composite(gradient, Image.new("RGB", silueta.size, (255, 255, 255)), mask)

    # === GUARDAR IMAGEN PERSONALIZADA ===
    if not os.path.exists("exportados"):
        os.makedirs("exportados")
    filename = os.path.join("exportados", f"{nombre}_Estado_{estado}.png".replace(" ", "_"))
    imagen_final.save(filename)

    # === GUARDAR EN HISTORIAL ===
    with open("historial.txt", "a", encoding="utf-8") as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{fecha}] {nombre} ({edad} años) - Estado: {estado}, Frecuencia: {promedio:.1f} Hz\n")
        f.write(f"  Emociones: {', '.join(emociones)}\n")
        f.write(f"  Recomendación: {recomendacion}\n\n")

    # === MOSTRAR RESULTADO ===
    plt.figure(figsize=(4, 8))
    plt.imshow(imagen_final)
    plt.axis("off")
    plt.title(f"{nombre}, {edad} años\nEstado: {estado}\nFrecuencia: {promedio:.1f} Hz")
    plt.tight_layout()
    plt.show()

    messagebox.showinfo("Recomendación", recomendacion)

    # === EXPORTAR PDF ===
    exportar_pdf(
        nombre=nombre,
        edad=edad,
        emocion_principal=estado,
        promedio=promedio,
        estado_salud=estado_salud,
        recomendacion=recomendacion,
        emociones=emociones,
        img_path=filename
    )

# === BOTÓN ===
tk.Button(ventana, text="Analizar Estado Interior", command=analizar).pack(pady=10)

ventana.mainloop()