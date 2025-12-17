import pandas as pd
import numpy as np

# Read input file
input_file = 'inputs.xlsx'
efficiency = float(input("Enter efficiency 0-1: "))

try:
    # Read all sheets
    quantities = pd.read_excel(input_file, sheet_name='Quantities')
    avg_parts_per_lot = pd.read_excel(input_file, sheet_name='Avg Parts per Lot')
    machining_rates = pd.read_excel(input_file, sheet_name='Machining Rates')
    setup_rates = pd.read_excel(input_file, sheet_name='Setup Rates')
    vendor_time = pd.read_excel(input_file, sheet_name='Vendor Time')
    machine_allocation = pd.read_excel(input_file, sheet_name='Machine Allocation')
    setup_allocation = pd.read_excel(input_file, sheet_name='Setup Allocation')
except Exception as e:
    print(f"Error reading input file: {e}")
    print("Please ensure 'inputs.xlsx' exists in the current directory.")
    exit(1)

# Use outer merge to find discrepancies in part numbers across sheets
# Start with quantities as base
merged = quantities[['Part Number']].copy()
merged['in_quantities'] = True

# Merge with avg_parts_per_lot
temp = avg_parts_per_lot[['Part Number']].copy()
temp['in_avg_parts'] = True
merged = pd.merge(merged, temp, on='Part Number', how='outer')

# Merge with machining_rates
temp = machining_rates[['Part Number']].copy()
temp['in_machining'] = True
merged = pd.merge(merged, temp, on='Part Number', how='outer')

# Merge with setup_rates
temp = setup_rates[['Part Number']].copy()
temp['in_setup'] = True
merged = pd.merge(merged, temp, on='Part Number', how='outer')

# Merge with vendor_time
temp = vendor_time[['Part Number']].copy()
temp['in_vendor'] = True
merged = pd.merge(merged, temp, on='Part Number', how='outer')

# Replace NaN with False for boolean columns
for col in ['in_quantities', 'in_avg_parts', 'in_machining', 'in_setup', 'in_vendor']:
    merged[col] = merged[col].fillna(False).astype(bool)

# Check for discrepancies
discrepancies = merged[
    (merged['in_quantities'] == False) | 
    (merged['in_avg_parts'] == False) | 
    (merged['in_machining'] == False) | 
    (merged['in_setup'] == False) |
    (merged['in_vendor'] == False)
]

if not discrepancies.empty:
    print("WARNING: Part number discrepancies found:")
    for _, row in discrepancies.iterrows():
        part = row['Part Number']
        missing = []
        if not row['in_quantities']:
            missing.append('Quantities')
        if not row['in_avg_parts']:
            missing.append('Avg Parts per Lot')
        if not row['in_machining']:
            missing.append('Machining Rates')
        if not row['in_setup']:
            missing.append('Setup Rates')
        if not row['in_vendor']:
            missing.append('Vendor Time')
        print(f"  {part}: Missing in {', '.join(missing)}")
    print()
else:
    print("All part numbers match across sheets.")
    print()

# Validate operations across sheets
# Get operations from each sheet (excluding Part Number column)
machining_operations = set([col for col in machining_rates.columns if col != 'Part Number'])
setup_operations = set([col for col in setup_rates.columns if col != 'Part Number'])
allocation_operations = set(machine_allocation['Operations'].dropna().tolist())

# Create merged operations list
all_operations = machining_operations | setup_operations | allocation_operations
operation_check = []

for operation in all_operations:
    operation_check.append({
        'Operation': operation,
        'in_machining_rates': operation in machining_operations,
        'in_setup_rates': operation in setup_operations,
        'in_machine_allocation': operation in allocation_operations
    })

operation_df = pd.DataFrame(operation_check)

# Check for discrepancies
operation_discrepancies = operation_df[
    (operation_df['in_machining_rates'] == False) |
    (operation_df['in_setup_rates'] == False) |
    (operation_df['in_machine_allocation'] == False)
]

if not operation_discrepancies.empty:
    print("WARNING: Operation discrepancies found:")
    for _, row in operation_discrepancies.iterrows():
        operation = row['Operation']
        missing = []
        if not row['in_machining_rates']:
            missing.append('Machining Rates')
        if not row['in_setup_rates']:
            missing.append('Setup Rates')
        if not row['in_machine_allocation']:
            missing.append('Machine Allocation')
        print(f"  {operation}: Missing in {', '.join(missing)}")
    print()
else:
    print("All operations match across sheets.")
    print()

# Validate machines across sheets
# Get machines from Machine Allocation (column headers excluding 'Operations' and 'Total')
# Also exclude empty/unnamed columns that pandas creates from empty Excel columns
allocation_machines = set([
    col for col in machine_allocation.columns
    if col not in ['Operations', 'Total']
    and not str(col).startswith('Unnamed:')
    and not str(col).startswith('_EMPTY')
    and pd.notna(col)
    and str(col).strip() != ''
])

# Get machines from Setup Allocation (column headers excluding 'Unnamed: 0' and 'Operator')
# Also exclude empty/unnamed columns
setup_machines = set([
    col for col in setup_allocation.columns
    if col not in ['Unnamed: 0', 'Operator']
    and not str(col).startswith('Unnamed:')
    and not str(col).startswith('_EMPTY')
    and pd.notna(col)
    and str(col).strip() != ''
])

# Create merged machines list
all_machines = allocation_machines | setup_machines
machine_check = []

for machine in all_machines:
    machine_check.append({
        'Machine': machine,
        'in_machine_allocation': machine in allocation_machines,
        'in_setup_allocation': machine in setup_machines
    })

machine_df = pd.DataFrame(machine_check)

# Check for discrepancies
machine_discrepancies = machine_df[
    (machine_df['in_machine_allocation'] == False) |
    (machine_df['in_setup_allocation'] == False)
]

if not machine_discrepancies.empty:
    print("WARNING: Machine discrepancies found:")
    for _, row in machine_discrepancies.iterrows():
        machine = row['Machine']
        missing = []
        if not row['in_machine_allocation']:
            missing.append('Machine Allocation')
        if not row['in_setup_allocation']:
            missing.append('Setup Allocation')
        print(f"  {machine}: Missing in {', '.join(missing)}")
    print()
else:
    print("All machines match across sheets.")
    print()


# Create a mapping of part number to vendor time (in minutes)
part_vendor_time = {}
for idx, row in vendor_time.iterrows():
    part_num = row['Part Number']
    vendor_days = row['Vendor Time per Lot (Business Days)']
    # Convert days to minutes: days * 18 hours/day * 60 minutes/hour
    vendor_minutes = vendor_days * 18 * 60
    part_vendor_time[part_num] = vendor_minutes

# Create a mapping of operation to machine
# Machine allocation shows which machine(s) handle each operation
# Get machine column names from the dataframe (excluding 'Operations' and 'Total')
# Also exclude empty/unnamed columns
machine_columns = [
    col for col in machine_allocation.columns
    if col not in ['Operations', 'Total']
    and not str(col).startswith('Unnamed:')
    and not str(col).startswith('_EMPTY')
    and pd.notna(col)
    and str(col).strip() != ''
]

operation_to_machine = {}
for idx, row in machine_allocation.iterrows():
    operation = row['Operations']
    # Find which machine has the first non-zero value
    for machine in machine_columns:
        if row[machine] > 0:
            operation_to_machine[operation] = machine
            break

# Create a mapping of machine to operator from setup allocation
# Get machine columns from setup_allocation (excluding 'Operator' or first column)
# Also exclude empty/unnamed columns
setup_machine_columns = [
    col for col in setup_allocation.columns
    if col != 'Unnamed: 0'
    and col != 'Operator'
    and not str(col).startswith('Unnamed:')
    and not str(col).startswith('_EMPTY')
    and pd.notna(col)
    and str(col).strip() != ''
]

machine_to_operator = {}
for machine in setup_machine_columns:
    operator_value = setup_allocation.loc[0, machine]
    
    # Check if the value is a string (could contain comma-separated names)
    if isinstance(operator_value, str):
        # If it contains commas, it's already a list of names
        if ',' in operator_value:
            machine_to_operator[machine] = operator_value.strip()
        else:
            # Single string name
            machine_to_operator[machine] = operator_value.strip()
    else:
        # It's a number, format as "Operator X"
        machine_to_operator[machine] = f'Operator {str(operator_value)}'

# Get list of years from column names
years = [col for col in quantities.columns if col != 'Part Number']

# Create output Excel file
output_file = 'output.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    
    for year in years:
        # Create empty list to store rows for this year
        output_rows = []
        
        # Get operations (columns from machining rates, excluding Part Number)
        operations = [col for col in machining_rates.columns if col != 'Part Number']
        
        # For each part number
        for idx, part_number in enumerate(quantities['Part Number']):
            # Get quantity for this year
            quantity = quantities.loc[idx, year]
            
            # Skip if quantity is NaN or 0
            if pd.isna(quantity) or quantity == 0:
                continue
            
            # Get avg parts per lot for this year
            parts_per_lot = avg_parts_per_lot.loc[idx, year]
            
            # Calculate number of lots
            num_lots = np.ceil(quantity / parts_per_lot) if parts_per_lot > 0 else 0
            
            # For each operation
            for operation in operations:
                # Get machining rate
                machining_rate = machining_rates.loc[idx, operation]
                
                # Skip if machining rate is NaN or 0 (operation not needed for this part)
                if pd.isna(machining_rate) or machining_rate == 0:
                    continue
                
                # Get setup rate
                setup_rate = setup_rates.loc[idx, operation]
                if pd.isna(setup_rate):
                    setup_rate = 0
                
                # Calculate on-machine minutes
                on_machine_minutes = quantity * machining_rate / efficiency
                
                # Calculate total setup time
                total_setup_time = num_lots * setup_rate / efficiency
                
                # Calculate setup time + machine time
                setup_plus_machine = total_setup_time + on_machine_minutes
                
                # Get machine assignment for this operation
                machine = operation_to_machine.get(operation, 'N/A')
                
                # Get operator assignment based on machine
                operator = machine_to_operator.get(machine, 'N/A')
                
                # Add row to output
                output_rows.append({
                    'Part Number': part_number,
                    'Operation': operation,
                    'Machine': machine,
                    'Operator': operator,
                    'Quantity': quantity,
                    'Machining Rate (minutes/part)': machining_rate,
                    'Setup Rate (minutes/lot)': setup_rate,
                    'On-Machine Minutes': on_machine_minutes,
                    'Number of Lots': num_lots,
                    'Total Setup Time (minutes)': total_setup_time,
                    'Setup Time + Machine Time': setup_plus_machine
                })
        
        # Create DataFrame for this year
        if output_rows:
            year_df = pd.DataFrame(output_rows)
            year_df.to_excel(writer, sheet_name=str(year), index=False)
        else:
            # Create empty sheet with headers if no data
            empty_df = pd.DataFrame(columns=[
                'Part Number', 'Operation', 'Machine', 'Operator', 'Quantity', 
                'Machining Rate (minutes/part)', 'Setup Rate (minutes/lot)',
                'On-Machine Minutes', 'Number of Lots', 
                'Total Setup Time (minutes)', 'Setup Time + Machine Time'
            ])
            empty_df.to_excel(writer, sheet_name=str(year), index=False)

print(f"Output file created: {output_file}")
print(f"Sheets created for years: {years}")

# Bottleneck Analysis
print("\n" + "="*60)
print("CAPACITY ANALYSIS")
print("="*60)

available_capacity = 252 * 18 * 60  # minutes

# Collect data for each year and store for early start analysis
year_data = {}
for year in years:
    year_df = pd.read_excel(output_file, sheet_name=str(year))
    
    if year_df.empty:
        year_data[year] = None
        continue
    
    # Calculate totals for each resource (machines and operators)
    resource_totals = {}
    resource_mins = {}
    
    # Machine totals (On-Machine Minutes only)
    for machine in year_df['Machine'].unique():
        if pd.notna(machine):
            machine_df = year_df[year_df['Machine'] == machine]
            resource_totals[machine] = machine_df['On-Machine Minutes'].sum()
            
            # Calculate minimum operation time for this machine
            op_mins = machine_df.groupby('Operation')['On-Machine Minutes'].sum()
            resource_mins[machine] = op_mins.min() if not op_mins.empty else 0
    
    # Operator totals (Total Setup Time divided by number of operators)
    for operator in year_df['Operator'].unique():
        if pd.notna(operator) and isinstance(operator, str):
            total_setup = 0
            operator_op_mins = {}
            
            for _, row in year_df.iterrows():
                if isinstance(row['Operator'], str) and operator in row['Operator']:
                    # Count number of operators
                    num_ops = len([op.strip() for op in row['Operator'].split(',') if op.strip()])
                    setup_time_per_operator = row['Total Setup Time (minutes)'] / num_ops if num_ops > 0 else 0
                    total_setup += setup_time_per_operator
                    
                    # Track by operation for minimum calculation
                    operation = row['Operation']
                    operator_op_mins[operation] = operator_op_mins.get(operation, 0) + setup_time_per_operator
            
            resource_totals[operator] = total_setup
            # Calculate minimum operation time for this operator
            resource_mins[operator] = min(operator_op_mins.values()) if operator_op_mins else 0
    
    # Calculate total vendor time for this year
    # Calculate total vendor time for this year (vendor time per lot × number of lots)
    total_vendor_time = 0
    for part_number in year_df['Part Number'].unique():
        if pd.notna(part_number) and part_number in part_vendor_time:
            # Get the number of lots for this part in this year
            part_rows = year_df[year_df['Part Number'] == part_number]
            if not part_rows.empty:
                # Vendor time is per lot, so multiply by number of lots
                # Get number of lots from the first row (it's the same for all operations)
                num_lots = part_rows.iloc[0]['Number of Lots']
                total_vendor_time += part_vendor_time[part_number] * num_lots
    
    # Find the bottleneck resource (machine or operator with maximum total time)
    if resource_totals:
        max_minutes = max(resource_totals.values())
        bottleneck = [r for r, v in resource_totals.items() if v == max_minutes][0]
        
        # Sum minimum operation times for all other resources
        other_resources_min = sum(
            resource_mins[resource]
            for resource in resource_mins
            if resource != bottleneck
        )
        
        # Total capacity = bottleneck + sum of mins from other resources + vendor time
        total_minutes = max_minutes + other_resources_min + total_vendor_time
        
        year_data[year] = {
            'total_minutes': total_minutes,
            'bottleneck': bottleneck,
            'max_minutes': max_minutes,
            'other_resources_min': other_resources_min,
            'vendor_time': total_vendor_time
        }

# Display bottleneck analysis with early start check
adjusted_capacity = {}
for year in years:
    if year_data.get(year) is None:
        print(f"\n{year}: No data")
        adjusted_capacity[year] = 0
        continue
    
    data = year_data[year]
    total_minutes = data['total_minutes']
    bottleneck = data['bottleneck']
    max_minutes = data['max_minutes']
    other_resources_min = data['other_resources_min']
    vendor_time = data['vendor_time']
    
    total_capacity = total_minutes / available_capacity
    # Check if bottleneck is in machine_columns (from Machine Allocation sheet) to determine type
    resource_type = "Machine" if bottleneck in machine_columns else "Operator"
    
    print(f"\n{year}:")
    print(f"  Bottleneck: {bottleneck} ({resource_type}) - {max_minutes:,.0f} minutes")
    print(f"  Other Resources Min Sum: {other_resources_min:,.0f} minutes")
    print(f"  Vendor Time: {vendor_time:,.0f} minutes")
    print(f"  Total Capacity: {total_capacity:.2%} ({total_minutes:,.0f} / {available_capacity:,} minutes)")
    
    # Check if at or over 100% capacity
    if total_capacity >= 1.0:
        overflow = total_minutes - available_capacity
        print(f"  ⚠ Over capacity by {overflow:,.0f} minutes!")
        
        # Check previous years for available capacity
        pulled_total = 0
        for prev_year in reversed([y for y in years if y < year]):
            if prev_year in adjusted_capacity:
                available_in_prev = available_capacity - adjusted_capacity[prev_year]
                if available_in_prev > 0:
                    pull_amount = min(overflow, available_in_prev)
                    adjusted_capacity[prev_year] += pull_amount
                    overflow -= pull_amount
                    pulled_total += pull_amount
                    print(f"  → Pulled {pull_amount:,.0f} minutes into {prev_year} (now at {(adjusted_capacity[prev_year]/available_capacity):.2%})")
                    if overflow <= 0:
                        break
        
        adjusted_capacity[year] = total_minutes - pulled_total
        
        if overflow > 0:
            print(f"  ⚠ WARNING: Capacity is at {(adjusted_capacity[year]/available_capacity):.2%} and there is no time available to start early in prior years.")
            print(f"     Remaining overflow: {overflow:,.0f} minutes")
    else:
        adjusted_capacity[year] = total_minutes

print("\n" + "="*60)