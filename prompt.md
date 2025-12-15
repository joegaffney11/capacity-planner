# Claude Code: Update Streamlit Capacity Dashboard

## Context
I have a manufacturing capacity analysis system with two main files:
1. **capacity_processor.py** - A data processing script that has been significantly enhanced with new features
2. **streamlitt.py** - A Streamlit dashboard that needs to be updated to reflect the new functionality

## Current State
The dashboard currently shows:
- Year selection
- Total capacity visualization with bottleneck analysis
- Machine-level capacity details
- Operations breakdown per machine

## New Features to Integrate
The processor now includes several major enhancements that need to be reflected in the dashboard:

### 1. **Multi-Sheet Input System**
- The processor now reads from a single `inputs.xlsx` file with multiple sheets:
  - Quantities
  - Avg Parts per Lot
  - Machining Rates
  - Setup Rates
  - Vendor Time
  - Machine Allocation
  - Setup Allocation

### 2. **Comprehensive Data Validation**
The processor validates three critical areas:
- **Part Number Consistency**: Checks that all part numbers appear in all required sheets (Quantities, Avg Parts per Lot, Machining Rates, Setup Rates, Vendor Time)
- **Operation Consistency**: Validates that operations match across Machining Rates, Setup Rates, and Machine Allocation
- **Machine Consistency**: Ensures machines are defined in both Machine Allocation and Setup Allocation

### 3. **Enhanced Capacity Calculations**
New metrics now calculated:
- **Setup Time Analysis**: 
  - Total Setup Time per operation/part
  - Setup Time + Machine Time combined metric
  - Number of lots calculated from quantities and average parts per lot
- **Operator Assignments**:
  - Maps machines to operators via Setup Allocation sheet
  - Tracks operator capacity separately from machine capacity
  - Handles multi-operator scenarios (operators can be shared across machines)
- **Vendor Time**:
  - Tracks vendor lead time per lot (in business days)
  - Converts to minutes and includes in total capacity calculation
  - Multiplies by number of lots for total vendor impact

### 4. **Advanced Bottleneck Analysis**
The processor now identifies bottlenecks across THREE resource types:
- **Machines** (using On-Machine Minutes)
- **Operators** (using Total Setup Time, divided among shared operators)
- **Vendor Time** (per-lot vendor time × number of lots)

Total capacity calculation:
```
Total Capacity = Bottleneck Resource + Sum of Other Resources' Minimums + Total Vendor Time
```

### 5. **Early Start Analysis**
When capacity exceeds 100% in a year:
- The system looks at previous years for available capacity
- Attempts to "pull forward" work into earlier years
- Shows which years absorb overflow work
- Warns if capacity cannot be accommodated even with early starts

### 6. **Efficiency Factor**
- User can input an efficiency factor (0-1)
- Applied to both machining rates and setup rates
- Adjusts all time calculations accordingly

### 7. **Enhanced Output Format**
Output Excel file now includes per-year sheets with columns:
- Part Number
- Operation
- Machine (assigned via Machine Allocation)
- Operator (assigned via Setup Allocation)
- Quantity
- Machining Rate (minutes/part)
- Setup Rate (minutes/lot)
- On-Machine Minutes
- Number of Lots
- Total Setup Time (minutes)
- Setup Time + Machine Time

## Dashboard Update Requirements

### High Priority Updates:

#### 1. **Input System Overhaul**
- Replace the three-file upload system with a single `inputs.xlsx` upload
- Add file validation that checks for all required sheets
- Display validation warnings prominently if data issues are found

#### 2. **Data Validation Dashboard Section**
Create a new expandable section showing:
- Part number validation status with specific discrepancies
- Operation validation status with specific discrepancies  
- Machine validation status with specific discrepancies
- Use color coding: green for validated, yellow/red for issues
- Show which sheets are missing which items

#### 3. **Efficiency Input**
- Add a sidebar input for efficiency factor (0.0 to 1.0, default 0.85)
- Show how efficiency affects calculations
- Recalculate all metrics when efficiency changes

#### 4. **Enhanced Capacity Metrics**
Update the capacity display to show:
- **Resource Type** of bottleneck (Machine, Operator, or Vendor)
- **Setup Time** alongside machine time
- **Operator Utilization** section showing:
  - Each operator's total setup time
  - Which machines they serve
  - Their capacity percentage
- **Vendor Time Impact** showing:
  - Total vendor time for the year
  - Which parts contribute most to vendor time

#### 5. **Early Start Analysis Visualization**
Create a new section showing:
- Multi-year capacity timeline
- Visual indication of years at or over 100% capacity
- Arrows or flows showing work pulled into earlier years
- Color coding for years with overflow (red), receiving overflow (yellow), normal (green)

#### 6. **Machine Detail Enhancements**
For each machine, show:
- On-Machine Minutes (existing)
- Total Setup Time (NEW)
- Combined Time (Setup + Machine) (NEW)
- Assigned Operator(s) (NEW)
- Operations table should include Setup Rate and Number of Lots

#### 7. **New "Operations View" Tab**
Add a new tab showing operations across all machines:
- Grouped by operation
- Shows which machines can perform each operation
- Total time per operation
- Setup time vs. machine time breakdown

#### 8. **New "Operator View" Tab**  
Add a tab dedicated to operator analysis:
- Each operator's total setup time
- Machines they operate
- Capacity utilization
- Breakdown by operation

#### 9. **Enhanced Bottleneck Analysis**
Update the bottleneck display to:
- Clearly identify resource type (Machine/Operator/Vendor)
- Show the bottleneck percentage
- Display other resources' minimum sum
- Show vendor time separately
- Explain how total capacity is calculated

### Medium Priority Updates:

#### 10. **Interactive Filtering**
Add filters for:
- Part numbers
- Operations
- Machines
- Operators
- Capacity threshold (e.g., show only machines >80%)

#### 11. **Export Functionality**
- Allow users to download filtered/selected data
- Export capacity reports as PDF or Excel
- Include validation results in export

#### 12. **Comparison View**
- Side-by-side year comparison
- Show year-over-year changes
- Highlight growing bottlenecks

### Visual Design Requirements:

1. **Maintain Current Aesthetic**: Keep the dark theme, blue gradients, and modern styling
2. **Color Coding System**:
   - Green: <80% capacity
   - Yellow/Orange: 80-100% capacity  
   - Red: >100% capacity
   - Blue: Informational/neutral
3. **Responsive Layout**: Ensure new sections work well on different screen sizes
4. **Loading States**: Add spinners and progress indicators for heavy calculations
5. **Error Handling**: Graceful handling of missing data or validation failures

### Technical Considerations:

1. **Data Flow**:
   - Read from `inputs.xlsx` instead of separate files
   - Validate data immediately after loading
   - Cache processed data to avoid recalculation
   - Use session state for efficiency factor and filters

2. **Performance**:
   - Lazy load detailed data tables
   - Use pagination for large datasets
   - Consider using @st.cache_data for expensive calculations

3. **Code Organization**:
   - Create helper functions for validation displays
   - Separate visualization functions from data processing
   - Keep the CapacityAnalyzer class structure but adapt for new input format

4. **User Experience**:
   - Show loading messages during processing
   - Provide tooltips explaining metrics
   - Add "What's This?" expandables for complex calculations
   - Include sample data or a demo mode

## Expected Deliverables:

1. **Updated streamlitt.py** with all new features integrated
2. **Updated CapacityAnalyzer class** matching the processor's new functionality
3. **README or documentation** explaining new features and how to use them
4. **Sample inputs.xlsx** structure for testing (or instructions to create one)

## Testing Requirements:

- Validate with missing data in various sheets
- Test with efficiency factors from 0.5 to 1.0
- Verify calculations match the processor output
- Test with years that exceed 100% capacity
- Verify operator assignment logic with shared operators
- Test vendor time calculations with various lot sizes

## Success Criteria:

The updated dashboard should:
1. ✅ Accept single inputs.xlsx file instead of multiple files
2. ✅ Display comprehensive data validation results
3. ✅ Show machine, operator, AND vendor capacity metrics
4. ✅ Include setup time in all relevant calculations
5. ✅ Visualize early start analysis for over-capacity years
6. ✅ Provide operator-specific capacity views
7. ✅ Maintain or improve current visual design quality
8. ✅ Handle errors gracefully with helpful messages
9. ✅ Allow efficiency factor adjustment
10. ✅ Match calculations from capacity_processor.py exactly

## Additional Notes:

- The processor uses an available capacity of 252 days × 18 hours × 60 minutes per year
- Operator setup time is divided among operators when multiple operators work on the same machine
- Vendor time is calculated as: vendor_days × 18 hours/day × 60 minutes/hour × number_of_lots
- The bottleneck can be ANY resource type (machine, operator, or vendor)
- Early start analysis only looks backward (pulling work into earlier years, not forward)

Please update the Streamlit dashboard to incorporate all these enhancements while maintaining the beautiful, professional design and user experience.
