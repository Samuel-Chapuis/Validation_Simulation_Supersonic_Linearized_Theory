import tkinter as tk
from tkinter import messagebox

# liste globale des zones de texte pour les colonnes
input_text_widgets = []

def process_text():
    print("Bouton Formater cliqué")  # message de débogage dans la console
    # Récupère le texte de chaque colonne
    columns_texts = [w.get("1.0", tk.END).strip() for w in input_text_widgets]
    if any(not text for text in columns_texts):
        messagebox.showwarning("Avertissement", "Veuillez coller les données dans toutes les zones d'entrée.")
        return

    # Découpe chaque colonne en lignes
    columns = [text.splitlines() for text in columns_texts]
    n_lines = len(columns[0])
    # Vérifie que toutes les colonnes contiennent le même nombre de lignes
    for col in columns:
        if len(col) != n_lines:
            messagebox.showwarning("Avertissement", "Toutes les colonnes doivent contenir le même nombre de lignes.")
            return

    points = []
    # Pour chaque ligne, rassemble les valeurs de chaque colonne
    for row in zip(*columns):
        # Prendre le texte sans remplacer automatiquement les virgules
        processed = [val.strip() for val in row]
        point = "(" + ", ".join(processed) + ")"
        points.append(point)

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "\n".join(points))

def change_commas():
	# Remplace dans chaque zone de texte toutes les virgules par des points
	for widget in input_text_widgets:
		text = widget.get("1.0", tk.END)
		new_text = text.replace(",", ".")
		widget.delete("1.0", tk.END)
		widget.insert(tk.END, new_text)
	messagebox.showinfo("Information", "Les virgules ont été remplacées par des points dans les colonnes.")

def change_points():
	# Remplace dans chaque zone de texte tous les points par des virgules
	for widget in input_text_widgets:
		text = widget.get("1.0", tk.END)
		new_text = text.replace(".", ",") 
		widget.delete("1.0", tk.END)
		widget.insert(tk.END, new_text)
	messagebox.showinfo("Information", "Les points ont été remplacés par des virgules dans les colonnes.")


def add_columns():
    # Ajoute une nouvelle colonne dans l'interface
    new_index = len(input_text_widgets)
    label = tk.Label(input_frame, text=f"Colonne {new_index + 1}:")
    label.grid(row=0, column=new_index, padx=5, pady=5)
    text_widget = tk.Text(input_frame, height=10, width=25)
    text_widget.grid(row=1, column=new_index, padx=5, pady=5)
    input_text_widgets.append(text_widget)
    print(f"Ajout de la colonne {new_index + 1}")

def remove_columns():
    # Supprime la dernière colonne si possible
    if len(input_text_widgets) <= 1:
        messagebox.showwarning("Avertissement", "Il faut au moins une colonne dans l'interface.")
        return
    last_index = len(input_text_widgets) - 1
    # Supprime le widget de la zone de texte
    widget = input_text_widgets.pop(last_index)
    widget.destroy()
    # Supprime également le label associé
    for label_widget in input_frame.grid_slaves(row=0, column=last_index):
        label_widget.destroy()
    print(f"Suppression de la colonne {last_index + 1}")

root = tk.Tk()
root.title("Formatage de Points")

# Barre de menu
menu_bar = tk.Menu(root)

# Menu Colonnes
colonnes_menu = tk.Menu(menu_bar, tearoff=0)
colonnes_menu.add_command(label="Ajouter des colonnes", command=add_columns)
colonnes_menu.add_command(label="Supprimer des colonnes", command=remove_columns)
menu_bar.add_cascade(label="Colonnes", menu=colonnes_menu)

# Nouveau menu Formatage
formatage_menu = tk.Menu(menu_bar, tearoff=0)
formatage_menu.add_command(label="Change ',' -> '.'", command=change_commas)
formatage_menu.add_command(label="Change '.' -> ','", command=change_points)
menu_bar.add_cascade(label="Formatage", menu=formatage_menu)

root.config(menu=menu_bar)

# Frame pour organiser les zones de texte d'entrée côte à côte
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5)

# Création des deux colonnes initiales
for i in range(2):
    label = tk.Label(input_frame, text=f"Colonne {i+1}:")
    label.grid(row=0, column=i, padx=5, pady=5)
    text_widget = tk.Text(input_frame, height=10, width=25)
    text_widget.grid(row=1, column=i, padx=5, pady=5)
    input_text_widgets.append(text_widget)

# Bouton pour lancer le formatage
process_button = tk.Button(root, text="Formater", command=process_text)
process_button.pack(pady=5)

# Zone de texte pour l'affichage du résultat
output_label = tk.Label(root, text="Liste de points formatée :")
output_label.pack(pady=(10, 0))
result_text = tk.Text(root, height=10, width=50)
result_text.pack(padx=10, pady=5)

root.mainloop()