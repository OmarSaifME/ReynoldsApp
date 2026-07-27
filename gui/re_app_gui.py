# gui/re_app_gui.py - V2 TABBED FOUNDATION
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules (AOA for now, Reynolds will join the party)
from core.Angle_of_Attack import calculate_aoa_components
from core.reynolds import re_to_velocity, velocity_to_re
from core.gci import calculate_gci as calculate_gci_core

# from core.reynolds import calculate_reynolds  # Ready for V2!


def copy_to_clipboard(text):
    """Copy text to clipboard."""
    app.clipboard_clear()
    app.clipboard_append(text)
    #status_label.config(text=f"✓ Copied to clipboard!")


def build_aoa_tab(parent):
    """Build the Angle of Attack calculator UI in the given parent frame."""

    def calculate_aoa():
        """AOA-specific calculation."""
        try:
            angle = float(angle_entry.get())
            velocity = float(velocity_entry.get())
            results = calculate_aoa_components(angle, velocity)

            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()

            # ===== DISPLAY BASIC PARAMETERS =====
            basic_params = ['Angle of Attack (deg)', 'Flow Velocity (m/s)',
                            'Velocity Component for X (m/s)', 'Velocity Component for Y (m/s)']
            row = 0
            for key in basic_params:
                value = results[key]

                tk.Label(results_frame, text=f"{key}:", font=("Arial", 10, "bold")) \
                    .grid(row=row, column=0, sticky="w", padx=5, pady=2)

                result_box = tk.Entry(results_frame, width=25, font=("Courier", 10))
                result_box.insert(0, value)
                result_box.config(state="readonly")
                result_box.grid(row=row, column=1, padx=5, pady=2)

                tk.Button(results_frame, text="📋 Copy",
                          command=lambda v=value: copy_to_clipboard(v)) \
                    .grid(row=row, column=2, padx=5, pady=2)

                row += 1

            # ===== SEPARATOR ===== (NOW OUTSIDE THE LOOP!)
            sep = ttk.Separator(results_frame, orient='horizontal')
            sep.grid(row=row, column=0, columnspan=3, sticky="ew", pady=10)
            row += 1

            # ===== DRAG FORCE VECTOR - SIDE BY SIDE ===== (NOW OUTSIDE THE LOOP!)
            drag_label = tk.Label(results_frame, text="Drag Force Vector:",
                                  font=("Arial", 10, "bold"), fg="#D32F2F")
            drag_label.grid(row=row, column=0, columnspan=6, sticky="w", padx=5, pady=2)
            row += 1

            # Create a sub-frame for drag components
            drag_frame = tk.Frame(results_frame)
            drag_frame.grid(row=row, column=0, columnspan=6, sticky="w", padx=20)

            # Drag X
            tk.Label(drag_frame, text="X:", font=("Arial", 9)).pack(side="left", padx=(0, 5))
            drag_x_box = tk.Entry(drag_frame, width=20, font=("Courier", 9))
            drag_x_box.insert(0, results['drag_x'])
            drag_x_box.config(state="readonly")
            drag_x_box.pack(side="left", padx=(0, 5))

            drag_x_btn = tk.Button(drag_frame, text="📋 Copy",
                                   command=lambda: copy_to_clipboard(results['drag_x']))
            drag_x_btn.pack(side="left", padx=(0, 20))

            # Drag Y
            tk.Label(drag_frame, text="Y:", font=("Arial", 9)).pack(side="left", padx=(0, 5))
            drag_y_box = tk.Entry(drag_frame, width=20, font=("Courier", 9))
            drag_y_box.insert(0, results['drag_y'])
            drag_y_box.config(state="readonly")
            drag_y_box.pack(side="left", padx=(0, 5))

            drag_y_btn = tk.Button(drag_frame, text="📋 Copy",
                                   command=lambda: copy_to_clipboard(results['drag_y']))
            drag_y_btn.pack(side="left")

            row += 1

            # ===== LIFT FORCE VECTOR - SIDE BY SIDE ===== (NOW OUTSIDE THE LOOP!)
            lift_label = tk.Label(results_frame, text="Lift Force Vector:",
                                  font=("Arial", 10, "bold"), fg="#1976D2")
            lift_label.grid(row=row, column=0, columnspan=6, sticky="w", padx=5, pady=(15, 2))
            row += 1

            # Create a sub-frame for lift components
            lift_frame = tk.Frame(results_frame)
            lift_frame.grid(row=row, column=0, columnspan=6, sticky="w", padx=20)

            # Lift X
            tk.Label(lift_frame, text="X:", font=("Arial", 9)).pack(side="left", padx=(0, 5))
            lift_x_box = tk.Entry(lift_frame, width=20, font=("Courier", 9))
            lift_x_box.insert(0, results['lift_x'])
            lift_x_box.config(state="readonly")
            lift_x_box.pack(side="left", padx=(0, 5))

            lift_x_btn = tk.Button(lift_frame, text="📋 Copy",
                                   command=lambda: copy_to_clipboard(results['lift_x']))
            lift_x_btn.pack(side="left", padx=(0, 20))

            # Lift Y
            tk.Label(lift_frame, text="Y:", font=("Arial", 9)).pack(side="left", padx=(0, 5))
            lift_y_box = tk.Entry(lift_frame, width=20, font=("Courier", 9))
            lift_y_box.insert(0, results['lift_y'])
            lift_y_box.config(state="readonly")
            lift_y_box.pack(side="left", padx=(0, 5))

            lift_y_btn = tk.Button(lift_frame, text="📋 Copy",
                                   command=lambda: copy_to_clipboard(results['lift_y']))
            lift_y_btn.pack(side="left")

            row += 1

            # Clear any error messages
            error_label.config(text="")
            # status_label.config(text="✓ AoA Settings Calculated!")

        except ValueError:
            # Handle bad input (non-numbers)
            error_label.config(text="⚠️ Enter valid numbers!")
            status_label.config(text="")

        except ValueError:
            error_label.config(text="⚠️ Enter valid numbers!")

    # === AOA UI Elements ===
    # Input frame
    input_frame = ttk.Frame(parent)
    input_frame.pack(pady=10)

    ttk.Label(input_frame, text="Angle of Attack (degrees):") \
        .grid(row=0, column=0, padx=5)
    angle_entry = ttk.Entry(input_frame, width=15)
    angle_entry.grid(row=0, column=1, padx=5)
    angle_entry.insert(0, "5.0")

    ttk.Label(input_frame, text="Flow Velocity (m/s):") \
        .grid(row=1, column=0, padx=5, pady=5)
    velocity_entry = ttk.Entry(input_frame, width=15)
    velocity_entry.grid(row=1, column=1, padx=5, pady=5)
    velocity_entry.insert(0, "10.0")

    # Create button
    calc_button = tk.Button(parent,
        text="Calculate",
        command=calculate_aoa,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        relief="raised",
        bd=2,
        activebackground="#45a049",
        activeforeground="white",
        cursor="hand2")

    # Pack it separately
    calc_button.pack(pady=10)

    # Error label (specific to AOA)
    global error_label  # We'll make this better in V3
    error_label = ttk.Label(parent, text="", foreground="red")
    error_label.pack()

    # Results frame
    results_frame = ttk.Frame(parent)
    results_frame.pack(pady=10, padx=10, fill="both", expand=True)

    return results_frame  # Return so other tabs can use similar pattern


def build_reynolds_tab(parent):
    """Build the Reynolds Number calculator UI."""

    # Variables
    mode_var = tk.StringVar(value="vel_to_Re")  # Default: Velocity → Re

    # Input fields (will be dynamically shown/hidden)
    vel_entry = None
    re_entry = None
    length_entry = None
    density_entry = None
    viscosity_entry = None
    results_frame = None
    error_label = None

    def toggle_mode(*args):
        """Show/hide input fields based on selected mode."""
        mode = mode_var.get()

        # Clear previous results when mode changes
        if results_frame:
            for widget in results_frame.winfo_children():
                widget.destroy()

        # Show/hide appropriate labels and entries
        if mode == "vel_to_Re":
            vel_label.grid()
            vel_entry.grid()
            re_label.grid_remove()
            re_entry.grid_remove()
        else:  # Re_to_vel
            vel_label.grid_remove()
            vel_entry.grid_remove()
            re_label.grid()
            re_entry.grid()

    def calculate_reynolds():
        """Perform Reynolds calculation based on selected mode."""
        try:
            mode = mode_var.get()

            # Get common inputs
            length = float(length_entry.get())
            density = float(density_entry.get())
            viscosity = float(viscosity_entry.get())

            if mode == "vel_to_Re":
                velocity = float(vel_entry.get())
                results = velocity_to_re(velocity, length, density, viscosity)
            else:  # Re_to_vel
                reynolds = float(re_entry.get())
                results = re_to_velocity(reynolds, length, density, viscosity)

            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()

            # Display results
            row = 0
            for key, value in results.items():
                # Skip mode (we already show it via radio buttons)
                if key == 'Mode':
                    continue

                tk.Label(results_frame, text=f"{key}:",
                         font=("Arial", 10, "bold")) \
                    .grid(row=row, column=0, sticky="w", padx=5, pady=2)

                result_box = tk.Entry(results_frame, width=25, font=("Courier", 10))
                result_box.insert(0, value)
                result_box.config(state="readonly")
                result_box.grid(row=row, column=1, padx=5, pady=2)

                tk.Button(results_frame, text="📋 Copy",
                          command=lambda v=value: copy_to_clipboard(v)) \
                    .grid(row=row, column=2, padx=5, pady=2)

                row += 1

            if error_label:
                error_label.config(text="")

        except ValueError:
            if error_label:
                error_label.config(text="⚠️ Enter valid numbers!")
        except Exception as e:
            if error_label:
                error_label.config(text=f"⚠️ Error: {str(e)}")

    # ===== UI CONSTRUCTION =====

    # Mode selection frame
    mode_frame = ttk.Frame(parent)
    mode_frame.pack(pady=10)

    ttk.Label(mode_frame, text="Module:", font=("Arial", 10, "bold")) \
        .pack(side="left", padx=5)

    ttk.Radiobutton(mode_frame, text="Velocity → Re",
                    variable=mode_var, value="vel_to_Re",
                    command=toggle_mode).pack(side="left", padx=5)

    ttk.Radiobutton(mode_frame, text="Re → Velocity",
                    variable=mode_var, value="Re_to_vel",
                    command=toggle_mode).pack(side="left", padx=15)

    # Input frame
    input_frame = ttk.Frame(parent)
    input_frame.pack(pady=10)

    # Common inputs (always visible)
    row = 0
    ttk.Label(input_frame, text="Characteristic Length (m):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    length_entry = ttk.Entry(input_frame, width=15)
    length_entry.grid(row=row, column=1, padx=5, pady=2)
    length_entry.insert(0, "0.5")  # Default chord length
    row += 1

    ttk.Label(input_frame, text="Fluid Density (kg/m³):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    density_entry = ttk.Entry(input_frame, width=15)
    density_entry.grid(row=row, column=1, padx=5, pady=2)
    density_entry.insert(0, "1.225")  # Air at sea level
    row += 1

    ttk.Label(input_frame, text="Dynamic Viscosity (Pa·s):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    viscosity_entry = ttk.Entry(input_frame, width=15)
    viscosity_entry.grid(row=row, column=1, padx=5, pady=2)
    viscosity_entry.insert(0, "1.8e-5")  # Air at 20°C
    row += 1

    # Mode-specific inputs
    vel_label = ttk.Label(input_frame, text="Flow Velocity (m/s):")
    vel_label.grid(row=row, column=0, sticky="w", padx=5, pady=2)
    vel_entry = ttk.Entry(input_frame, width=15)
    vel_entry.grid(row=row, column=1, padx=5, pady=2)
    vel_entry.insert(0, "10.0")

    re_label = ttk.Label(input_frame, text="Reynolds Number:")
    re_label.grid(row=row, column=0, sticky="w", padx=5, pady=2)
    re_entry = ttk.Entry(input_frame, width=15)
    re_entry.grid(row=row, column=1, padx=5, pady=2)
    re_entry.insert(0, "100000")

    # Set initial visibility
    re_label.grid_remove()
    re_entry.grid_remove()

    calc_button = tk.Button(parent,
        text="Calculate",
        command=calculate_reynolds,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5,
        relief="raised",
        bd=2,
        activebackground="#45a049",
        activeforeground="white",
        cursor="hand2")
    calc_button.pack(pady=10)

    # Error label
    error_label = ttk.Label(parent, text="", foreground="red")
    error_label.pack()

    # Results frame
    results_frame = ttk.Frame(parent)
    results_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Bind mode toggle
    mode_var.trace('w', toggle_mode)


def build_gci_tab(parent):
    """Build the Grid Convergence Index calculator UI."""

    # Variables
    mode_var = tk.StringVar(value="auto_p")  # Default: Auto-calculate p

    # Input fields
    r12_entry = None
    r23_entry = None
    coarse_entry = None
    medium_entry = None
    fine_entry = None
    fixed_p_entry = None
    results_frame = None
    error_label = None

    def toggle_p_mode(*args):
        """Show/hide fixed p input based on mode selection."""
        mode = mode_var.get()

        if results_frame:
            for widget in results_frame.winfo_children():
                widget.destroy()

        if mode == "fixed_p":
            fixed_p_label.grid()
            fixed_p_entry.grid()
        else:
            fixed_p_label.grid_remove()
            fixed_p_entry.grid_remove()

    def calculate_gci(*args):
        """Perform GCI calculation."""
        try:
            # Get refinement ratios
            r12 = float(r12_entry.get())
            r23 = float(r23_entry.get())

            # Get solution values
            coarse = float(coarse_entry.get())
            medium = float(medium_entry.get())
            fine = float(fine_entry.get())

            # Get safety factor
            fs = float(fs_entry.get())

            # Check mode
            mode = mode_var.get()
            fixed_p = None
            if mode == "fixed_p":
                fixed_p = float(fixed_p_entry.get())

            # Call core function
            results = calculate_gci_core(r12, r23, coarse, medium, fine, fs, fixed_p)

            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()

            # Display results
            row = 0
            for key, value in results.items():
                tk.Label(results_frame, text=f"{key}:",
                         font=("Arial", 10, "bold")) \
                    .grid(row=row, column=0, sticky="w", padx=5, pady=2)

                result_box = tk.Entry(results_frame, width=25, font=("Courier", 10))
                result_box.insert(0, value)
                result_box.config(state="readonly")
                result_box.grid(row=row, column=1, padx=5, pady=2)

                tk.Button(results_frame, text="📋 Copy",
                          command=lambda v=value: copy_to_clipboard(v)) \
                    .grid(row=row, column=2, padx=5, pady=2)

                row += 1

            if error_label:
                error_label.config(text="")

        except ValueError:
            if error_label:
                error_label.config(text="⚠️ Enter valid numbers!")
        except Exception as e:
            if error_label:
                error_label.config(text=f"⚠️ Error: {str(e)}")

    # ===== UI CONSTRUCTION =====

    # Mode selection
    mode_frame = ttk.Frame(parent)
    mode_frame.pack(pady=10)

    ttk.Label(mode_frame, text="Order of Accuracy:", font=("Arial", 10, "bold")) \
        .pack(side="left", padx=5)

    ttk.Radiobutton(mode_frame, text="Auto-calculate p",
                    variable=mode_var, value="auto_p",
                    command=toggle_p_mode).pack(side="left", padx=5)

    ttk.Radiobutton(mode_frame, text="Use fixed p",
                    variable=mode_var, value="fixed_p",
                    command=toggle_p_mode).pack(side="left", padx=15)

    # Input frame
    input_frame = ttk.Frame(parent)
    input_frame.pack(pady=10)

    row = 0

    # Refinement ratios
    ttk.Label(input_frame, text="Refinement Ratio (r12 - coarse→medium):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    r12_entry = ttk.Entry(input_frame, width=15)
    r12_entry.grid(row=row, column=1, padx=5, pady=2)
    r12_entry.insert(0, "1.29")
    row += 1

    ttk.Label(input_frame, text="Refinement Ratio (r23 - medium→fine):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    r23_entry = ttk.Entry(input_frame, width=15)
    r23_entry.grid(row=row, column=1, padx=5, pady=2)
    r23_entry.insert(0, "1.29")
    row += 1

    # Solution values
    ttk.Label(input_frame, text="Solution Value (Coarse Mesh):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    coarse_entry = ttk.Entry(input_frame, width=15)
    coarse_entry.grid(row=row, column=1, padx=5, pady=2)
    coarse_entry.insert(0, "0.20029")
    row += 1

    ttk.Label(input_frame, text="Solution Value (Medium Mesh):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    medium_entry = ttk.Entry(input_frame, width=15)
    medium_entry.grid(row=row, column=1, padx=5, pady=2)
    medium_entry.insert(0, "0.19318")
    row += 1

    ttk.Label(input_frame, text="Solution Value (Fine Mesh):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    fine_entry = ttk.Entry(input_frame, width=15)
    fine_entry.grid(row=row, column=1, padx=5, pady=2)
    fine_entry.insert(0, "0.18591")
    row += 1

    # Safety factor
    ttk.Label(input_frame, text="Safety Factor (Fs):") \
        .grid(row=row, column=0, sticky="w", padx=5, pady=2)
    fs_entry = ttk.Entry(input_frame, width=15)
    fs_entry.grid(row=row, column=1, padx=5, pady=2)
    fs_entry.insert(0, "1.25")
    row += 1

    # Fixed p input (hidden by default)
    fixed_p_label = ttk.Label(input_frame, text="Fixed Order (p):")
    fixed_p_label.grid(row=row, column=0, sticky="w", padx=5, pady=2)
    fixed_p_entry = ttk.Entry(input_frame, width=15)
    fixed_p_entry.grid(row=row, column=1, padx=5, pady=2)
    fixed_p_entry.insert(0, "2.0")
    fixed_p_label.grid_remove()
    fixed_p_entry.grid_remove()
    row += 1

    # Calculate button
    calc_button = tk.Button(parent,
                            text="Calculate GCI",
                            command=calculate_gci,
                            bg="#4CAF50",
                            fg="white",
                            font=("Arial", 12, "bold"),
                            padx=20,
                            pady=5,
                            relief="raised",
                            bd=2,
                            activebackground="#45a049",
                            activeforeground="white",
                            cursor="hand2")
    calc_button.pack(pady=10)

    # Error label
    error_label = ttk.Label(parent, text="", foreground="red")
    error_label.pack()

    # Results frame
    results_frame = ttk.Frame(parent)
    results_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Bind mode toggle
    mode_var.trace('w', toggle_p_mode)


def build_future_tab(parent):
    """Placeholder for future modules."""
    ttk.Label(parent, text="🔮 More CFD Tools Coming...",
              font=("Arial", 14)).pack(pady=50)

# ===== MAIN WINDOW =====
app = tk.Tk()
app.title("Reynold's App v3.1")
app.geometry("550x700")

# ===== ICON SETUP - BAKED INTO EXE =====
try:
    import sys
    import os

    # Method 1: Window icon - try multiple approaches
    if hasattr(sys, '_MEIPASS'):
        # We're in a PyInstaller bundle - icons are in temp folder
        icon_path = os.path.join(sys._MEIPASS, "reapp.ico")
        png_path = os.path.join(sys._MEIPASS, "ra32.png")
    else:
        # We're running from source
        icon_path = "reapp.ico"
        png_path = "ra32.png"

    # Set window icon
    app.iconbitmap(icon_path)

    # Set taskbar icon using PNG
    if os.path.exists(png_path):
        app.taskbar_icon = tk.PhotoImage(file=png_path)
        app.iconphoto(True, app.taskbar_icon)

    # Windows app ID (helps with taskbar grouping)
    try:
        import ctypes

        myappid = 'madlad.reynoldsapp.v2'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    # Force refresh
    app.withdraw()
    app.deiconify()
    app.update_idletasks()

    print("✓ Icons baked successfully!")
except Exception as e:
    print(f"Icon note: {e}")
# =========================================

# Title - CENTERED with manual offset
title_canvas = tk.Canvas(app, height=40, highlightthickness=0)
title_canvas.pack(pady=10, fill="x")  # fill="x" makes canvas expand with window

def center_title(event=None):
    """Center the title text whenever window resizes."""
    # Get current canvas width
    canvas_width = title_canvas.winfo_width()

    # Delete old text
    title_canvas.delete("all")

    # Calculate positions for centered text
    emoji_width = 30  # Rough width of emoji in pixels
    text_width = 120  # Rough width of "Ryenold's App"
    total_width = emoji_width + text_width

    # Starting X position to center the combined text
    start_x = (canvas_width - total_width) // 2

    # ===== ADD OFFSET HERE =====
    offset = -25  # Negative = left, Positive = right. Adjust this value!
    # ============================

    # Place emoji and text with offset
    title_canvas.create_text(start_x + offset, 20, text="🛩️",
                             font=("Arial", 18, "bold"), anchor="w")
    title_canvas.create_text(start_x + emoji_width + offset, 20, text="Ryenold's App",
                             font=("Arial", 18, "bold"), anchor="w")


# Center initially
app.after(100, center_title)  # Wait a bit for window to render

# Recenter if window is resized
title_canvas.bind("<Configure>", center_title)

# Remove focus from the notebook entirely
notebook = ttk.Notebook(app, takefocus=0)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

# Tab 1: AOA
aoa_tab = ttk.Frame(notebook)
notebook.add(aoa_tab, text="Angle of Attack")
build_aoa_tab(aoa_tab)

# Tab 2: Reynolds
reynolds_tab = ttk.Frame(notebook)
notebook.add(reynolds_tab, text="Reynolds Number")
build_reynolds_tab(reynolds_tab)

# Tab 3: GCI
gci_tab = ttk.Frame(notebook)
notebook.add(gci_tab, text="📊 Grid Convergence Index")
build_gci_tab(gci_tab)

# Tab 4: Future
future_tab = ttk.Frame(notebook)
notebook.add(future_tab, text="⚙️ More Tools")
build_future_tab(future_tab)

# ===== STATUS BAR =====
status_label = ttk.Label(app, text="© Madlad One | Powered by Caffeine",
                         foreground="gray")
status_label.pack(side="bottom", pady=5)

# ===== RUN =====
app.mainloop()