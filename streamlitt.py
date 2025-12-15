import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

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
    
    /* Center tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(145deg, #35354a, #3f3f57);
        padding: 0.75rem;
        border-radius: 15px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, #2a2a3a, #36364d);
        color: #f3f4f6 !important;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #60a5fa, #3b82f6) !important;
        color: white !important;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
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
    
    /* Dividers */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.5), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #2a2a3a, #36364d);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] p {
        color: #f3f4f6 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e1e2e;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label, [data-testid="stSidebar"] .stRadio label {
        color: #f3f4f6 !important;
    }
    
    /* Caption text */
    .stCaption, small {
        color: #9ca3af !important;
    }
    
    /* Bordered containers - section cards */
    div[data-testid="column"] > div > div > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(145deg, #2a2a3a, #36364d) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
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
    def __init__(self):
        self.merged = None
        self.machining_rates = None
        self.forecast_quantities = None
        self.years = None
        self.capacity_results = None
        self.machine_totals = {}
        self.machine_mins = {}
        self.available_capacity = 252 * 18 * 60  # 252 days * 18 hours * 60 minutes
    
    def data_input_setup(self, machining_rates_file, forecast_quantities_file):
        # Read the Excel files
        self.machining_rates = pd.read_excel(machining_rates_file)
        self.forecast_quantities = pd.read_excel(forecast_quantities_file)

        # Merge on Part Number
        self.merged = pd.merge(
            self.machining_rates,
            self.forecast_quantities,
            on='Part Number',
            how='outer',
            indicator=True
        )

        # Get year columns
        self.years = [col for col in self.forecast_quantities.columns if col not in ['Part Number']]
    
    def check_merge_errors(self):
        left_only = self.merged[self.merged['_merge'] == 'left_only']
        right_only = self.merged[self.merged['_merge'] == 'right_only']

        errors = []
        if len(left_only) > 0:
            errors.append(f"⚠️ WARNING: {len(left_only)} part numbers in machining_rates.xlsx not found in forecast_quantities.xlsx")
        if len(right_only) > 0:
            errors.append(f"⚠️ WARNING: {len(right_only)} part numbers in forecast_quantities.xlsx not found in machining_rates.xlsx")
        
        return errors if errors else ["✓ No errors!"]

    def operation_lines(self):
        operations = [col for col in self.machining_rates.columns if col not in ['Part Number']]
        
        self.capacity_results = {}
        
        for year in self.years:
            rows = []
            
            for _, row in self.merged.iterrows():
                part_number = row['Part Number']
                year_quantity = row[year]
                
                for op in operations:
                    rate = row[op]
                    rows.append({
                        'Part Number': part_number,
                        'Operation': op,
                        'Quantity': year_quantity,
                        'Rate (minutes/part)': rate,
                        'On-Machine Minutes': rate * year_quantity
                    })
            
            self.capacity_results[year] = pd.DataFrame(rows)
    
    def create_machine_data(self, allocation_file):
        """Create machine data based on operation allocation with support for split allocations."""
        allocation = pd.read_excel(allocation_file)
        machines = [col for col in allocation.columns if col not in ['Operations', 'Total']]
        
        machine_data = {}
        
        for year in self.years:
            capacity_data = self.capacity_results[year]
            
            if year not in self.machine_totals:
                self.machine_totals[year] = {}
            if year not in self.machine_mins:
                self.machine_mins[year] = {}
            
            machine_data[year] = {}
            
            for machine in machines:
                # Get operations with their allocation percentages for this machine
                machine_allocation = allocation[['Operations', machine]].copy()
                machine_allocation = machine_allocation[machine_allocation[machine] > 0]
                
                # Create empty list to store all rows for this machine
                machine_rows = []
                
                for _, alloc_row in machine_allocation.iterrows():
                    operation = alloc_row['Operations']
                    allocation_pct = alloc_row[machine]
                    
                    # Get all capacity data for this operation
                    op_data = capacity_data[
                        (capacity_data['Operation'] == operation) & 
                        (capacity_data['On-Machine Minutes'] > 0)
                    ].copy()
                    
                    if not op_data.empty:
                        # Check if this operation is split across multiple machines
                        op_total_allocation = allocation[allocation['Operations'] == operation][machines].sum(axis=1).values[0]
                        
                        if op_total_allocation > 0:
                            # Normalize allocation percentage if total is not 1
                            normalized_pct = allocation_pct / op_total_allocation
                            
                            # Check if this is the first machine in the allocation for this operation
                            # (to handle remainder)
                            machines_with_allocation = []
                            for m in machines:
                                if allocation[allocation['Operations'] == operation][m].values[0] > 0:
                                    machines_with_allocation.append(m)
                            is_first_machine = (machine == machines_with_allocation[0])
                            
                            # Split quantities according to allocation percentage
                            for idx, row in op_data.iterrows():
                                original_qty = row['Quantity']
                                rate = row['Rate (minutes/part)']
                                
                                # Calculate split quantity
                                split_qty = original_qty * normalized_pct
                                
                                # If this is the first machine, add the remainder rounded up
                                if is_first_machine and len(machines_with_allocation) > 1:
                                    # Calculate what would be distributed to other machines
                                    other_qty = 0
                                    for other_machine in machines_with_allocation[1:]:
                                        other_alloc = allocation[allocation['Operations'] == operation][other_machine].values[0]
                                        other_normalized_pct = other_alloc / op_total_allocation
                                        other_qty += math.floor(original_qty * other_normalized_pct)
                                    
                                    # First machine gets the remainder to ensure total matches
                                    split_qty = original_qty - other_qty
                                else:
                                    # Other machines get floored values
                                    split_qty = math.floor(split_qty)
                                
                                machine_rows.append({
                                    'Part Number': row['Part Number'],
                                    'Operation': operation,
                                    'Quantity': split_qty,
                                    'Rate (minutes/part)': rate,
                                    'On-Machine Minutes': split_qty * rate
                                })
                
                # Create dataframe from all rows
                if machine_rows:
                    machine_df = pd.DataFrame(machine_rows)
                else:
                    machine_df = pd.DataFrame(columns=['Part Number', 'Operation', 'Quantity', 'Rate (minutes/part)', 'On-Machine Minutes'])

                # Calculate totals
                total_minutes = machine_df['On-Machine Minutes'].sum()
                total_quantity = machine_df['Quantity'].sum()
                
                self.machine_totals[year][machine] = total_minutes
                self.machine_mins[year][machine] = machine_df['On-Machine Minutes'].min() if not machine_df.empty else 0
                
                machine_data[year][machine] = {
                    'data': machine_df,
                    'total_minutes': total_minutes,
                    'total_quantity': total_quantity
                }
        
        return machine_data, machines
    
    def get_total_capacity(self, year):
        """Calculate total capacity utilization for a year."""
        if year not in self.machine_totals or not self.machine_totals[year]:
            return None, None, None, None
        
        max_minutes = max(self.machine_totals[year].values())
        max_machine = [m for m, v in self.machine_totals[year].items() if v == max_minutes][0]
        
        other_machines_min = sum(
            self.machine_mins[year][machine] 
            for machine in self.machine_mins[year] 
            if machine != max_machine
        )
        
        total_minutes = max_minutes + other_machines_min
        total_capacity = total_minutes / self.available_capacity
        
        return total_capacity, total_minutes, max_machine, max_minutes

def create_capacity_indicator(capacity_pct):
    """Create a small colored bar indicator for capacity - green (<80%), yellow (80-100%), red (>100%)."""
    # Determine color based on capacity
    if capacity_pct < 0.8:
        color = '#10b981'  # Green
    elif capacity_pct <= 1.0:
        color = '#f59e0b'  # Yellow
    else:
        color = '#ef4444'  # Red
    
    # Create wider HTML bar that fills the card width
    bar_html = f"""
    <div style="display: flex; align-items: center; width: 100%;">
        <div style="flex: 1; height: 28px; background: rgba(255,255,255,0.1); 
                    border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,0.2);">
            <div style="width: {min(capacity_pct * 100, 100)}%; height: 100%; background: {color}; 
                        transition: width 0.3s ease;"></div>
        </div>
        <span style="margin-left: 12px; color: {color}; font-weight: 600; font-size: 1rem; min-width: 60px;">
            {capacity_pct:.1%}
        </span>
    </div>
    """
    return bar_html

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
st.markdown("<h1>🏭 Capacity Analysis Dashboard</h1>", unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.header("📂 Data Files")
upload_option = st.sidebar.radio(
    "Choose data source:",
    ["Use local files", "Upload files"]
)

if upload_option == "Upload files":
    machining_rates_upload = st.sidebar.file_uploader("Upload machining_rates.xlsx", type=['xlsx'])
    forecast_quantities_upload = st.sidebar.file_uploader("Upload forecast_quantities.xlsx", type=['xlsx'])
    allocation_upload = st.sidebar.file_uploader("Upload machine_allocation.xlsx", type=['xlsx'])
    
    if not all([machining_rates_upload, forecast_quantities_upload, allocation_upload]):
        st.info("👆 Please upload all three Excel files in the sidebar to begin.")
        st.stop()
    
    machining_rates_file = machining_rates_upload
    forecast_quantities_file = forecast_quantities_upload
    allocation_file = allocation_upload
else:
    # File paths - these should be in the same directory as this script
    machining_rates_file = 'machining_rates.xlsx'
    forecast_quantities_file = 'forecast_quantities.xlsx'
    allocation_file = 'machine_allocation.xlsx'

# Initialize analyzer
analyzer = CapacityAnalyzer()

try:
    # Load and process data
    with st.spinner("Loading data..."):
        analyzer.data_input_setup(machining_rates_file, forecast_quantities_file)
        analyzer.operation_lines()
        machine_data, machines = analyzer.create_machine_data(allocation_file)
    
    
    # Initialize session state for selected year
    if 'selected_year' not in st.session_state:
        st.session_state.selected_year = analyzer.years[0]
    
    # Create two-column layout: Left side (Year Selector + Total Capacity), Right side (Machine Details)
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
        
        # Total Capacity Section - Simplified Card
        st.markdown("<h2>📊 Total Capacity</h2>", unsafe_allow_html=True)
        total_capacity, total_minutes, bottleneck_machine, bottleneck_minutes = analyzer.get_total_capacity(st.session_state.selected_year)
        
        if total_capacity is not None:
            # Calculate other machines minimum sum
            other_machines_min = sum(
                analyzer.machine_mins[st.session_state.selected_year][machine] 
                for machine in analyzer.machine_mins[st.session_state.selected_year] 
                if machine != bottleneck_machine
            )
            
            # Total Capacity Card - Only bar visualization
            with st.container(border=True):
                # Capacity bar visualization only
                st.markdown(
                    f"<div style='margin-bottom: 1rem;'>"
                    f"{create_total_capacity_indicator(total_capacity)}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
                # Expandable details matching print_total_capacity output
                with st.expander("📋 View Capacity Details"):
                    st.markdown(f"**Bottleneck Machine:** {bottleneck_machine} ({bottleneck_minutes:,.0f} minutes)")
                    st.markdown(f"**Other Machines Min Sum:** {other_machines_min:,.0f} minutes")
                    st.markdown(f"**Total Capacity:** {total_capacity:.2%} ({total_minutes:,.0f} / {analyzer.available_capacity:,} minutes)")
        else:
            st.info("No data available for this year")
    
    with col_right:
        # Machine Details Section - All machines vertically
        year_display = str(st.session_state.selected_year).replace(' Qty', '')
        st.markdown(f"<h2>🔧 Machine Details - {year_display}</h2>", unsafe_allow_html=True)
        
        # Create machine cards vertically (one per row)
        machines_list = list(machines)
        for machine in machines_list:
            if machine in machine_data[st.session_state.selected_year]:
                machine_info = machine_data[st.session_state.selected_year][machine]
                machine_df = machine_info['data']
                total_minutes = machine_info['total_minutes']
                capacity_pct = total_minutes / analyzer.available_capacity
                
                # Machine card - simplified and compact
                with st.container(border=True):
                    # Determine color based on capacity
                    if capacity_pct < 0.8:
                        color = '#10b981'  # Green
                    elif capacity_pct <= 1.0:
                        color = '#f59e0b'  # Yellow
                    else:
                        color = '#ef4444'  # Red
                    
                    # Machine header with percentage and bar graph in one markdown call
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
                    with st.expander("📋 View Operations Details"):
                        if not machine_df.empty:
                            # Format the dataframe for display
                            display_df = machine_df.copy()
                            display_df['Quantity'] = display_df['Quantity'].fillna(0).round(2)
                            display_df['Rate (minutes/part)'] = display_df['Rate (minutes/part)'].fillna(0).round(2)
                            display_df['On-Machine Minutes'] = display_df['On-Machine Minutes'].fillna(0).round(2)
                            
                            # Sort by on-machine minutes descending
                            display_df = display_df.sort_values('On-Machine Minutes', ascending=False)
                            
                            # Add summary row
                            summary_row = pd.DataFrame({
                                'Part Number': ['TOTAL'],
                                'Operation': [''],
                                'Quantity': [float(display_df['Quantity'].sum())],
                                'Rate (minutes/part)': [0.0],
                                'On-Machine Minutes': [float(display_df['On-Machine Minutes'].sum())]
                            })
                            
                            display_df = pd.concat([display_df, summary_row], ignore_index=True)
                            
                            st.dataframe(
                                display_df,
                                use_container_width=True,
                                hide_index=True,
                                height=min(400, (len(display_df) + 1) * 35 + 38)
                            )
                        else:
                            st.info(f"No operations for {machine} in {year_display}")

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.exception(e)
