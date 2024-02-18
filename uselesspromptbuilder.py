import tkinter as tk
from tkinter import ttk

def set_dark_mode_style():
    style = ttk.Style()
    style.theme_create("darkmode", parent="alt", settings={
        "TFrame": {"configure": {"background": "#333333"}},
        "TLabel": {"configure": {"background": "#333333", "foreground": "white"}},
        "TButton": {"configure": {"background": "#424242", "foreground": "white", "borderwidth": 0},
                    "map": {"background": [("active", "#535353")], "foreground": [("active", "white")]}},
        "TEntry": {"configure": {"fieldbackground": "#424242", "foreground": "white", "insertbackground": "white", "borderwidth": 0}},
    })
    style.theme_use("darkmode")

class UselessPromptBuilder:
    def __init__(self, root):
        self.root = root
        self.data = {}
        set_dark_mode_style()  # Apply dark mode styles right after initializing the app
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Useless Prompt Builder")
        self.root.configure(background='#333333')
        self.container = ttk.Frame(self.root)
        self.container.pack(fill='both', expand=True, padx=20, pady=20)
        self.pages_info = [
            ("Medium/+ opt. Mod/Main style", "which medium do you want to use? Painting, comic, 3D, photo, drawing? Any specific style you want to get? Comic, fantasy, cyberpunk, Steampunk? Optionally you can insert a mod here and the perspective can also be included.\n\n\n\nExample: 'a vivid scifi illustration, low camera angle, upper body'"),
            ("Object/Subject", "Your main motives in simple, clear words starting with 'of'\n\n\n\nExample: 'of a female astronaut'"),
            ("Details", "Details include everything that should define your main motives more clearly. Clothes, poses, hair colors, body types, etc. Here you can quickly accumulate endless tokens, but the more tokens you use, the less accurate the generated image will be in the end. So try to use tokens sparingly and think about what exactly you want.\n\n\n\nExample: 'pretty face, skintight bodysuit, helmet, futuristic, floating in space'"),
            ("Background", "This should be self-explanatory, define your background in simple terms. Less is more.\n\n\n\Example: vast galaxy background"),
            ("Mods/Embeddings", "Mods Example: 'cinematic lighting, hires, volumetric lighting, highly detailed background, masterpiece...'\n\n\n\nKeep in mind that terms like 'Insanely' or 'absurd' have no influence on the general quality and only cost unnecessary tokens.")
        ]
        self.current_page = 0
        self.create_page(self.current_page)
        
    def create_page(self, page_index):
        self.current_page = page_index
        for widget in self.container.winfo_children():
            widget.destroy()
            
        if page_index < len(self.pages_info):
            page_title, description = self.pages_info[page_index]
            ttk.Label(self.container, text=f"Enter {page_title}:").pack()
            ttk.Label(self.container, text=description, wraplength=400).pack()
            
            entry = ttk.Entry(self.container)
            entry.insert(0, self.data.get(str(page_index + 1), ""))  # Prefill with existing data if available
            entry.pack()
            
            next_button = ttk.Button(self.container, text="Next", command=lambda: self.save_data_and_advance(page_index, entry.get()))
            next_button.pack(side='right', padx=(0, 10))
            
            if page_index > 0:
                back_button = ttk.Button(self.container, text="Back", command=lambda: self.create_page(page_index - 1))
                back_button.pack(side='left')
        else:
            self.display_final_prompt()
            
    def save_data_and_advance(self, page_index, data):
        self.data[str(page_index + 1)] = data
        self.create_page(page_index + 1)
        
    def display_final_prompt(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        final_prompt = ", ".join([self.data[str(i)] for i in range(1, 6)])
        ttk.Label(self.container, text="Completed Prompt is..:").pack()
        
        prompt_label = ttk.Label(self.container, text=final_prompt, wraplength=400)
        prompt_label.pack()
        
        copy_button = ttk.Button(self.container, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(final_prompt))
        copy_button.pack(side='right', padx=(0, 10))
        
        start_over_button = ttk.Button(self.container, text="Start Over", command=lambda: self.create_page(0))
        start_over_button.pack(side='left')

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

root = tk.Tk()
app = UselessPromptBuilder(root)
root.mainloop()
