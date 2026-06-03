import tkinter as tk
from tkinter import messagebox
import re
import random
import string

# ==========================================
# DESIGN SYSTEM & CONSTANTS
# ==========================================
FONT_TITLE = ("Helvetica Neue", 18, "bold")
FONT_SUBTITLE = ("Helvetica Neue", 10, "normal")
FONT_LABEL = ("Helvetica Neue", 11, "bold")
FONT_INPUT = ("Consolas", 13)
FONT_BUTTON = ("Helvetica Neue", 11, "bold")
FONT_FEEDBACK = ("Helvetica Neue", 14, "bold")
FONT_CHECKLIST = ("Helvetica Neue", 11, "normal")

# Colors
COLOR_BG = "#1E1E2E"         # Sleek dark window background
COLOR_CARD = "#252538"       # Slightly lighter card background
COLOR_INPUT_BG = "#181825"   # Dark input field background
COLOR_BORDER = "#313244"     # Thin borders
COLOR_TEXT_MAIN = "#CDD6F4"  # High contrast text
COLOR_TEXT_MUTED = "#A6ADC8" # Low contrast secondary text
COLOR_ACCENT = "#89B4FA"     # Pastel blue accent

COLOR_WEAK = "#F38BA8"       # Modern Red
COLOR_MEDIUM = "#FAB387"     # Modern Peach/Orange
COLOR_STRONG = "#A6E3A1"     # Modern Green
COLOR_VSTRONG = "#94E2D5"    # Modern Teal
COLOR_DISABLED = "#45475A"   # Muted grey for unfulfilled segments

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity | Password Shield")
        self.root.configure(bg=COLOR_BG)
        
        # Set fixed size and center on screen
        self.window_width = 460
        self.window_height = 680
        self.center_window()
        
        # State variables
        self.show_password_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar()
        
        # Trace variable changes for real-time validation
        self.password_var.trace_add("write", self.on_password_change)
        
        # Build the Interface
        self.create_widgets()
        self.update_ui(0, {})

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)

    def create_widgets(self):
        # 1. HEADER SECTION
        header_frame = tk.Frame(self.root, bg=COLOR_BG)
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # Shield Emoji / Icon representation
        self.icon_label = tk.Label(
            header_frame, 
            text="🛡️", 
            font=("Segoe UI Emoji", 32), 
            bg=COLOR_BG, 
            fg=COLOR_ACCENT
        )
        self.icon_label.pack()
        
        self.title_label = tk.Label(
            header_frame, 
            text="PASSWORD SHIELD", 
            font=FONT_TITLE, 
            bg=COLOR_BG, 
            fg=COLOR_TEXT_MAIN
        )
        self.title_label.pack(pady=(5, 2))
        
        self.subtitle_label = tk.Label(
            header_frame, 
            text="Evaluate and strengthen your digital security", 
            font=FONT_SUBTITLE, 
            bg=COLOR_BG, 
            fg=COLOR_TEXT_MUTED
        )
        self.subtitle_label.pack()

        # 2. INPUT CARD
        card_frame = tk.Frame(self.root, bg=COLOR_CARD, bd=1, relief="flat")
        card_frame.pack(fill="x", padx=30, pady=0)
        
        # Inner padding for card
        inner_padding = tk.Frame(card_frame, bg=COLOR_CARD)
        inner_padding.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Input Label
        input_label = tk.Label(
            inner_padding, 
            text="ENTER PASSWORD", 
            font=FONT_LABEL, 
            bg=COLOR_CARD, 
            fg=COLOR_TEXT_MUTED
        )
        input_label.pack(anchor="w", pady=(0, 8))
        
        # Password Entry Container (to hold Entry and Show/Hide button)
        entry_container = tk.Frame(
            inner_padding, 
            bg=COLOR_INPUT_BG, 
            highlightbackground=COLOR_BORDER,
            highlightcolor=COLOR_ACCENT,
            highlightthickness=1,
            bd=0
        )
        entry_container.pack(fill="x", ipady=4)
        
        self.password_entry = tk.Entry(
            entry_container, 
            textvariable=self.password_var,
            font=FONT_INPUT,
            bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT_MAIN,
            bd=0,
            insertbackground=COLOR_TEXT_MAIN, # Cursor color
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=12, pady=6)
        
        # Show/Hide Toggle Button
        self.toggle_btn = tk.Button(
            entry_container,
            text="Show",
            font=FONT_SUBTITLE,
            bg=COLOR_INPUT_BG,
            fg=COLOR_ACCENT,
            activebackground=COLOR_INPUT_BG,
            activeforeground=COLOR_TEXT_MAIN,
            bd=0,
            cursor="hand2",
            command=self.toggle_password_visibility
        )
        self.toggle_btn.pack(side="right", padx=10)

        # 3. VISUAL STRENGTH METER (PROGRESS BAR)
        self.meter_canvas = tk.Canvas(
            inner_padding, 
            height=14, 
            bg=COLOR_CARD, 
            bd=0, 
            highlightthickness=0
        )
        self.meter_canvas.pack(fill="x", pady=(20, 10))
        self.meter_canvas.bind("<Configure>", lambda e: self.on_password_change())

        # 4. RESULT BANNER
        self.result_frame = tk.Frame(inner_padding, bg=COLOR_CARD)
        self.result_frame.pack(fill="x", pady=5)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="WEAK",
            font=FONT_FEEDBACK,
            bg=COLOR_CARD,
            fg=COLOR_WEAK
        )
        self.result_label.pack(anchor="center")

        # 5. REQUIREMENTS CHECKLIST CARD
        checklist_card = tk.Frame(self.root, bg=COLOR_CARD)
        checklist_card.pack(fill="both", expand=True, padx=30, pady=(20, 20))
        
        checklist_padding = tk.Frame(checklist_card, bg=COLOR_CARD)
        checklist_padding.pack(fill="both", expand=True, padx=20, pady=20)
        
        checklist_title = tk.Label(
            checklist_padding,
            text="SECURITY CRITERIA",
            font=FONT_LABEL,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MUTED
        )
        checklist_title.pack(anchor="w", pady=(0, 12))

        # Checklist Items
        self.criteria_widgets = {}
        self.criteria_list = [
            ("length", "At least 8 characters long"),
            ("uppercase", "Contains uppercase letters (A-Z)"),
            ("lowercase", "Contains lowercase letters (a-z)"),
            ("numbers", "Contains numbers (0-9)"),
            ("special", "Contains special characters (e.g., ! @ # $ %)")
        ]
        
        for key, text in self.criteria_list:
            item_frame = tk.Frame(checklist_padding, bg=COLOR_CARD)
            item_frame.pack(fill="x", pady=4)
            
            # Indicator sign (✗ or ✓)
            indicator = tk.Label(
                item_frame, 
                text="✗", 
                font=("Segoe UI Symbol", 12, "bold"), 
                bg=COLOR_CARD, 
                fg=COLOR_WEAK,
                width=3
            )
            indicator.pack(side="left")
            
            # Criterion Label
            lbl = tk.Label(
                item_frame, 
                text=text, 
                font=FONT_CHECKLIST, 
                bg=COLOR_CARD, 
                fg=COLOR_TEXT_MUTED
            )
            lbl.pack(side="left", padx=8)
            
            self.criteria_widgets[key] = {
                "indicator": indicator,
                "label": lbl
            }

        # 6. ACTION BUTTONS FRAME
        action_frame = tk.Frame(self.root, bg=COLOR_BG)
        action_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        # Primary Action: Check Password
        self.check_btn = tk.Button(
            action_frame,
            text="Check Password",
            font=FONT_BUTTON,
            bg=COLOR_ACCENT,
            fg=COLOR_BG,
            activebackground="#A6E3A1", # Light green on hover active
            activeforeground=COLOR_BG,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.on_check_button_click
        )
        self.check_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Secondary Action: Generator
        self.gen_btn = tk.Button(
            action_frame,
            text="Generate Secure",
            font=FONT_BUTTON,
            bg=COLOR_CARD,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_INPUT_BG,
            activeforeground=COLOR_TEXT_MAIN,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            cursor="hand2",
            padx=15,
            pady=10,
            command=self.generate_password
        )
        self.gen_btn.pack(side="right", fill="x", expand=True, padx=(8, 0))

    # ==========================================
    # LOGIC AND EVENT HANDLERS
    # ==========================================
    
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="Show", fg=COLOR_ACCENT)
            self.show_password_var.set(False)
        else:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="Hide", fg=COLOR_TEXT_MUTED)
            self.show_password_var.set(True)

    def evaluate_password(self, password):
        if not password:
            return 0, {k: False for k in ["length", "uppercase", "lowercase", "numbers", "special"]}
            
        metrics = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "numbers": any(c.isdigit() for c in password),
            "special": any(not c.isalnum() for c in password)
        }
        
        # Scoring logic
        score = sum(metrics.values())
        return score, metrics

    def on_password_change(self, *args):
        password = self.password_var.get()
        score, metrics = self.evaluate_password(password)
        self.update_ui(score, metrics)

    def on_check_button_click(self):
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Empty Password", "Please enter or generate a password first.")
            return
            
        score, metrics = self.evaluate_password(password)
        self.update_ui(score, metrics)
        
        # Display custom dialog report
        strength_levels = {
            0: ("Weak", COLOR_WEAK),
            1: ("Weak", COLOR_WEAK),
            2: ("Weak", COLOR_WEAK),
            3: ("Medium", COLOR_MEDIUM),
            4: ("Strong", COLOR_STRONG),
            5: ("Very Strong", COLOR_VSTRONG)
        }
        
        level_str, color = strength_levels[score]
        
        # If length is not met, cap at Medium even if other requirements are met
        if not metrics["length"] and score >= 3:
            level_str = "Weak"
            color = COLOR_WEAK
            
        suggestions = []
        if not metrics["length"]:
            suggestions.append("• Make it at least 8 characters long.")
        if not metrics["uppercase"]:
            suggestions.append("• Add uppercase letters (A-Z).")
        if not metrics["lowercase"]:
            suggestions.append("• Add lowercase letters (a-z).")
        if not metrics["numbers"]:
            suggestions.append("• Include at least one number (0-9).")
        if not metrics["special"]:
            suggestions.append("• Include special characters (e.g. @, #, $, %).")
            
        report_msg = f"Password: {'*' * len(password) if not self.show_password_var.get() else password}\n"
        report_msg += f"Strength Level: {level_str.upper()}\n\n"
        
        if suggestions:
            report_msg += "Suggestions for improvement:\n" + "\n".join(suggestions)
        else:
            report_msg += "Excellent! Your password meets all security guidelines."
            
        messagebox.showinfo("Password Strength Report", report_msg)

    def generate_password(self):
        # Generate a premium quality 16-character secure password
        length = 16
        
        # Guarantee at least one character from each set
        chars_upper = string.ascii_uppercase
        chars_lower = string.ascii_lowercase
        chars_digits = string.digits
        chars_special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        all_chars = chars_upper + chars_lower + chars_digits + chars_special
        
        pw_list = [
            random.choice(chars_upper),
            random.choice(chars_lower),
            random.choice(chars_digits),
            random.choice(chars_special)
        ]
        
        # Fill rest of length
        for _ in range(length - 4):
            pw_list.append(random.choice(all_chars))
            
        # Shuffle to mix guaranteed positions
        random.shuffle(pw_list)
        generated_pw = "".join(pw_list)
        
        # Set field
        self.password_var.set(generated_pw)
        
        # Auto-focus the entry field
        self.password_entry.focus()

    def update_ui(self, score, metrics):
        # Determine classification and colors
        if not self.password_var.get():
            level_str = "EMPTY"
            color = COLOR_TEXT_MUTED
            filled_segments = 0
        else:
            # Enforce that length must be met for a password to be Medium or higher
            is_length_ok = metrics.get("length", False)
            
            if score <= 2:
                level_str = "WEAK"
                color = COLOR_WEAK
                filled_segments = 1
            elif score == 3:
                if is_length_ok:
                    level_str = "MEDIUM"
                    color = COLOR_MEDIUM
                    filled_segments = 2
                else:
                    level_str = "WEAK"
                    color = COLOR_WEAK
                    filled_segments = 1
            elif score == 4:
                if is_length_ok:
                    level_str = "STRONG"
                    color = COLOR_STRONG
                    filled_segments = 3
                else:
                    level_str = "WEAK"
                    color = COLOR_WEAK
                    filled_segments = 1
            else: # score == 5
                level_str = "VERY STRONG"
                color = COLOR_VSTRONG
                filled_segments = 4

        # Update Result label
        self.result_label.configure(text=level_str, fg=color)
        
        # Draw custom visual strength bar
        self.draw_strength_meter(filled_segments, color)
        
        # Update requirement checklist signs & colors
        for key, text in self.criteria_list:
            widget = self.criteria_widgets[key]
            satisfied = metrics.get(key, False) if self.password_var.get() else False
            
            if satisfied:
                widget["indicator"].configure(text="✓", fg=COLOR_STRONG)
                widget["label"].configure(fg=COLOR_TEXT_MAIN)
            else:
                widget["indicator"].configure(text="✗", fg=COLOR_WEAK if self.password_var.get() else COLOR_DISABLED)
                widget["label"].configure(fg=COLOR_TEXT_MUTED)

    def draw_strength_meter(self, filled_segments, color):
        self.meter_canvas.delete("all")
        
        # Fetch actual width dynamically to support packing layout
        width = self.meter_canvas.winfo_width()
        if width <= 1:
            width = 400 # Fallback width during init
            
        segment_count = 4
        spacing = 6
        segment_width = (width - (spacing * (segment_count - 1))) / segment_count
        
        for i in range(segment_count):
            x1 = i * (segment_width + spacing)
            y1 = 0
            x2 = x1 + segment_width
            y2 = 12
            
            fill_color = color if i < filled_segments else COLOR_DISABLED
            
            # Draw segment with flat modern aesthetic
            self.draw_rounded_rect(x1, y1, x2, y2, radius=4, fill=fill_color)

    def draw_rounded_rect(self, x1, y1, x2, y2, radius=4, fill=""):
        # Helper to draw beautiful rounded corners on standard canvas
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.meter_canvas.create_polygon(points, smooth=True, fill=fill)

# ==========================================
# APPLICATION ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()
