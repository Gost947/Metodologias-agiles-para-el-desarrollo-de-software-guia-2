import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import urllib3
from io import BytesIO
from PIL import ImageTk, Image

# colores
co1 = "#ffffff"
co2 = "#333333"
co3 = "#f0f0f0"
co4 = "#e74c3c"
co5 = "#3498db"

window = tk.Tk()
window.geometry("500x800")
window.title("Pokedex")
window.config(padx=10, pady=10, bg=co1)
style = ttk.Style(window)
style.theme_use("default")


def show_instructions():
    instructions = """
    ¡Bienvenido a la Pokedex!

    Instrucciones:
    1. Escribe el nombre o número de un Pokémon
    2. Haz clic en 'Buscar Pokémon'
    3. Verás su imagen, información y evoluciones

    Puedes buscar por nombre (pikachu) o número (25)
    """
    messagebox.showinfo("Instrucciones", instructions)


show_instructions()


main_frame = tk.Frame(window, bg=co1)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(main_frame, text="Pokedex", fg=co4, bg=co1)
title_label.config(font=("Comfortaa", 32, "bold"))
title_label.pack(pady=(10, 20))

img_frame = tk.Frame(main_frame, bg=co1, bd=2, relief=tk.RIDGE)
img_frame.pack(pady=10)

pokemon_image = tk.Label(img_frame, bg=co1)
pokemon_image.pack(padx=10, pady=10)

info_frame = tk.Frame(main_frame, bg=co3, bd=2, relief=tk.GROOVE)
info_frame.pack(fill=tk.X, padx=10, pady=10)

pokemon_information = tk.Label(info_frame, bg=co3)
pokemon_information.config(font=("Arial", 16, "bold"))
pokemon_information.pack(pady=5)

pokemon_types = tk.Label(info_frame, bg=co3)
pokemon_types.config(font=("Arial", 14))
pokemon_types.pack(pady=5)

pokemon_height_weight = tk.Label(info_frame, bg=co3)
pokemon_height_weight.config(font=("Arial", 12))
pokemon_height_weight.pack(pady=5)

evo_frame = tk.Frame(main_frame, bg=co1)
evo_frame.pack(fill=tk.X, padx=10, pady=10)

evo_title = tk.Label(evo_frame, text="Evoluciones", fg=co2, bg=co1)
evo_title.config(font=("Arial", 14, "bold"))
evo_title.pack()

evo_images_frame = tk.Frame(evo_frame, bg=co1)
evo_images_frame.pack()

search_frame = tk.Frame(main_frame, bg=co1)
search_frame.pack(fill=tk.X, padx=10, pady=20)

label_id_name = tk.Label(search_frame, text="Nombre o Número:", fg=co2, bg=co1)
label_id_name.config(font=("Arial", 12))
label_id_name.pack()

text_id_name = tk.Entry(search_frame,
                        bg=co3,
                        fg=co2,
                        bd=2,
                        relief=tk.SUNKEN,
                        font=("Arial", 14),
                        width=25)
text_id_name.insert(0, "pikachu")
text_id_name.pack(pady=5)
text_id_name.focus_set()

btn_load = tk.Button(search_frame,
                     text="Buscar Pokémon",
                     command=lambda: load_pokemon(),
                     bg=co4,
                     fg=co1,
                     activebackground=co5,
                     activeforeground=co1,
                     bd=0)
btn_load.config(font=("Arial", 14, "bold"), height=1, width=15)
btn_load.pack(pady=10)


def load_pokemon():
    try:
        query = text_id_name.get().strip().lower()
        if not query:
            raise ValueError("Por favor ingresa un nombre o número de Pokémon")

        pokemon = pypokedex.get(name=query)

        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        image = PIL.Image.open(BytesIO(response.data))
        img = PIL.ImageTk.PhotoImage(image)
        pokemon_image.config(image=img)
        pokemon_image.image = img

        pokemon_information.config(text=f"#{pokemon.dex} - {pokemon.name.title()}")
        pokemon_types.config(text=f"Tipo: {' / '.join([t.title() for t in pokemon.types])}")
        pokemon_height_weight.config(text=f"Altura: {pokemon.height / 10}m | Peso: {pokemon.weight / 10}kg")

        for widget in evo_images_frame.winfo_children():
            widget.destroy()

        try:
            if pokemon.dex == 25:
                evos = [("pichu", 172), ("pikachu", 25), ("raichu", 26)]
            elif pokemon.dex == 1:
                evos = [("bulbasaur", 1), ("ivysaur", 2), ("venusaur", 3)]
            elif pokemon.dex == 4:
                evos = [("charmander", 4), ("charmeleon", 5), ("charizard", 6)]
            else:
                evos = [(pokemon.name, pokemon.dex)]

            for i, (evo_name, evo_dex) in enumerate(evos):
                try:
                    evo_pokemon = pypokedex.get(name=evo_name)
                    evo_response = http.request('GET', evo_pokemon.sprites.front.get('default'))
                    evo_image = PIL.Image.open(BytesIO(evo_response.data))

                    evo_image = evo_image.resize((80, 80), Image.LANCZOS)
                    evo_img = PIL.ImageTk.PhotoImage(evo_image)

                    evo_label = tk.Label(evo_images_frame, image=evo_img, bg=co1)
                    evo_label.image = evo_img
                    evo_label.grid(row=0, column=i, padx=5)

                    name_label = tk.Label(evo_images_frame, text=f"#{evo_dex} {evo_name.title()}", bg=co1)
                    name_label.grid(row=1, column=i, padx=5)

                    if evo_name == pokemon.name:
                        evo_label.config(bd=3, relief=tk.SOLID, highlightbackground=co4)
                        name_label.config(fg=co4, font=("Arial", 10, "bold"))
                    else:
                        name_label.config(fg=co2, font=("Arial", 9))

                except Exception as e:
                    print(f"Error cargando evolución {evo_name}: {e}")

        except Exception as e:
            print(f"Error obteniendo evoluciones: {e}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

load_pokemon()

window.mainloop()