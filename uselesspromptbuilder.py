import customtkinter as ctk
from tkinter import PhotoImage, messagebox, scrolledtext, Toplevel
import threading
import time

# Configure customtkinter
ctk.set_appearance_mode("dark")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")

def show_splash_screen(duration=3000): #note: idk why but there is some text i thought i removed on the splash screen that is still there. idk lol i suck with code.
    splash_root = ctk.CTk()
    splash_root.overrideredirect(True)
    splash_root.geometry("600x400")
    
    splash_image = PhotoImage(file=r'D:\Documents\HACKY STUFF\UselessPromptBuilder\uselesssplash.png')
    splash_label = ctk.CTkLabel(splash_root, image=splash_image)
    splash_label.image = splash_image
    splash_label.pack(expand=True)
    
    splash_root.update()
    time.sleep(duration / 1000)
    splash_root.destroy()


class UselessPromptBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'D:\Documents\HACKY STUFF\UselessPromptBuilder\uselessicon.ico')
        self.title("Useless Prompt Builder")
        self.geometry("800x600")

        self.data = {}
        self.completed_prompts = []  # This will store the prompts
        self.setup_ui()
        
    def setup_ui(self):
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.pages_info = [
            ("Medium/+ opt. Mod/Main style", "Which medium do you want to use? Painting, comic, 3D, photo, drawing? Any specific style you want to get? Comic, fantasy, cyberpunk, Steampunk? Optionally you can insert a mod here and the perspective can also be included.\n\nExample: 'a vivid sci-fi illustration, low camera angle, upper body'"),
            ("Object/Subject", "Your main motives in simple, clear words starting with 'of'.\n\nExample: 'of a female astronaut'"),
            ("Details", "Details include everything that should define your main motives more clearly. Clothes, poses, hair colors, body types, etc. Here you can quickly accumulate endless tokens, but the more tokens you use, the less accurate the generated image will be in the end. So try to use tokens sparingly and think about what exactly you want.\n\nExample: 'pretty face, skintight bodysuit, helmet, futuristic, floating in space'"),
            ("Background", "This should be self-explanatory, define your background in simple terms. Less is more.\n\nExample: 'vast galaxy background'"),
            ("Mods/Embeddings", "Mods Example: 'cinematic lighting, hires, volumetric lighting, highly detailed background, masterpiece...'\n\nKeep in mind that terms like 'Insanely' or 'absurd' have no influence on the general quality and only cost unnecessary tokens.")
        ]
        self.current_page = 0
        self.create_page(self.current_page)
        
    def center_window(self, width=800, height=600):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
    def go_back(self, page_index, data):
        self.data[page_index] = data  # Save the current input.

    def create_page(self, page_index):
        for widget in self.container.winfo_children():
            widget.destroy()

        if page_index < len(self.pages_info):
            page_title, description = self.pages_info[page_index]
            ctk.CTkLabel(self.container, text=page_title, wraplength=400).pack(pady=10)
            ctk.CTkLabel(self.container, text=description, wraplength=400).pack()

            entry = ctk.CTkEntry(self.container, width=400)
            entry.pack(pady=10)
            
            if page_index in self.data:
                entry.insert(0, self.data[page_index])

            next_button = ctk.CTkButton(self.container, text="Next",
                            command=lambda: self.save_data_and_advance(page_index, entry.get()))
            next_button.pack(side='right', padx=(0, 10))

            if page_index > 0:
                back_button = ctk.CTkButton(self.container, text="Back", command=lambda: self.create_page(page_index - 1))
                back_button.pack(side='left')
        else:
            self.display_final_prompt()

    def save_data_and_advance(self, page_index, data):
        self.data[str(page_index + 1)] = data.strip()
        self.completed_prompts.append(data.strip())
        self.data[page_index] = data
        print("Current completed prompts:", self.completed_prompts)
        next_page = page_index + 1

        if next_page < len(self.pages_info):
            self.create_page(next_page)
        else:
            self.display_final_prompt()
    

    def display_final_prompt(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        final_prompt = ", ".join([self.data[str(i)] for i in range(1, len(self.pages_info) + 1)])
        prompt_label = ctk.CTkLabel(self.container, text="Completed Prompt:", wraplength=400)
        prompt_label.pack()        

        prompt_text = scrolledtext.ScrolledText(self.container, wrap='word', height=10)
        prompt_text.pack(fill='both', expand=True, padx=20, pady=10)
        prompt_text.insert('end', final_prompt)
        prompt_text.config(state='disabled', bg="#2e2e2e", fg="white", insertbackground="white")

        copy_button = ctk.CTkButton(self.container, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(final_prompt))
        copy_button.pack(side='right', padx=(0, 10))

        start_over_button = ctk.CTkButton(self.container, text="Start Over", command=self.start_over)
        start_over_button.pack(side='left')

    def start_over(self):
        self.data = {}
        self.current_page = 0
        self.create_page(self.current_page)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo(title="Success", message="Prompt copied to clipboard!")
        
    def load_prompts_from_file(self):
        """Load completed prompts from a file."""
        try:
            with open("completed_prompts.txt", "r") as file:
                self.completed_prompts = [line.strip().replace("|||", "\n") for line in file.readlines()]
        except FileNotFoundError:
            self.completed_prompts = []                

if __name__ == "__main__":
    show_splash_screen(3000)
    app = UselessPromptBuilder()
    app.mainloop()
