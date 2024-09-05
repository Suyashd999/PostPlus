import json
import pandas as pd
import matplotlib.pyplot as plt

# Path for saving the output image
output_image_path = 'truck_progress_overview.png'

def process_data():
    # Load data from items file
    with open('data.json', 'r') as file:
        items = json.load(file)
    
    step = 1
    cumulative_data = []  # To store all steps data
    truck_id = "325101"  # Updated to the correct truck ID

    # Load truck data for max weight and volume information
    truck_data = {
        "325101": {
            "max_weight": 1000,
            "max_volume": 20000
        }
    }
    
    max_weight = truck_data[truck_id]['max_weight']
    max_volume = truck_data[truck_id]['max_volume']
    
    current_weight = 0
    current_volume = 0
    ignore_entries = False

    for item in items:
        if ignore_entries:
            break
        
        weight = item['weight']
        dimensions = item['dimensions']
        action = item['action']
        
        # Convert dimensions to volume
        w, h, d = map(int, dimensions.split('x'))
        volume = w * h * d
        
        # Calculate potential new weight and volume
        new_weight = current_weight + weight
        new_volume = current_volume + volume
        
        # Check if adding the item exceeds truck capacity
        if new_weight > max_weight or new_volume > max_volume:
            print(f"Step {step}: Cannot load item {item['item']}. Exceeds truck capacity.")
            ignore_entries = True
            break
        
        # Update current weight and volume
        current_weight = new_weight
        current_volume = new_volume
        
        # Calculate filled capacity percentages
        filled_weight_percentage = (current_weight / max_weight) * 100
        filled_volume_percentage = (current_volume / max_volume) * 100
        
        # Append to cumulative data for tracking
        cumulative_data.append({
            'Step': step,
            'Item': item['item'],
            'Weight': weight,
            'Volume': volume,
            'Current Weight': current_weight,
            'Current Volume': current_volume,
            'Filled Capacity': f"{filled_weight_percentage:.2f}% Weight, {filled_volume_percentage:.2f}% Volume",
            'Action': action
        })
        
        step += 1

    # Convert cumulative data to DataFrame for visualization
    df = pd.DataFrame(cumulative_data)

    # Plot and save the single comprehensive image
    plt.figure(figsize=(15, len(df) * 0.6 + 2))  # Adjust height based on the number of steps
    plt.axis('off')

    # Add the title
    plt.text(0.5, 1.05, f"Truck Progress Overview for Truck ID {truck_id}", ha='center', va='center', fontsize=16, fontweight='bold')

    # Adjusted max weight and max volume info
    max_info_text = f"Max Weight = {max_weight} kg\nMax Volume = {max_volume} cu units"
    plt.text(0.95, 1.0, max_info_text, ha='right', va='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.5'))

    # Create the table with adjusted position and better alignment
    ax = plt.gca()
    table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', bbox=[0.05, 0.15, 0.9, 0.75])

    # Adjust column widths and alignments for better readability
    table.auto_set_column_width(col=list(range(len(df.columns))))
    table.auto_set_font_size(False)
    table.set_fontsize(9)

    # Bold the header row
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(weight='bold')

    # Save the figure
    plt.savefig(output_image_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Comprehensive progress image saved at {output_image_path}")

if __name__ == "__main__":
    process_data()
