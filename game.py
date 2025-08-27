import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

# Start sound engine
pygame.mixer.init()
try:
    pygame.mixer.music.load("images1/eerie.wav")  # Your sound file
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop forever
except:
    print("Sound file not found or error in loading sound.")

# Game data
inventory = []

# Scenes with storyline and options
scenes = {
    "intro": {
        "image": "images1/intro.png",
        "text": "You wake up in a desolate city, the air thick with ash. There's a faint glow on the horizon.",
        "choices": [
            {"text": "Explore the ruins", "next": "ruins"},
            {"text": "Enter the nearby bunker", "next": "bunker"}
        ]
    },
    "ruins": {
        "image": "images1/ruins.png",
        "text": "Twisted metal and echoes of the past surround you. You might find something useful.",
        "choices": [
            {"text": "Search the area", "next": "found_item"},
            {"text": "Head back", "next": "intro"}
        ]
    },
    "bunker": {
        "image": "images1/bunker.png",
        "text": "The bunker door creaks open. It's dark, but you hear something inside.",
        "choices": [
            {"text": "Enter the darkness", "next": "random_event"},
            {"text": "Close the door and leave", "next": "intro"}
        ]
    },
    "found_item": {
        "image": "images1/inventory.png",
        "text": "You found an old ration pack and a flashlight!",
        "choices": [
            {"text": "Take items and go to bunker", "next": "bunker"}
        ],
        "items": ["ration pack", "flashlight"]
    },
    "random_event": {
        "image": None,
        "text": None,
        "choices": []
    },
    "trader": {
        "image": "images1/trader.png",
        "text": "A wandering trader offers you a mysterious device in exchange for your flashlight.",
        "choices": [
            {"text": "Trade flashlight for device", "next": "escape"},
            {"text": "Refuse and move on", "next": "trapped"}
        ]
    },
    "enemy": {
        "image": "images1/enemy.png",
        "text": "A shadowy figure lunges from the darkness!",
        "choices": [
            {"text": "Fight", "next": "death"},
            {"text": "Run", "next": "trapped"}
        ]
    },
    "escape": {
        "image": "images1/escape.png",
        "text": "You escape the ruins with your life and a strange device that glows warmly.",
        "choices": []
    },
    "trapped": {
        "image": "images1/trapped.png",
        "text": "You get trapped in a collapsed tunnel. This might be the end.",
        "choices": [
            {"text": "Die", "next": "death"},
            {"text": "Try once again", "next": "devil_fight"}
        ]
    },
    "devil_fight": {
        "image": "images1/demon.png",
        "text": "A devil blocks your way. You feel fear, but also a spark of courage.",
        "choices": [
            {"text": "Fight", "next": "victory"},
            {"text": "Run back to tunnel", "next": "death"}
        ]
    },
    "victory": {
        "image": "images1/victory.png",
        "text": "You defeat the devil. Atlast courage wins",
        "choices": []
    },
    "death": {
        "image": "images1/death.png",
        "text": "The creature was too strong. Darkness consumes you.",
        "choices": []
    }
}

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Wasteland Survival RPG")
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.bg = tk.Label(root)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.text_box = tk.Label(root, text="", wraplength=760, justify="center",font=("Helvetica", 14), bg="#000", fg="#FFF")
        self.text_box.place(x=20, y=420, width=760, height=100)

        self.button_area = tk.Frame(root, bg="#222")
        self.button_area.place(x=20, y=530, width=760, height=60)

        self.inv_button = tk.Button(root, text="Inventory", command=self.show_inventory)
        self.inv_button.place(x=700, y=20)

        self.current = "intro"
        self.show_scene(self.current)

    def show_inventory(self):
        stuff = ", ".join(inventory) if inventory else "Empty"
        messagebox.showinfo("Inventory", f"Your inventory contains: {stuff}")

    def clear_buttons(self):
        for item in self.button_area.winfo_children():
            item.destroy()

    def show_scene(self, key):
        scene = scenes[key]

        # Handle random event
        if key == "random_event":
            next_scene = random.choice(["trader", "enemy"])
            self.show_scene(next_scene)
            return

        self.current = key
        self.clear_buttons()

        # Show background
        if scene["image"]:
            try:
                image = Image.open(scene["image"])
                image = image.resize((800, 600))
                self.photo = ImageTk.PhotoImage(image)
                self.bg.config(image=self.photo)
            except:
                self.bg.config(image="")
        else:
            self.bg.config(image="")

        # Set text
        self.text_box.config(text=scene["text"])

        # Add items if found
        if "items" in scene:
            for item in scene["items"]:
                if item not in inventory:
                    inventory.append(item)

        # Show choices
        for option in scene["choices"]:
            btn = tk.Button(self.button_area, text=option["text"],
                            command=lambda n=option["next"]: self.show_scene(n))
            btn.pack(side="left", padx=10)

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
