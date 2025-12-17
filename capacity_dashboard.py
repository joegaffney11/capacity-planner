import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Capacity Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Main app styling */
    .stApp {
        background: #000000;
        font-family: 'Inter', sans-serif;
        color: #f3f4f6;
    }

    /* Remove default padding */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }

    /* All text should be light colored */
    p, span, div, label, li {
        color: #f3f4f6 !important;
    }

    /* Headers */
    h1 {
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #1d4ed8);
        color: white !important;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.3);
        margin-bottom: 2rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    h2 {
        color: #60a5fa !important;
        padding: 0rem 0;
        border-bottom: 2px solid #60a5fa;
        margin: 1rem 0 1rem 0 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    h3 {
        color: #60a5fa !important;
        margin-bottom: 0 !important;
        font-size: 2rem !important;
    }

    /* Expander styling - no color change when open */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
        color: #f3f4f6 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
    }

    [data-testid="stExpander"] {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }

    /* Prevent color change when expanded - all states */
    [data-testid="stExpander"][open],
    [data-testid="stExpander"] details[open],
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"][aria-expanded="true"],
    details[open] > summary {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
    }

    [data-testid="stExpander"] details {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
    }

    [data-testid="stExpander"] div[role="region"] {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
        color: #f3f4f6 !important;
        padding: 0.5rem !important;
    }

    /* Override any default expander background changes */
    [data-testid="stExpander"] > div,
    [data-testid="stExpander"] > div > div {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
    }

    /* Expander content text */
    [data-testid="stExpander"] p, [data-testid="stExpander"] span, [data-testid="stExpander"] div {
        color: #f3f4f6 !important;
    }

    /* Container with border styling */
    [data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]) {
        background: linear-gradient(145deg, #2a2a3a, #36364d) !important;
        border-radius: 12px !important;
        padding: 0rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }

    [data-testid="stMetricLabel"] {
        color: #f3f4f6 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* DataFrames */
    [data-testid="stDataFrame"], .stDataFrame {
        background: transparent !important;
    }

    [data-testid="stDataFrame"] div[data-testid="stDataFrameResizable"] {
        background: linear-gradient(145deg, #1e1e2e, #252539) !important;
        border-radius: 10px !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #2a2a3a, #323247) !important;
    }

    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #f3f4f6 !important;
    }

    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #60a5fa !important;
    }

    /* Info/Success/Warning boxes */
    .stAlert {
        background: linear-gradient(145deg, #2a2a3a, #36364d) !important;
        color: #f3f4f6 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(96, 165, 250, 0.3) !important;
    }

    .stAlert p, .stAlert div {
        color: #f3f4f6 !important;
    }

    /* Make buttons always grey (not just on hover) */
    button[kind="secondary"] {
        background: linear-gradient(145deg, #2a2a3a, #36364d) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    button[kind="secondary"]:hover {
        background: linear-gradient(145deg, #35354a, #3f3f57) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Primary buttons - blue instead of red */
    button[kind="primary"] {
        background: linear-gradient(135deg, #60a5fa, #3b82f6) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
    }

    /* More compact containers for machine cards */
    [data-testid="stVerticalBlock"] > [data-testid="element-container"] > div[data-testid="stVerticalBlock"] > div > div {
        padding: 0.75rem 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

class CapacityAnalyzer:
    def __init__(self, efficiency=1.0):
        self.efficiency = efficiency
        self.quantities = None
        self.avg_parts_per_lot = None
        self.machining_rates = None
        self.setup_rates = None
        self.vendor_time = None
        self.machine_allocation = None
        self.setup_allocation = None
        self.years = None
        self.part_vendor_time = {}
        self.operation_to_machine = {}
        self.machine_to_operator = {}
        self.available_capacity = 252 * 18 * 60  # minutes per year
        self.validation_results = {}

    def load_data(self, file):
        """Load all sheets from inputs.xlsx"""
        try:
            all_sheets = pd.read_excel(file, sheet_name=None)
            return all_sheets
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None

    def data_input_setup(self, file):
        """Read and setup data from inputs.xlsx"""
        all_sheets = self.load_data(file)
        if all_sheets is None:
            return False

        required_sheets = ['Quantities', 'Avg Parts per Lot', 'Machining Rates',
                          'Setup Rates', 'Vendor Time', 'Machine Allocation', 'Setup Allocation']

        missing_sheets = [sheet for sheet in required_sheets if sheet not in all_sheets]
        if missing_sheets:
            st.error(f"Missing required sheets: {', '.join(missing_sheets)}")
            return False

        self.quantities = all_sheets['Quantities']
        self.avg_parts_per_lot = all_sheets['Avg Parts per Lot']
        self.machining_rates = all_sheets['Machining Rates']
        self.setup_rates = all_sheets['Setup Rates']
        self.vendor_time = all_sheets['Vendor Time']
        self.machine_allocation = all_sheets['Machine Allocation']
        self.setup_allocation = all_sheets['Setup Allocation']

        # Get years
        self.years = [col for col in self.quantities.columns if col != 'Part Number']

        # Create mappings
        self._create_mappings()

        # Validate data
        self._validate_data()

        return True

    def _create_mappings(self):
        """Create mapping dictionaries"""
        # Vendor time mapping (convert days to minutes)
        for idx, row in self.vendor_time.iterrows():
            part_num = row['Part Number']
            vendor_days = row['Vendor Time per Lot (Business Days)']
            vendor_minutes = vendor_days * 18 * 60  # 18-hour business days
            self.part_vendor_time[part_num] = vendor_minutes

        # Operation to machine mapping with percentage allocation
        machine_columns = [col for col in self.machine_allocation.columns
                          if col not in ['Operations', 'Total']
                          and not str(col).startswith('Unnamed:')
                          and not str(col).startswith('_EMPTY')
                          and pd.notna(col)
                          and str(col).strip() != '']

        for idx, row in self.machine_allocation.iterrows():
            operation = row['Operations']
            if pd.isna(operation):
                continue

            # Collect all machines with their allocation percentages
            machine_allocations = []
            total_allocation = 0

            for machine in machine_columns:
                allocation = float(row[machine]) if pd.notna(row[machine]) else 0
                if allocation > 0:
                    machine_allocations.append({
                        'machine': machine,
                        'allocation': allocation
                    })
                    total_allocation += allocation

            # Normalize to percentages (in case they don't add up to 100)
            if machine_allocations and total_allocation > 0:
                for ma in machine_allocations:
                    ma['percentage'] = ma['allocation'] / total_allocation
                self.operation_to_machine[operation] = machine_allocations

        # Machine to operator mapping
        setup_machine_columns = [col for col in self.setup_allocation.columns
                                if col not in ['Unnamed: 0', 'Operator']]
        for machine in setup_machine_columns:
            operator_value = self.setup_allocation.loc[0, machine]
            if isinstance(operator_value, str):
                self.machine_to_operator[machine] = operator_value.strip()
            else:
                self.machine_to_operator[machine] = f'Operator {int(operator_value)}'

    def _validate_data(self):
        """Validate consistency across sheets"""
        self.validation_results = {
            'part_numbers': {'status': 'success', 'discrepancies': []},
            'operations': {'status': 'success', 'discrepancies': []},
            'machines': {'status': 'success', 'discrepancies': []}
        }

        # Validate part numbers
        sheets_with_parts = {
            'Quantities': set(self.quantities['Part Number'].dropna()),
            'Avg Parts per Lot': set(self.avg_parts_per_lot['Part Number'].dropna()),
            'Machining Rates': set(self.machining_rates['Part Number'].dropna()),
            'Setup Rates': set(self.setup_rates['Part Number'].dropna()),
            'Vendor Time': set(self.vendor_time['Part Number'].dropna())
        }

        all_parts = set().union(*sheets_with_parts.values())
        for part in all_parts:
            missing_in = [sheet for sheet, parts in sheets_with_parts.items() if part not in parts]
            if missing_in:
                self.validation_results['part_numbers']['discrepancies'].append({
                    'item': part,
                    'missing_in': missing_in
                })
                self.validation_results['part_numbers']['status'] = 'warning'

        # Validate operations
        machining_ops = set([col for col in self.machining_rates.columns if col != 'Part Number'])
        setup_ops = set([col for col in self.setup_rates.columns if col != 'Part Number'])
        allocation_ops = set(self.machine_allocation['Operations'].dropna())

        all_ops = machining_ops | setup_ops | allocation_ops
        for op in all_ops:
            missing_in = []
            if op not in machining_ops:
                missing_in.append('Machining Rates')
            if op not in setup_ops:
                missing_in.append('Setup Rates')
            if op not in allocation_ops:
                missing_in.append('Machine Allocation')
            if missing_in:
                self.validation_results['operations']['discrepancies'].append({
                    'item': op,
                    'missing_in': missing_in
                })
                self.validation_results['operations']['status'] = 'warning'

        # Validate machines
        allocation_machines = set([col for col in self.machine_allocation.columns
                                  if col not in ['Operations', 'Total']])
        setup_machines = set([col for col in self.setup_allocation.columns
                             if col not in ['Unnamed: 0', 'Operator']])

        all_machines = allocation_machines | setup_machines
        for machine in all_machines:
            missing_in = []
            if machine not in allocation_machines:
                missing_in.append('Machine Allocation')
            if machine not in setup_machines:
                missing_in.append('Setup Allocation')
            if missing_in:
                self.validation_results['machines']['discrepancies'].append({
                    'item': machine,
                    'missing_in': missing_in
                })
                self.validation_results['machines']['status'] = 'warning'

    def calculate_year_data(self, year):
        """Calculate all capacity data for a specific year"""
        output_rows = []
        operations = [col for col in self.machining_rates.columns if col != 'Part Number']

        for idx, part_number in enumerate(self.quantities['Part Number']):
            quantity = self.quantities.loc[idx, year]

            if pd.isna(quantity) or quantity == 0:
                continue

            parts_per_lot = self.avg_parts_per_lot.loc[idx, year]
            num_lots = np.ceil(quantity / parts_per_lot) if parts_per_lot > 0 else 0

            for operation in operations:
                machining_rate = self.machining_rates.loc[idx, operation]

                if pd.isna(machining_rate) or machining_rate == 0:
                    continue

                setup_rate = self.setup_rates.loc[idx, operation]
                if pd.isna(setup_rate):
                    setup_rate = 0

                # Calculate total times before distribution
                total_on_machine_minutes = quantity * machining_rate / self.efficiency
                total_setup_time = num_lots * setup_rate / self.efficiency

                # Get machine allocations for this operation
                machine_allocations = self.operation_to_machine.get(operation)

                if not machine_allocations:
                    # No machine allocation found - create N/A entry
                    output_rows.append({
                        'Part Number': part_number,
                        'Operation': operation,
                        'Machine': 'N/A',
                        'Operator': 'N/A',
                        'Quantity': quantity,
                        'Machining Rate (minutes/part)': machining_rate,
                        'Setup Rate (minutes/lot)': setup_rate,
                        'On-Machine Minutes': total_on_machine_minutes,
                        'Number of Lots': num_lots,
                        'Total Setup Time (minutes)': total_setup_time,
                        'Setup Time + Machine Time': total_setup_time + total_on_machine_minutes,
                        'Allocation %': 100.0
                    })
                else:
                    # Distribute time across all allocated machines
                    for allocation in machine_allocations:
                        machine = allocation['machine']
                        percentage = allocation['percentage']

                        on_machine_minutes = total_on_machine_minutes * percentage
                        setup_time = total_setup_time * percentage
                        setup_plus_machine = setup_time + on_machine_minutes

                        operator = self.machine_to_operator.get(machine, 'N/A')

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
                            'Total Setup Time (minutes)': setup_time,
                            'Setup Time + Machine Time': setup_plus_machine,
                            'Allocation %': percentage * 100
                        })

        return pd.DataFrame(output_rows) if output_rows else pd.DataFrame()

    def calculate_capacity_for_year(self, year):
        """Calculate bottleneck analysis for a specific year"""
        year_df = self.calculate_year_data(year)

        if year_df.empty:
            return None

        machine_totals = {}
        machine_mins = {}
        machine_columns = [col for col in self.machine_allocation.columns
                          if col not in ['Operations', 'Total']]

        # Machine totals (On-Machine Minutes + Setup Time - they work in series)
        for machine in year_df['Machine'].unique():
            if pd.notna(machine):
                machine_df = year_df[year_df['Machine'] == machine]
                # Combined time since setup and machining happen in series on the same machine
                machine_totals[machine] = machine_df['Setup Time + Machine Time'].sum()
                # Minimum operation time (also combined)
                op_mins = machine_df.groupby('Operation')['Setup Time + Machine Time'].sum()
                machine_mins[machine] = op_mins.min() if not op_mins.empty else 0

        # Calculate total vendor time
        total_vendor_time = 0
        for part_number in year_df['Part Number'].unique():
            if pd.notna(part_number) and part_number in self.part_vendor_time:
                part_rows = year_df[year_df['Part Number'] == part_number]
                if not part_rows.empty:
                    num_lots = part_rows.iloc[0]['Number of Lots']
                    total_vendor_time += self.part_vendor_time[part_number] * num_lots

        # Find bottleneck machine
        if machine_totals:
            max_minutes = max(machine_totals.values())
            bottleneck = [m for m, v in machine_totals.items() if v == max_minutes][0]

            other_machines_min = sum(
                machine_mins[machine]
                for machine in machine_mins
                if machine != bottleneck
            )

            total_minutes = max_minutes + other_machines_min + total_vendor_time

            return {
                'year_df': year_df,
                'total_minutes': total_minutes,
                'bottleneck': bottleneck,
                'resource_type': 'Machine',
                'max_minutes': max_minutes,
                'other_machines_min': other_machines_min,
                'vendor_time': total_vendor_time,
                'machine_totals': machine_totals
            }

        return None

    def calculate_all_years_with_overflow(self):
        """Calculate capacity for all years with overflow distribution logic"""
        year_data = {}

        # First pass: calculate raw capacity for each year
        for year in self.years:
            year_info = self.calculate_capacity_for_year(year)
            year_data[year] = year_info

        # Second pass: handle overflow distribution
        adjusted_capacity = {}
        overflow_info = {}
        received_from_future = {}  # Track what each year received from future years

        for year in self.years:
            if year_data.get(year) is None:
                adjusted_capacity[year] = 0
                overflow_info[year] = {'status': 'no_data', 'pulled_from': [], 'overflow': 0}
                received_from_future[year] = 0
                continue

            data = year_data[year]
            total_minutes = data['total_minutes']
            total_capacity = total_minutes / self.available_capacity

            overflow_info[year] = {'status': 'normal', 'pulled_from': [], 'overflow': 0}
            if year not in received_from_future:
                received_from_future[year] = 0

            if total_capacity >= 1.0:
                overflow = total_minutes - self.available_capacity
                overflow_info[year]['status'] = 'over_capacity'
                overflow_info[year]['overflow'] = overflow

                pulled_total = 0
                for prev_year in reversed([y for y in self.years if y < year]):
                    if prev_year in adjusted_capacity:
                        available_in_prev = self.available_capacity - adjusted_capacity[prev_year]
                        if available_in_prev > 0:
                            pull_amount = min(overflow, available_in_prev)
                            adjusted_capacity[prev_year] += pull_amount

                            # Track that prev_year received this amount from a future year
                            if prev_year not in received_from_future:
                                received_from_future[prev_year] = 0
                            received_from_future[prev_year] += pull_amount

                            overflow -= pull_amount
                            pulled_total += pull_amount
                            overflow_info[year]['pulled_from'].append({
                                'year': prev_year,
                                'amount': pull_amount,
                                'new_capacity': adjusted_capacity[prev_year] / self.available_capacity
                            })
                            if overflow <= 0:
                                break

                adjusted_capacity[year] = total_minutes - pulled_total
                overflow_info[year]['overflow'] = overflow

                if overflow > 0:
                    overflow_info[year]['status'] = 'critical'
            else:
                adjusted_capacity[year] = total_minutes

        return year_data, adjusted_capacity, overflow_info, received_from_future

def create_total_capacity_indicator(capacity_pct):
    """Create capacity indicator for total capacity card with percentage above the bar."""
    # Determine color based on capacity
    if capacity_pct < 0.8:
        color = '#10b981'  # Green
    elif capacity_pct <= 1.0:
        color = '#f59e0b'  # Yellow
    else:
        color = '#ef4444'  # Red

    # Create HTML with percentage above bar
    bar_html = f"""
    <div style="width: 100%;">
        <div style="text-align: center; margin-bottom: 0rem;">
            <span style="color: {color}; font-weight: 700; font-size: 2.5rem;">
                {capacity_pct:.1%}
            </span>
        </div>
        <div style="width: 100%; height: 28px; background: rgba(255,255,255,0.1);
                    border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,0.2);">
            <div style="width: {min(capacity_pct * 100, 100)}%; height: 100%; background: {color};
                        transition: width 0.3s ease;"></div>
        </div>
    </div>
    """
    return bar_html

# Main Streamlit App
st.markdown("<h1>🏭 Tufflex Production Capacity Utilization</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown(f"**Available Capacity**: 252 days × 18 hrs × 60 min = 272,160 min/year")

# Always use local inputs.xlsx file
uploaded_file = 'inputs.xlsx'

# Initialize efficiency in session state
if 'efficiency' not in st.session_state:
    st.session_state.efficiency = 0.85

# Initialize analyzer
analyzer = CapacityAnalyzer(efficiency=st.session_state.efficiency)

# Load data
with st.spinner("Loading and validating data..."):
    if analyzer.data_input_setup(uploaded_file):
        st.sidebar.success("✅ Data loaded successfully")
    else:
        st.error("Failed to load data. Please check your input file.")
        st.stop()

# Data validation section (collapsible)
# Check if there are any validation errors to auto-expand
has_validation_errors = (
    analyzer.validation_results['part_numbers']['status'] != 'success' or
    analyzer.validation_results['operations']['status'] != 'success' or
    analyzer.validation_results['machines']['status'] != 'success'
)

with st.expander("✅ Data Validation Results", expanded=has_validation_errors):
    # Part Numbers
    st.markdown("**📦 Part Numbers Validation**")
    if analyzer.validation_results['part_numbers']['status'] == 'success':
        st.success("✅ All part numbers are consistent across all sheets")
    else:
        st.warning("⚠️ Part number discrepancies found:")
        for disc in analyzer.validation_results['part_numbers']['discrepancies'][:5]:  # Show first 5
            st.error(f"**{disc['item']}** missing in: {', '.join(disc['missing_in'])}")
        if len(analyzer.validation_results['part_numbers']['discrepancies']) > 5:
            st.info(f"...and {len(analyzer.validation_results['part_numbers']['discrepancies']) - 5} more")

    st.markdown("**⚙️ Operations Validation**")
    if analyzer.validation_results['operations']['status'] == 'success':
        st.success("✅ All operations are consistent across all sheets")
    else:
        st.warning("⚠️ Operation discrepancies found:")
        for disc in analyzer.validation_results['operations']['discrepancies']:
            st.error(f"**{disc['item']}** missing in: {', '.join(disc['missing_in'])}")

    st.markdown("**🔧 Machines Validation**")
    if analyzer.validation_results['machines']['status'] == 'success':
        st.success("✅ All machines are consistent across all sheets")
    else:
        st.warning("⚠️ Machine discrepancies found:")
        for disc in analyzer.validation_results['machines']['discrepancies']:
            st.error(f"**{disc['item']}** missing in: {', '.join(disc['missing_in'])}")

# Initialize session state for selected year
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = analyzer.years[0]

# Calculate all years with overflow distribution
all_year_data, adjusted_capacity, overflow_info, received_from_future = analyzer.calculate_all_years_with_overflow()

# Create two-column layout: Left side (Year Selector + Total Capacity), Right side (Machine & Operator Details)
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    # Year Selector Section
    st.markdown("<h2>📅 Select Year</h2>", unsafe_allow_html=True)

    with st.container(border=True):
        # All year buttons in one row
        years_display = [str(year).replace(' Qty', '') for year in analyzer.years]
        cols = st.columns(len(years_display), gap="small")

        for year_idx, (col, year_display, year_value) in enumerate(zip(cols, years_display, analyzer.years)):
            with col:
                # Check if this year is selected
                is_selected = (st.session_state.selected_year == year_value)

                # Use primary type for selected year (blue), secondary for others
                button_type = "primary" if is_selected else "secondary"

                if st.button(
                    year_display,
                    key=f"year_btn_{year_idx}",
                    use_container_width=True,
                    type=button_type
                ):
                    st.session_state.selected_year = year_value
                    st.rerun()

    # Total Capacity Section
    st.markdown("<h2>📊 Total Capacity</h2>", unsafe_allow_html=True)

    year_info = all_year_data.get(st.session_state.selected_year)

    if year_info is not None:
        # Efficiency Factor Input (inline with card background)
        # SPACING CONTROL: Column proportions below control the width of each section
        # Format: [label_width, number_input_width]
        # Current proportions: [1.75, 1.5] - adjust these numbers to change spacing
        with st.container(border=True):
            col_label, col_number = st.columns([.6, 1.5])
            with col_label:
                # Height value controls vertical centering - matches height of input control
                st.markdown("<div style='display: flex; align-items: center; height: 40px;'><p style='margin: 0;'><strong>Efficiency (0.1 - 1.0)</strong></p></div>", unsafe_allow_html=True)
            with col_number:
                efficiency_number = st.number_input(
                    "Efficiency Number",
                    min_value=0.1,
                    max_value=1.0,
                    value=st.session_state.efficiency,
                    step=0.05,
                    help="Applied to both machining and setup rates. Lower efficiency increases required time.",
                    key="efficiency_number_input",
                    label_visibility="collapsed"
                )

            # Update session state if changed
            if abs(efficiency_number - st.session_state.efficiency) > 0.001:
                st.session_state.efficiency = efficiency_number
                st.rerun()

        # Use adjusted capacity (after overflow distribution)
        adjusted_minutes = adjusted_capacity[st.session_state.selected_year]
        total_capacity = adjusted_minutes / analyzer.available_capacity
        overflow_data = overflow_info[st.session_state.selected_year]

        # Total Capacity Card
        with st.container(border=True):
            # Capacity bar visualization
            st.markdown(
                f"<div style='margin-bottom: 1rem;'>"
                f"{create_total_capacity_indicator(total_capacity)}"
                f"</div>",
                unsafe_allow_html=True
            )

            # Expandable details matching print_total_capacity output
            with st.expander("📋 View Capacity Details"):
                st.markdown(f"**Bottleneck Machine:** {year_info['bottleneck']} - {year_info['max_minutes']:,.0f} minutes")
                st.markdown(f"**Other Machines Min Sum:** {year_info['other_machines_min']:,.0f} minutes")
                st.markdown(f"**Vendor Time:** {year_info['vendor_time']:,.0f} minutes")

                # Show total capacity with note about pulled from future years
                received_minutes = received_from_future.get(st.session_state.selected_year, 0)
                if received_minutes > 0:
                    st.markdown(f"**Total Capacity:** {total_capacity:.2%} ({adjusted_minutes:,.0f} / {analyzer.available_capacity:,} minutes) - *{received_minutes:,.0f} minutes pulled from future years*")
                else:
                    st.markdown(f"**Total Capacity:** {total_capacity:.2%} ({adjusted_minutes:,.0f} / {analyzer.available_capacity:,} minutes)")

                # Show overflow information if applicable
                if overflow_data['status'] == 'over_capacity' or overflow_data['status'] == 'critical':
                    st.markdown("---")
                    st.markdown("**⚠️ Overflow Distribution:**")
                    if overflow_data['pulled_from']:
                        for pull in overflow_data['pulled_from']:
                            st.markdown(f"→ Pulled **{pull['amount']:,.0f} minutes** into **{pull['year']}** (now at {pull['new_capacity']:.1%})")

                    if overflow_data['overflow'] > 0:
                        st.error(f"**CRITICAL**: Remaining overflow of **{overflow_data['overflow']:,.0f} minutes** cannot be accommodated!")

                    st.markdown(f"**Adjusted Capacity:** {total_capacity:.2%} ({adjusted_minutes:,.0f} / {analyzer.available_capacity:,} minutes)")
                    st.markdown(f"**Raw Total:** {year_info['total_minutes']:,.0f} minutes ({year_info['total_minutes']/analyzer.available_capacity:.2%})")

        # Operator Time Section
        st.markdown("<h2>👷 Operator Time</h2>", unsafe_allow_html=True)

        # Calculate operator data
        year_df = year_info['year_df']
        operator_data = {}
        for _, row in year_df.iterrows():
            operator = row['Operator']
            if pd.notna(operator) and isinstance(operator, str):
                operators = [op.strip() for op in operator.split(',')]
                num_ops = len(operators)
                setup_time_per_op = row['Total Setup Time (minutes)'] / num_ops if num_ops > 0 else 0

                for op in operators:
                    if op not in operator_data:
                        operator_data[op] = 0
                    operator_data[op] += setup_time_per_op

        with st.container(border=True):
            if operator_data:
                # Sort operators by setup time descending
                sorted_operators = sorted(operator_data.items(), key=lambda x: x[1], reverse=True)

                for operator, setup_time in sorted_operators:
                    st.markdown(f"**{operator}:** {setup_time:,.0f} minutes")
            else:
                st.info("No operator data available")
    else:
        st.info("No data available for this year")

with col_right:
    # Machine Capacity Section
    year_display = str(st.session_state.selected_year).replace(' Qty', '')
    st.markdown(f"<h2>🔧 Machine Capacity - {year_display}</h2>", unsafe_allow_html=True)

    if year_info is not None:
        year_df = year_info['year_df']

        # Get machines
        machines = sorted([m for m in year_df['Machine'].unique() if pd.notna(m)])

        # Display machine cards
        for machine in machines:
            machine_df = year_df[year_df['Machine'] == machine]

            total_on_machine = machine_df['On-Machine Minutes'].sum()
            total_setup = machine_df['Total Setup Time (minutes)'].sum()
            total_combined = machine_df['Setup Time + Machine Time'].sum()

            # Capacity based on combined time (setup + machine work in series)
            capacity_pct = total_combined / analyzer.available_capacity

            # Determine color based on capacity
            if capacity_pct < 0.8:
                color = '#10b981'  # Green
            elif capacity_pct <= 1.0:
                color = '#f59e0b'  # Yellow
            else:
                color = '#ef4444'  # Red

            # Machine card
            with st.container(border=True):
                # Machine header with percentage and bar graph
                st.markdown(
                    f"<div>"
                    f"<div style='display: flex; align-items: baseline; justify-content: center; margin-bottom: 0rem;'>"
                    f"<h3 style='margin: 0; font-size: 1.1rem; line-height: 0;'>⚙️ {machine}</h3>"
                    f"<span style='margin-left: 12px; color: {color}; font-weight: 600; font-size: 2rem; line-height: 1;'>"
                    f"{capacity_pct:.1%}"
                    f"</span>"
                    f"</div>"
                    f"<div style='margin-bottom: 0.75rem;'>"
                    f"<div style='width: 100%; height: 28px; background: rgba(255,255,255,0.1); "
                    f"border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,0.2);'>"
                    f"<div style='width: {min(capacity_pct * 100, 100)}%; height: 100%; background: {color}; "
                    f"transition: width 0.3s ease;'></div>"
                    f"</div>"
                    f"</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                # Expandable operations table
                with st.expander("📋 View Machine Details"):
                    # Get operator
                    operator = analyzer.machine_to_operator.get(machine, 'N/A')
                    st.markdown(f"**Operator:** {operator}  |  **On-Machine Minutes:** {total_on_machine:,.0f}  |  **Setup Time:** {total_setup:,.0f}  |  **Combined Time:** {total_combined:,.0f}")

                    if not machine_df.empty:
                        # Format the dataframe for display
                        display_df = machine_df[['Part Number', 'Operation', 'Allocation %', 'Quantity',
                                                'On-Machine Minutes', 'Number of Lots',
                                                'Total Setup Time (minutes)', 'Setup Time + Machine Time']].copy()

                        # Sort by combined time descending
                        display_df = display_df.sort_values('Setup Time + Machine Time', ascending=False)

                        # Format numbers
                        display_df['Allocation %'] = display_df['Allocation %'].round(0).astype(int)
                        display_df['Quantity'] = display_df['Quantity'].round(0).astype(int)
                        display_df['On-Machine Minutes'] = display_df['On-Machine Minutes'].round(0).astype(int)
                        display_df['Number of Lots'] = display_df['Number of Lots'].round(0).astype(int)
                        display_df['Total Setup Time (minutes)'] = display_df['Total Setup Time (minutes)'].round(0).astype(int)
                        display_df['Setup Time + Machine Time'] = display_df['Setup Time + Machine Time'].round(0).astype(int)

                        st.dataframe(
                            display_df,
                            use_container_width=True,
                            hide_index=True,
                            height=min(400, (len(display_df) + 1) * 35 + 38)
                        )
                    else:
                        st.info(f"No operations for {machine} in {year_display}")
    else:
        st.info(f"No data available for {year_display}")
