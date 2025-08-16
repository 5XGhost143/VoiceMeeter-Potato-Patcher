import tkinter as tk
from tkinter import messagebox
import threading
from patcher import VoiceMeeterPatcher

class VoiceMeeterPatcherUI:
    def __init__(self, root):
        self.root = root
        self.patcher = VoiceMeeterPatcher()
        self.is_patching = False
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.root.title("VoiceMeeter Patcher")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#0a0a0a')
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400)
        y = (self.root.winfo_screenheight() // 2) - (250)
        self.root.geometry(f'800x500+{x}+{y}')
    
    def create_shadow_text(self, parent, text, x, y, font, shadow_color='#333333', text_color='#ffffff'):
        shadow = tk.Label(parent, text=text, font=font, 
                         fg=shadow_color, bg='#0a0a0a')
        shadow.place(x=x+3, y=y+3)
        
        # Main text
        main_text = tk.Label(parent, text=text, font=font, 
                            fg=text_color, bg='#0a0a0a')
        main_text.place(x=x, y=y)
        
        return main_text, shadow
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=50, pady=40)
        
        self.create_shadow_text(main_frame, "VoiceMeeter", 80, 30, 
                               ('Arial', 56, 'bold'), '#1a1a1a', '#00ff88')
        
        self.create_shadow_text(main_frame, "Patcher", 380, 100, 
                               ('Arial', 40, 'bold'), '#1a1a1a', '#ffffff')
        
        self.status_var = tk.StringVar(value="Ready to patch")
        self.status_label = tk.Label(main_frame, textvariable=self.status_var,
                                    font=('Arial', 14),
                                    fg='#888888', bg='#0a0a0a')
        self.status_label.place(x=80, y=180)
        
        self.create_patch_button(main_frame)
        
        info_frame = tk.Frame(main_frame, bg='#0a0a0a')
        info_frame.place(x=80, y=420)
        
        tk.Label(info_frame, text=f"Module: {self.patcher.get_module_name()}",
                font=('Consolas', 11), fg='#666666', bg='#0a0a0a').pack(anchor='w')
    
    def create_patch_button(self, parent):
        
        self.patch_button = tk.Button(parent, text="PATCH",
                                     font=('Arial', 28, 'bold'),
                                     width=16, height=2,
                                     bg='#00ff88', fg='#000000',
                                     bd=3, relief='raised',
                                     cursor='hand2',
                                     command=self.patch_clicked,
                                     activebackground='#00dd77',
                                     activeforeground='#000000')
        self.patch_button.place(x=150, y=270)
        
        self.patch_button.bind('<Enter>', self.on_button_hover)
        self.patch_button.bind('<Leave>', self.on_button_leave)
    
    def on_button_hover(self, event):
        if not self.is_patching:
            self.patch_button.configure(bg='#00dd77', fg='#000000')
    
    def on_button_leave(self, event):
        if not self.is_patching:
            self.patch_button.configure(bg='#00ff88', fg='#000000')
    
    def update_status(self, message, color='#888888'):
        self.status_var.set(message)
        self.status_label.configure(fg=color)
        self.root.update()
    
    def patch_clicked(self):
        if not self.is_patching:
            threading.Thread(target=self.apply_patch_async, daemon=True).start()
    
    def apply_patch_async(self):
        self.is_patching = True
        
        self.patch_button.configure(text="PATCHING...", bg='#ffaa00', state='disabled')
        self.update_status("Applying patch...", '#ffaa00')
        
        try:
            if self.patcher.check_status():
                self.update_status("Already patched!", '#ffaa00')
                messagebox.showwarning("Already Patched", 
                                     "VoiceMeeter is already patched!")
            else:
                result = self.patcher.apply_patch()
                
                if result == "success":
                    self.update_status("Patch applied successfully!", '#00ff88')
                    messagebox.showinfo("Sucess", 
                                      "✅ Patch applied successfully!")
                elif result == "already_patched":
                    self.update_status("Already patched!", '#ffaa00')
                    messagebox.showwarning("Failed", 
                                         "VoiceMeeter is already patched!")
                    
        except Exception as e:
            self.update_status("Patch failed!", '#ff4444')
            messagebox.showerror("Error", f"Patching failed:\n\n{str(e)}")
        
        finally:
            self.patch_button.configure(text="PATCH", bg='#00ff88', state='normal')
            self.is_patching = False
            self.root.after(3000, lambda: self.update_status("Ready to patch"))
