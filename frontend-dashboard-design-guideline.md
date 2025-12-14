# Frontend Dashboard Design Guideline

This document provides comprehensive design principles and patterns for creating professional, modern dashboards. Use this as a reference when building data visualization interfaces.

---

## Color Palette & Theme

### Primary Colors
- **Background**: Dark theme with `#1a1a2e` as the main background
- **Accent Blue**: `#60a5fa` (light blue) and `#3b82f6` (medium blue) for highlights and interactive elements
- **Text**: `#f3f4f6` for primary text (light gray for readability on dark backgrounds)
- **Container Backgrounds**: Gradient backgrounds using `#2a2a3a` to `#36364d` for cards and sections

### Color Usage Principles
- Use blue gradients for headers and important UI elements
- Maintain high contrast (light text on dark backgrounds)
- Apply subtle gradients for depth: `linear-gradient(145deg, #35354a, #3f3f57)`
- Use shadow effects to create elevation: `0 10px 25px rgba(0, 0, 0, 0.2)`

---

## Typography

### Font Family
- **Primary Font**: 'Inter' (Google Fonts)
- **Fallback**: Sans-serif system fonts
- Import: `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap')`

### Font Weights
- Regular (400): Body text
- Medium (500): Labels and secondary headings
- Semi-bold (600): Important UI elements
- Bold (700): Primary headings

### Text Hierarchy
```
H1: Large gradient background headers (2rem padding, centered)
H2: Section headers with bottom border (color: #60a5fa, centered)
H3: Subsection headers (2rem font size, color: #60a5fa)
Body: Standard text (color: #f3f4f6)
```

### Text Effects
- **H1 Headers**: 
  - Gradient background: `linear-gradient(135deg, #60a5fa, #3b82f6, #1d4ed8)`
  - Box shadow: `0 15px 35px rgba(59, 130, 246, 0.3)`
  - Text shadow: `0 2px 4px rgba(0, 0, 0, 0.3)`
- **H2 Headers**: 
  - Bottom border: `2px solid #60a5fa`
  - Subtle text shadow

---

## Layout Principles

### Spacing & Padding
- **Container Padding**: `2rem 3rem` for main content areas
- **Card Padding**: `1.5rem` for internal card content
- **Element Margins**: `1rem` to `2rem` between major sections
- **Consistent Gaps**: Use standardized spacing (0.5rem, 1rem, 1.5rem, 2rem)

### Grid System
- Use multi-column layouts for metrics and cards
- Responsive columns that adapt to content
- Equal-width columns for balanced visual weight
- Example: 3-column layout for key metrics, 2-column for detailed views

### Container Patterns
```css
Background: linear-gradient(145deg, #2a2a3a, #36364d)
Border-radius: 12px to 20px (larger for prominent elements)
Box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25)
Border: 1px solid rgba(255, 255, 255, 0.08) for subtle definition
```

---

## Component Design Patterns

### Metric Cards
- **Metric Value**: Large, bold, blue text (`#60a5fa`, 1.5rem+, bold)
- **Metric Label**: Smaller, medium weight text (`#f3f4f6`, 0.9rem)
- **Layout**: Value on top, label below
- **Delta Indicators**: Green for positive, red for negative with appropriate icons

### Expandable Sections (Accordions)
```css
Header Background: linear-gradient(145deg, #35354a, #3f3f57)
Border-radius: 10px for headers, 15px for containers
Padding: 0.75rem 1rem for header
Content Padding: 0.5rem
Border: 1px solid rgba(255, 255, 255, 0.1)
Maintain consistent background in all states (collapsed/expanded)
```

### Buttons
- **Primary Button**: Blue background, white text, rounded corners
- **Secondary Button**: Outlined style with blue border
- **Button States**: Clear hover and active states with color transitions
- **Full Width**: Use `use_container_width=True` for form buttons

### Input Fields
```css
Background: Slightly lighter than container (#35354a range)
Border: 1px solid rgba(255, 255, 255, 0.1)
Border-radius: 8px
Padding: 0.75rem
Text Color: #f3f4f6
Focus State: Blue border glow
```

### Sidebar
```css
Background: #16213e or similar dark blue
Width: Appropriate for navigation (250-300px)
State: Expanded by default for desktop
Border: Subtle right border to separate from main content
```

---

## Data Visualization

### Chart Styling (Plotly)
```python
Theme: Dark background ('rgba(0,0,0,0)' for transparency)
Plot Background: '#2a2a3a'
Paper Background: 'rgba(0,0,0,0)'
Grid: Subtle gray (#404040) with low opacity
Text Color: #f3f4f6 for all labels and titles
Font Family: 'Inter'
```

### Chart Types & Usage
1. **Bar Charts**: For comparing discrete values (e.g., capacity by machine)
2. **Gauge Charts**: For showing percentage utilization or progress
3. **Line Charts**: For trends over time
4. **Waterfall Charts**: For showing sequential contributions

### Chart Best Practices
- Consistent color scheme across all charts (blues and complementary colors)
- Clear axis labels with appropriate font sizes
- Tooltips with detailed information
- Legend positioned to not obscure data
- Margins: Adequate spacing around charts (l=80, r=80, t=100, b=80)

### Interactive Features
- Hover effects with detailed tooltips
- Zoom and pan capabilities where appropriate
- Click interactions for drill-down functionality
- Responsive sizing with appropriate height (400-600px typical)

---

## Interactive Elements

### Tables & DataFrames
- **Styling**: Hide index, use clean headers
- **Formatting**: Right-align numbers, left-align text
- **Alternating Rows**: Subtle background difference for readability
- **Column Width**: Auto-adjust or fixed based on content type
- **Scrollable**: Enable vertical scroll for long tables

### Select Boxes & Dropdowns
```css
Background: #35354a
Border: 1px solid rgba(255, 255, 255, 0.1)
Border-radius: 8px
Option Background: #2a2a3a
Hover State: Slightly lighter background
Selected State: Blue accent
```

### Number Inputs
- Clear min/max constraints
- Appropriate step values (0.1 for decimals, 1 for integers)
- Inline labels positioned to the left
- Validation feedback (error states in red)

### Radio Buttons & Checkboxes
- Horizontal layout for binary choices
- Clear active state with blue accent
- Adequate spacing between options
- Labels clearly associated with controls

---

## Dashboard Sections & Organization

### 1. Header Section
- Large, prominent title with gradient background
- Optional subtitle or description
- Center-aligned for visual impact
- Adequate bottom margin (2rem)

### 2. Controls/Filter Section
- Sidebar for persistent filters (year selection, machine selection, etc.)
- Inline filters for quick adjustments
- Clear labels for all controls
- Grouped related controls together

### 3. Key Metrics Section
- Top row showing 3-5 critical metrics
- Large, easy-to-read numbers
- Delta indicators where relevant
- Equal-width columns for balance

### 4. Visualization Section
- Multiple chart types as needed
- Organized in logical groups or tabs
- Full-width or multi-column layouts
- Each chart with clear title

### 5. Detailed Data Section
- Expandable/collapsible for space efficiency
- Tables with raw data
- Download options where appropriate
- Search and filter capabilities

### 6. Action/Edit Section
- Modal dialogs or expandable sections for editing
- Clear "Apply" and "Cancel" actions
- Form validation with helpful error messages
- Success/error notifications

---

## Responsive Design Principles

### Mobile Considerations
- Stack columns vertically on small screens
- Maintain readable font sizes (minimum 14px)
- Touch-friendly button sizes (minimum 44px height)
- Simplified charts or alternative views for mobile

### Desktop Optimizations
- Wide layout utilizing full screen width
- Multi-column layouts for efficient space usage
- Sidebar visible by default
- Larger charts with more detail

---

## Animation & Transitions

### Micro-interactions
- Smooth transitions: `transition: all 0.3s ease`
- Hover states on interactive elements
- Loading states with spinners or progress indicators
- Fade-in effects for content that loads asynchronously

### Performance
- Avoid animating large datasets
- Use CSS transforms for smooth animations
- Debounce rapid user inputs
- Lazy load heavy components

---

## Accessibility Guidelines

### Color Contrast
- Maintain WCAG AA standards (4.5:1 minimum)
- Light text (#f3f4f6) on dark backgrounds (#1a1a2e) exceeds this
- Ensure interactive elements have sufficient contrast
- Don't rely solely on color to convey information

### Keyboard Navigation
- All interactive elements keyboard accessible
- Clear focus indicators
- Logical tab order
- Keyboard shortcuts for common actions

### Screen Readers
- Semantic HTML elements
- ARIA labels where needed
- Descriptive link text
- Alt text for visual elements

---

## Error Handling & User Feedback

### Success Messages
```python
Style: Green checkmark icon, light green background
Duration: Auto-dismiss after 3-5 seconds
Position: Top-right corner or inline near affected element
```

### Error Messages
```python
Style: Red X icon, light red background
Duration: Persistent until dismissed or issue resolved
Content: Clear explanation of error and how to fix
```

### Warning Messages
```python
Style: Yellow/orange alert icon, amber background
Use: For non-critical issues or confirmations needed
```

### Info Messages
```python
Style: Blue info icon, light blue background
Use: For helpful tips or additional context
```

---

## Code Organization Best Practices

### Structure
```python
1. Imports and configuration
2. Custom CSS/styling
3. Helper functions
4. Session state initialization
5. Sidebar/controls
6. Main content sections
7. Error handling wrapper
```

### Session State Management
- Initialize all session state variables at startup
- Use descriptive keys: `st.session_state.selected_year`
- Clear state when needed to reset UI
- Avoid storing large objects unnecessarily

### Reusability
- Extract repeated styling into variables
- Create functions for complex chart configurations
- Use loops for repetitive UI elements
- Separate data processing from display logic

---

## Performance Optimization

### Data Loading
- Cache data loading functions: `@st.cache_data`
- Load data once, filter in memory
- Use efficient data structures (pandas DataFrames)
- Lazy load heavy visualizations

### Rendering
- Minimize use of `st.rerun()` - only when necessary
- Update only changed components
- Use columns and containers efficiently
- Avoid nested containers when not needed

### User Experience
- Show loading indicators for slow operations
- Provide immediate feedback for user actions
- Use optimistic UI updates where safe
- Debounce inputs that trigger expensive operations

---

## Design Checklist

Before finalizing your dashboard, verify:

- [ ] Consistent color palette throughout
- [ ] All text is readable with sufficient contrast
- [ ] Responsive layout works on different screen sizes
- [ ] Interactive elements have clear hover/active states
- [ ] Charts are properly labeled and formatted
- [ ] Loading states are shown for async operations
- [ ] Error handling provides clear user guidance
- [ ] Navigation is intuitive and accessible
- [ ] Data refreshes properly when filters change
- [ ] All numbers are formatted appropriately
- [ ] Success/error messages are clear and helpful
- [ ] No console errors or warnings
- [ ] Performance is acceptable for expected data volumes

---

## Example Implementation Snippets

### Metric Display
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Total Capacity",
        value=f"{total_minutes:,.0f} min",
        delta=f"{delta_percent}% vs target"
    )
```

### Styled Container
```python
with st.container():
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    st.subheader("Section Title")
    # Content here
    st.markdown('</div>', unsafe_allow_html=True)
```

### Chart Configuration
```python
fig = go.Figure()
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#2a2a3a',
    font=dict(family='Inter', color='#f3f4f6'),
    margin=dict(l=80, r=80, t=100, b=80),
    height=500
)
```

### Form with Validation
```python
with st.form("input_form"):
    value = st.number_input("Enter value", min_value=0, max_value=100)
    submitted = st.form_submit_button("Submit", use_container_width=True, type="primary")
    
    if submitted:
        if value > 0:
            st.success("✅ Value submitted successfully")
        else:
            st.error("❌ Value must be greater than 0")
```

---

## Summary

This design system prioritizes:
1. **Visual Clarity**: High contrast, clear hierarchy, readable typography
2. **Professional Aesthetics**: Modern gradients, shadows, and spacing
3. **User Experience**: Intuitive navigation, helpful feedback, responsive design
4. **Data Focus**: Charts and metrics prominently displayed and easy to understand
5. **Consistency**: Unified color palette, spacing system, and component styling

Apply these principles consistently across all dashboard pages for a cohesive, professional user experience.
