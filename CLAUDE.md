# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a manufacturing capacity planning and analysis system that processes production data from Excel files and generates capacity reports. The system consists of:

1. **capacity_processor.py** - Core data processing engine that reads production inputs and generates yearly capacity analysis
2. **capacity_dashboard.py** - Streamlit-based interactive dashboard (placeholder/in development)
3. **inputs.xlsx** - Multi-sheet input workbook containing production data
4. **output.xlsx** - Generated output workbook with processed capacity data by year

## Running the Application

### Process Capacity Data
```bash
python capacity_processor.py
```
This will:
- Prompt for efficiency value (0-1 decimal, e.g., 0.85 for 85% efficiency)
- Read data from `inputs.xlsx`
- Validate part numbers, operations, and machines across all input sheets
- Generate `output.xlsx` with capacity analysis for each year
- Display bottleneck analysis and capacity warnings in console

### Launch Dashboard (when implemented)
```bash
streamlit run capacity_dashboard.py
```

## Dependencies

Install required packages:
```bash
pip install pandas numpy openpyxl streamlit plotly streamlit-aggrid
```

Core libraries:
- **pandas** - DataFrame operations and Excel I/O
- **numpy** - Numerical calculations (ceiling for lot calculations)
- **openpyxl** - Excel file engine for pandas
- **streamlit** - Web dashboard framework
- **plotly** - Interactive charting library

## Input Data Structure (inputs.xlsx)

The system expects 7 sheets in `inputs.xlsx`:

1. **Quantities** - Part numbers and yearly production quantities
2. **Avg Parts per Lot** - Average parts produced per manufacturing lot
3. **Machining Rates** - Time (minutes/part) for each operation
4. **Setup Rates** - Setup time (minutes/lot) for each operation
5. **Vendor Time** - External vendor lead time (business days per lot)
6. **Machine Allocation** - Maps operations to machines
7. **Setup Allocation** - Maps machines to operators

**Critical constraint**: Part numbers must be consistent across all sheets. Operations must be consistent across Machining Rates, Setup Rates, and Machine Allocation. Machines must be consistent across Machine Allocation and Setup Allocation. The processor validates this on startup.

## Core Architecture

### Data Flow

```
inputs.xlsx → capacity_processor.py → output.xlsx
                      ↓
            Console Bottleneck Analysis
```

### Key Processing Steps (capacity_processor.py)

1. **Validation Phase** (lines 22-164)
   - Cross-sheet validation of part numbers using outer merge
   - Cross-sheet validation of operations across machining/setup/allocation
   - Cross-sheet validation of machines across allocation sheets
   - Reports discrepancies before processing

2. **Mapping Creation** (lines 167-209)
   - `part_vendor_time` dict: part number → vendor time in minutes (converts days to minutes using 18-hour business days)
   - `operation_to_machine` dict: operation → assigned machine (first machine with >0 allocation)
   - `machine_to_operator` dict: machine → operator name(s)

3. **Output Generation** (lines 214-296)
   - For each year in Quantities sheet:
     - For each part with non-zero quantity:
       - Calculate number of lots: `ceil(quantity / parts_per_lot)`
       - For each operation with non-zero machining rate:
         - Calculate on-machine minutes: `quantity × machining_rate / efficiency`
         - Calculate total setup time: `num_lots × setup_rate / efficiency`
         - Create output row with machine, operator, and time calculations
   - Generates one sheet per year in output.xlsx

4. **Bottleneck Analysis** (lines 300-438)
   - Calculates available capacity: 252 days × 18 hours × 60 minutes = 272,160 minutes/year
   - For each year:
     - Sums on-machine minutes by machine
     - Sums setup time by operator (divided by number of operators if shared)
     - Calculates vendor time: `vendor_time_per_lot × num_lots` for each part
     - Identifies bottleneck: resource (machine or operator) with maximum total time
     - Calculates total capacity: `bottleneck_time + sum(min_time_for_other_resources) + vendor_time`
     - If over capacity (≥100%), attempts to pull work into prior years with available capacity
     - Reports final capacity percentage and overflow warnings

### Critical Calculation Details

- **Business day conversion**: Vendor time in days → minutes uses `days × 18 × 60` (18-hour days)
- **Lot calculation**: Uses `np.ceil()` to round up partial lots
- **Efficiency factor**: User-provided efficiency (0-1) is applied as divisor to both machining and setup rates, increasing required time
- **Shared operators**: When multiple operators are assigned to a machine (comma-separated), setup time is divided equally among them
- **Bottleneck logic**: The bottleneck resource runs at full capacity; all other resources only need to cover their minimum single-operation time
- **Early start logic**: Overflow capacity can be pulled into previous years if they have available capacity

## Dashboard Design Guidelines

See `frontend-dashboard-design-guideline.md` for comprehensive UI/UX patterns:

- **Dark theme**: Primary background `#1a1a2e`, accent blue `#60a5fa`
- **Typography**: 'Inter' font from Google Fonts
- **Charts**: Plotly with dark theme, transparent paper background, `#2a2a3a` plot background
- **Components**: Gradient containers with `linear-gradient(145deg, #2a2a3a, #36364d)`, border-radius 12-20px
- **Layout**: Multi-column metrics, expandable sections, sidebar filters
- **Interactivity**: Hover states, smooth transitions, clear feedback messages

When building dashboard features, always reference the design guideline for consistent styling.

## Common Modifications

### Changing Capacity Assumptions
- Available capacity calculation: capacity_processor.py:305
- Business days per year: 252 (hardcoded)
- Hours per business day: 18 (hardcoded in vendor time conversion at line 173)

### Adding New Operations
1. Add column to Machining Rates sheet
2. Add column to Setup Rates sheet
3. Add row to Machine Allocation sheet
4. Assign machine and operator in allocation sheets
5. Validation will confirm consistency on next run

### Modifying Bottleneck Logic
- Resource totals calculation: capacity_processor.py:316-348
- Bottleneck selection: capacity_processor.py:365-375
- Early start capacity pull: capacity_processor.py:418-429

### Dashboard Development
- The capacity_dashboard.py file is currently a placeholder
- When implementing, follow patterns in frontend-dashboard-design-guideline.md
- Use `@st.cache_data` for loading Excel files
- Key visualizations needed:
  - Capacity utilization by year (gauge or bar chart)
  - Bottleneck comparison across years
  - Machine/operator utilization breakdown
  - Vendor time vs. internal time comparison
  - Part-level detail tables with filtering

## File Locations

- Input data: `inputs.xlsx` (must be in same directory as scripts)
- Output data: `output.xlsx` (generated in same directory)
- Main processor: `capacity_processor.py`
- Dashboard app: `capacity_dashboard.py`
- Design guide: `frontend-dashboard-design-guideline.md`

## Troubleshooting

**"Error reading input file"**: Ensure `inputs.xlsx` exists in working directory with all 7 required sheets

**Validation warnings**: Review reported discrepancies - missing part numbers, operations, or machines will cause incomplete analysis

**Over capacity warnings**: System will attempt early start into prior years; if still over capacity after pull-back, manual intervention needed (increase efficiency, add machines, or reduce quantities)

**Empty output sheets**: Check that year has non-zero quantities in inputs.xlsx
