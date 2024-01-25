import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Enable dark mode
ctk.set_appearance_mode("Dark")

# Estes Rocket Motors Data (Example Data)
estes_motors = {
    "A8-3": {"thrust": 5, "weight": 0.018, "burn_time": 2.5},
    "B6-4": {"thrust": 10, "weight": 0.024, "burn_time": 3},
    "C6-5": {"thrust": 15, "weight": 0.030, "burn_time": 3.5}
}

app = ctk.CTk()
app.title("Rocket Design Simulator")

# Frames for organizing layout
input_frame = ctk.CTkFrame(app, corner_radius=10)
stats_frame = ctk.CTkFrame(app, corner_radius=10)

input_frame.pack(pady=10, padx=10, fill="both", expand=True)
stats_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Input widgets
height_var = ctk.StringVar()
outer_diameter_var = ctk.StringVar()
inner_diameter_var = ctk.StringVar()
infill_var = ctk.StringVar()
nosecone_height_var = ctk.StringVar(value="20")  # Default value in millimeters
fin_count_var = ctk.StringVar(value="4")  # Default to 4 fins
fin_length_var = ctk.StringVar(value="20")  # Default fin length as percentage of rocket height
fin_width_var = ctk.StringVar(value="10")  # Default fin width
fin_top_width_var = ctk.StringVar(value="5")  # Default top width of the fin
motor_var = ctk.StringVar()

#%% Element Creation
# Configure the grid layout for input_frame
input_frame.grid_columnconfigure(1, weight=1)  # This makes the second column expandable

# ... [previous code]

# Configure the grid layout for input_frame
input_frame.grid_columnconfigure(1, weight=1)  # This makes the second column expandable

# Define padding
padx = 10
pady = 5

# Add input fields with grid layout and padding
ctk.CTkLabel(input_frame, text="Rocket Height (mm):").grid(row=0, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=height_var).grid(row=0, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Outer Diameter (mm):").grid(row=1, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=outer_diameter_var).grid(row=1, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Inner Diameter (mm):").grid(row=2, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=inner_diameter_var).grid(row=2, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Infill (%):").grid(row=3, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=infill_var).grid(row=3, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Nosecone Height (mm):").grid(row=4, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=nosecone_height_var).grid(row=4, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Fin Count:").grid(row=5, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=fin_count_var).grid(row=5, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Fin Length (% of Rocket Height):").grid(row=6, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=fin_length_var).grid(row=6, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Fin Base Width (mm):").grid(row=7, column=0, sticky='e', padx=padx, pady=pady)
ctk.CTkEntry(input_frame, textvariable=fin_width_var).grid(row=7, column=1, sticky='we', padx=padx, pady=pady)

ctk.CTkLabel(input_frame, text="Select Motor:").grid(row=8, column=0, sticky='e', padx=padx, pady=pady)
motor_combo = ctk.CTkComboBox(input_frame, variable=motor_var, values=list(estes_motors.keys()))
motor_combo.grid(row=8, column=1, sticky='we', padx=padx, pady=pady)

update_button = ctk.CTkButton(input_frame, text="Update Design")
update_button.grid(row=9, column=0, columnspan=2, padx=padx, pady=pady, sticky='we')


# Stats widgets placeholders
weight_label = ctk.CTkLabel(stats_frame, text="Estimated Weight: TBD")
weight_label.pack()

height_label = ctk.CTkLabel(stats_frame, text="Estimated Flight Height: TBD")
height_label.pack()

cg_label = ctk.CTkLabel(stats_frame, text="CG from Bottom: TBD")
cg_label.pack()

thrust_to_weight_label = ctk.CTkLabel(stats_frame, text="Thrust-to-Weight Ratio: TBD")
thrust_to_weight_label.pack()

#%%calculations for stats

def calculate_rocket_parameters():
    try:
        # Retrieve and validate input values
        height = float(height_var.get()) if height_var.get() else None
        outer_diameter = float(outer_diameter_var.get()) if outer_diameter_var.get() else None
        inner_diameter = float(inner_diameter_var.get()) if inner_diameter_var.get() else None
        infill_percentage = float(infill_var.get()) if infill_var.get() else None
        nosecone_height = float(nosecone_height_var.get()) if nosecone_height_var.get() else None
        fin_count = int(fin_count_var.get()) if fin_count_var.get() else None
        fin_length_percentage = float(fin_length_var.get()) if fin_length_var.get() else None
        fin_width = float(fin_width_var.get()) if fin_width_var.get() else None
        motor = estes_motors[motor_var.get()] if motor_var.get() in estes_motors else None

        if None in [height, outer_diameter, inner_diameter, infill_percentage, nosecone_height, 
                    fin_count, fin_length_percentage, fin_width, motor]:
            return None  # Return None if any input is missing

        # Constants for calculations
        density = 0.0012  # Density of material in g/mm^3
        gravity = 9.81  # Gravity in m/s^2

        # Rocket Body
        volume_inner = np.pi * (inner_diameter / 2)**2 * height
        volume_outer = np.pi * (outer_diameter / 2)**2 * height
        volume_infill = (volume_outer - volume_inner) * (infill_percentage / 100)
        weight_body = (volume_inner + volume_infill) * density / 1000  # Convert to kg
        cg_body = height / 2  # Midpoint of the cylindrical body

        # Fins
        fin_length = fin_length_percentage / 100 * height  # Length along the rocket body
        fin_area_rect = fin_width * fin_length  # Area of the rectangular part of the fin
        fin_area_tri = 0.5 * fin_width * (outer_diameter - inner_diameter) / 2  # Area of the triangular part
        fin_area = fin_area_rect + fin_area_tri
        fin_volume = fin_area * fin_count
        weight_fins = fin_volume * density / 1000  # Convert to kg
        # CG of fins (approximate)
        cg_fins = height - (fin_length / 2)  # Assuming fins are located at the bottom half of the rocket


        # Nosecone
        nosecone_volume = (1/3) * np.pi * (outer_diameter / 2)**2 * nosecone_height
        weight_nosecone = nosecone_volume * density / 1000  # Convert to kg
        cg_nosecone = height + (nosecone_height / 4)  # CG of a cone is 1/4th from the base

        # Total weight and CG
        total_weight = weight_body + weight_fins + weight_nosecone
        total_cg = (cg_body * weight_body + cg_fins * weight_fins + cg_nosecone * weight_nosecone) / total_weight

        # Flight height (simplified)
        flight_height = motor['thrust'] / (total_weight * gravity) * 100

        # Thrust-to-weight ratio
        thrust_to_weight_ratio = motor['thrust'] / (total_weight * gravity)

        return total_weight, flight_height, total_cg, thrust_to_weight_ratio

    except ValueError:
        return None



def update_stats():
    calculated_values = calculate_rocket_parameters()
    if calculated_values:
        weight, flight_height, cg, thrust_to_weight_ratio = calculated_values

        # Update stats labels
        weight_label.configure(text=f"Estimated Weight: {weight:.2f} kg")
        height_label.configure(text=f"Estimated Flight Height: {flight_height:.2f} m")
        cg_label.configure(text=f"CG from Bottom: {cg:.2f} mm")
        thrust_to_weight_label.configure(text=f"Thrust-to-Weight Ratio: {thrust_to_weight_ratio:.2f}")

    else:
        print("Please fill all inputs correctly.")

    # Schedule the next update
    app.after(500, update_stats)


# Modify the update button to initiate the update process
update_button.configure(command=update_stats)


app.mainloop()
