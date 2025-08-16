import tkinter as tk
from tkinter import messagebox
import sys
import os
from ui import VoiceMeeterPatcherUI

def main():
    try:
        root = tk.Tk()
        
        try:
            if os.path.exists('icon.ico'):
                root.iconbitmap('icon.ico')
        except:
            pass
        
        app = VoiceMeeterPatcherUI(root)
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Startup Error", 
                           f"Failed to start the application:\n\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
