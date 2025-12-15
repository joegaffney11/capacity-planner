import pandas as pd

class CapacityAnalyzer:
    def __init__(self):
        self.merged = None
        self.merged_setup = None
        self.machining_rates = None
        self.setup_rates = None
        self.forecast_quantities = None
        self.avg_parts_per_lot = None
        self.years = None
        self.machine_to_operator = {}  # Map machines to operators
            
    def data_input_setup(self):
        # Read all sheets from inputs.xlsx at once
        self.all_sheets = pd.read_excel('inputs.xlsx', sheet_name=None)
        
        self.machining_rates = self.all_sheets['Machining Rates']
        self.setup_rates = self.all_sheets['Setup Rates']
        self.forecast_quantities = self.all_sheets['Quantities']
        self.avg_parts_per_lot = self.all_sheets['Avg Parts per Lot']

        # Parse the Setup Allocation sheet (new format: single row with operator numbers)
        setup_allocation = self.all_sheets['Setup Allocation']
        # First column is label, rest are machines
        for col in setup_allocation.columns:
            if col != 'Unnamed: 0' and 'Machine' in col:
                operator_num = setup_allocation[col].iloc[0]
                self.machine_to_operator[col] = f"Operator {int(operator_num)}"

        # Merge machining data on Part Number
        self.merged = pd.merge(
            self.machining_rates,
            self.forecast_quantities,
            on='Part Number',
            how='outer',
            indicator=True
        )
        
        # Merge setup data on Part Number
        self.merged_setup = pd.merge(
            self.setup_rates,
            self.forecast_quantities,
            on='Part Number',
            how='outer',
            indicator=True
        )
        
        # Also merge avg parts per lot for setup calculations
        self.merged_setup = pd.merge(
            self.merged_setup,
            self.avg_parts_per_lot,
            on='Part Number',
            how='left',
            suffixes=('_qty', '_lot')
        )

        # Get year columns (all columns from forecast_quantities except Part Number)
        self.years = [col for col in self.forecast_quantities.columns if col not in ['Part Number']]
        print(self.years)
   
    def check_merge_errors(self):
        # CHECK TO MAKE SURE PART NUMBER LISTS MATCH
        # Check for unmerged rows
        left_only = self.merged[self.merged['_merge'] == 'left_only']
        right_only = self.merged[self.merged['_merge'] == 'right_only']

        print(f"\n{'='*50}")
        print("Merge Errors:")
        print(f"{'='*50}")

        if len(left_only) > 0:
            print(f"⚠️  WARNING: {len(left_only)} part numbers in machining_rates.xlsx not found in forecast_quantities.xlsx:")
            print(left_only['Part Number'].tolist())

        if len(right_only) > 0:
            print(f"⚠️  WARNING: {len(right_only)} part numbers in forecast_quantities.xlsx not found in machining_rates.xlsx:")
            print(right_only['Part Number'].tolist())

        else:
            print("No errors!")

    def operation_lines(self):
        # Get operation columns (all columns from machining_rates except Part Number)
        operations = [col for col in self.machining_rates.columns if col not in ['Part Number']]
        
        # Store results in memory instead of saving to CSV
        self.capacity_results = {}
        
        for year in self.years:
            rows = []
            
            # Iterate through each row in merged DataFrame
            for _, row in self.merged.iterrows():
                part_number = row['Part Number']
                year_quantity = row[year]  # Get the quantity for this year
                
                # Create a row for each operation
                for op in operations:
                    rate = row[op]  # Get the rate for this operation
                    rows.append({
                        'Part Number': part_number,
                        'Operation': op,
                        'Quantity': year_quantity,
                        'Rate (minutes/part)': rate,
                        'On-Machine Minutes': rate * year_quantity
                    })
            
            

            # Store DataFrame in memory
            self.capacity_results[year] = pd.DataFrame(rows)
            self.capacity_results[year].to_csv(f'capacity_{year}.csv', index=False)
            print(f"Processed capacity data for {year}")
    
    def create_machine_csvs(self, allocation_file='machine_allocation.xlsx'):
        """Create separate CSV files for each machine based on operation allocation."""
        allocation = pd.read_excel(allocation_file)
        machines = [col for col in allocation.columns if col not in ['Operations', 'Total']]
        
        for year in self.years:
            # Use in-memory capacity data instead of reading from CSV
            capacity_data = self.capacity_results[year]
            
            # Initialize dictionaries for this year if not exists
            if year not in self.machine_totals:
                self.machine_totals[year] = {}
            if year not in self.machine_mins:
                self.machine_mins[year] = {}
            
            for machine in machines:
                # Get operations where this machine has a 1
                machine_ops = allocation[allocation[machine] == 1]['Operations'].tolist()
                
                # Filter for machine operations and non-zero on-machine time
                machine_data = capacity_data[
                    (capacity_data['Operation'].isin(machine_ops)) & 
                    (capacity_data['On-Machine Minutes'] > 0)
                ]

                # Add SUM row
                sum_row = {}
                sum_row['Part Number'] = 'SUM'
                for col in machine_data.columns[2:5:2]:
                    sum_row[col] = machine_data[col].sum()
                machine_data = pd.concat([machine_data, pd.DataFrame([sum_row])], ignore_index=True)
                
                # Store the total and minimum on-machine minutes
                self.machine_totals[year][machine] = machine_data['On-Machine Minutes'].sum()
                self.machine_mins[year][machine] = machine_data['On-Machine Minutes'].min() if not machine_data.empty else 0
                
                #machine_data.to_csv(f'{machine}_{year}.csv', index=False)
                print(f"Created {machine}_{year}.csv")
    
    def print_machine_capacity(self):

        print(f"\n{'='*50}")
        print("By-Machine Capacity:")
        print(f"{'='*50}")

        """Calculate and print capacity for each machine."""
        # Available capacity per year: 252 days * 18 hours * 60 minutes
        available_capacity = 252 * 18 * 60
        
        for year in self.years:
            print(f"\n{year} Machine Capacity:")
            print("-" * 50)
            
            for machine, total_minutes in self.machine_totals[year].items():
                # Calculate capacity utilization
                capacity = total_minutes / available_capacity
                
                print(f"{machine}: {capacity:.2%} ({total_minutes:,.0f} / {available_capacity:,} minutes)")
    
    def print_total_capacity(self):
        """Calculate and print total capacity utilization for each year."""
        # Available capacity per year: 252 days * 18 hours * 60 minutes
        available_capacity = 252 * 18 * 60
        
        print(f"\n{'='*50}")
        print("Total Capacity Utilization:")
        print(f"{'='*50}")
        
        for year in self.years:
            # Find the machine with maximum on-machine minutes
            max_minutes = max(self.machine_totals[year].values())
            max_machine = [m for m, v in self.machine_totals[year].items() if v == max_minutes][0]
            
            # Sum the minimum operation times for all other machines
            other_machines_min = sum(
                self.machine_mins[year][machine] 
                for machine in self.machine_mins[year] 
                if machine != max_machine
            )
            
            # Total capacity = max machine + sum of mins from other machines
            total_minutes = max_minutes + other_machines_min
            total_capacity = total_minutes / available_capacity
            
            print(f"\n{year}:")
            print(f"  Bottleneck Machine: {max_machine} ({max_minutes:,.0f} minutes)")
            print(f"  Other Machines Min Sum: {other_machines_min:,.0f} minutes")
            print(f"  Total Capacity: {total_capacity:.2%} ({total_minutes:,.0f} / {available_capacity:,} minutes)")

# Example usage
if __name__ == "__main__":
    analyzer = CapacityAnalyzer()
    analyzer.data_input_setup()
    analyzer.operation_lines()
    analyzer.create_machine_csvs()
    analyzer.print_machine_capacity()
    analyzer.print_total_capacity()
    analyzer.check_merge_errors()