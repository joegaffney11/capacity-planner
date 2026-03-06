# Dashboard Compatibility Update Plan

## What Changed in the Excel File

### Sheet Renames

| Old Sheet Name | New Sheet Name |
|---|---|
| `Avg Parts per Lot` | `Number of Setups` |
| `Machining Rates` | `Machining Rates (mins per prt)` |
| `Setup Rates` | `Setup Rates (hours per order)` |

One new sheet was added (`Parameters Master Lists`) that the dashboard doesn't need to read.

### Column Rename: `Part Number` -> `Associated Part Numbers`

Applies to: `Quantities`, `Machining Rates (mins per prt)`, `Setup Rates (hours per order)`, `Vendor Time`.

### Logic Change: `Avg Parts per Lot` -> `Number of Setups`

**Old logic:**
```
partsPerLot = avgPartsPerLot[partIdx][year]   // e.g. 50
numLots = CEILING(quantity / partsPerLot)      // e.g. ceil(250 / 50) = 5
```

**New logic:**
```
numLots = numberOfSetups[partIdx][year]        // e.g. 5 (stored directly)
```

The number of lots is now stored explicitly in the sheet rather than derived from parts-per-lot.

### Unit Change: Setup Rates

- **Old:** `minutes / lot` - used directly in calculations
- **New:** `hours / order` - must be multiplied by 60 to convert to minutes

---

## Required Code Changes

### 0. Define a `PART_NUMBER_COL` constant

Add a single constant at the top of the `<script>` block (alongside the existing globals):

```js
const PART_NUMBER_COL = 'Associated Part Numbers';
```

Every place in the code that currently hardcodes `'Part Number'` (or will now reference `'Associated Part Numbers'`) uses `PART_NUMBER_COL` instead. If the column is ever renamed again, only this one line needs updating.

---

### 1. `requiredSheets` array in `loadData()`

Update the list of required sheet names:

```js
// OLD
['Quantities', 'Avg Parts per Lot', 'Machining Rates', 'Setup Rates', 'Vendor Time', 'Machine Allocation', 'Setup Allocation']

// NEW
['Quantities', 'Number of Setups', 'Machining Rates (mins per prt)', 'Setup Rates (hours per order)', 'Vendor Time', 'Machine Allocation', 'Setup Allocation']
```

### 2. Sheet loading assignments in `loadData()`

```js
// OLD
this.avgPartsPerLot = sheets['Avg Parts per Lot'].filter(r => r['Part Number']);
this.machiningRates = sheets['Machining Rates'].filter(r => r['Part Number']);
this.setupRates     = sheets['Setup Rates'].filter(r => r['Part Number']);
this.quantities     = sheets['Quantities'].filter(r => r['Part Number']);
this.vendorTime     = sheets['Vendor Time'].filter(r => r['Part Number']);

// NEW
this.numberOfSetups = sheets['Number of Setups'].filter(r => r[PART_NUMBER_COL]);
this.machiningRates = sheets['Machining Rates (mins per prt)'].filter(r => r[PART_NUMBER_COL]);
this.setupRates     = sheets['Setup Rates (hours per order)'].filter(r => r[PART_NUMBER_COL]);
this.quantities     = sheets['Quantities'].filter(r => r[PART_NUMBER_COL]);
this.vendorTime     = sheets['Vendor Time'].filter(r => r[PART_NUMBER_COL]);
```

Also rename the class property `this.avgPartsPerLot` to `this.numberOfSetups` in the constructor.

### 3. Year detection in `loadData()`

```js
// OLD
this.years = Object.keys(this.quantities[0]).filter(col => col !== 'Part Number');

// NEW
this.years = Object.keys(this.quantities[0]).filter(col => col !== PART_NUMBER_COL);
```

### 4. `createMappings()` - vendor time lookup

```js
// OLD
const partNum = row['Part Number'];

// NEW
const partNum = row[PART_NUMBER_COL];
```

### 5. `validateData()` - all `r['Part Number']` references

Four places in the `sheetsWithParts` object:

```js
// OLD
'Quantities':        new Set(this.quantities.map(r => r['Part Number']).filter(p => p)),
'Avg Parts per Lot': new Set(this.avgPartsPerLot.map(r => r['Part Number']).filter(p => p)),
'Machining Rates':   new Set(this.machiningRates.map(r => r['Part Number']).filter(p => p)),
'Setup Rates':       new Set(this.setupRates.map(r => r['Part Number']).filter(p => p)),
'Vendor Time':       new Set(this.vendorTime.map(r => r['Part Number']).filter(p => p))

// NEW
'Quantities':        new Set(this.quantities.map(r => r[PART_NUMBER_COL]).filter(p => p)),
'Number of Setups':  new Set(this.numberOfSetups.map(r => r[PART_NUMBER_COL]).filter(p => p)),
'Machining Rates':   new Set(this.machiningRates.map(r => r[PART_NUMBER_COL]).filter(p => p)),
'Setup Rates':       new Set(this.setupRates.map(r => r[PART_NUMBER_COL]).filter(p => p)),
'Vendor Time':       new Set(this.vendorTime.map(r => r[PART_NUMBER_COL]).filter(p => p))
```

### 6. `calculateYearData()` - core calculation logic

**Part number lookup:**
```js
// OLD
const partNumber = row['Part Number'];

// NEW
const partNumber = row[PART_NUMBER_COL];
```

**Number of lots - replace partsPerLot logic with direct lookup:**
```js
// OLD
const partsPerLot = this.avgPartsPerLot[idx]?.[year];
if (partsPerLot == null || partsPerLot === 0) { ... return; }
const numLots = Math.ceil(quantity / partsPerLot);

// NEW
const numLots = this.numberOfSetups[idx]?.[year];
if (numLots == null || numLots === 0) { ... return; }
// numLots is used directly, no Math.ceil() needed
```

**Setup rate unit conversion (hours -> minutes):**
```js
// OLD
const setupRate = this.setupRates[idx]?.[setupRateOp] || 0;
const totalSetupTime = numLots * setupRate / this.efficiency;

// NEW
const setupRateHours = this.setupRates[idx]?.[setupRateOp] || 0;
const setupRate = setupRateHours * 60;  // convert hours to minutes
const totalSetupTime = numLots * setupRate / this.efficiency;
```

### 7. Operations column detection in `validateData()` and `calculateYearData()`

```js
// OLD
Object.keys(this.machiningRates[0]).filter(col => col !== 'Part Number')

// NEW
Object.keys(this.machiningRates[0]).filter(col => col !== PART_NUMBER_COL)
```

Same for `setupRates`.

---

## What Does NOT Need to Change

- `Machine Allocation` sheet: same structure, no changes needed
- `Setup Allocation` sheet: new format shifts the "Operator" label to a value in an empty-header column (`__EMPTY`), which the existing filter already excludes - no code change needed
- All rendering functions (`renderMachineCards`, `renderOperatorTime`, etc.)
- Overflow/deliverability calculation logic
- Available capacity constant (272,160 min/year)
- CSS and layout

---

## Summary of Changes by Location

| Location | Change |
|---|---|
| Constructor | Rename `this.avgPartsPerLot` to `this.numberOfSetups` |
| `loadData()` - requiredSheets | Update 3 sheet names |
| `loadData()` - sheet assignments | Update 5 sheet references + column name |
| `loadData()` - year detection | `'Part Number'` -> `'Associated Part Numbers'` |
| `createMappings()` | `'Part Number'` -> `'Associated Part Numbers'` |
| `validateData()` - sheetsWithParts | Update 5 keys + column name |
| `validateData()` - operations | `'Part Number'` -> `'Associated Part Numbers'` (x2) |
| `calculateYearData()` - part lookup | `'Part Number'` -> `'Associated Part Numbers'` |
| `calculateYearData()` - numLots | Replace partsPerLot calculation with direct lookup |
| `calculateYearData()` - setup rate | Multiply by 60 to convert hours to minutes |
| `calculateYearData()` - operations | `'Part Number'` -> `'Associated Part Numbers'` |
