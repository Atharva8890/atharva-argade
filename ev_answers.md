# EV Exam — Complete 9-Mark Answers (All 40 Questions in Sequence)

---

# SECTION A: Motors, Batteries, BMS Basics

---

## Q1. Numerical — Motor Rating from Vehicle Data (GCW, Gradient, Range, Frontal Area, Cd, ρ)

**Given (Typical Data Set):**

- GCW (Gross Combined Weight) W = 1500 kg
- Road gradient α = 5° (sin α ≈ 0.0872)
- Velocity V = 60 km/h = 16.67 m/s
- Frontal area A = 2.0 m²
- Coefficient of drag Cd = 0.3
- Air density ρ = 1.225 kg/m³
- Coefficient of rolling resistance μ = 0.015
- Range = 100 km
- g = 9.81 m/s²

**Step 1 — Rolling Resistance Force (Fr):**

Fr = μ × W × g × cos α
Fr = 0.015 × 1500 × 9.81 × cos 5°
Fr = 0.015 × 1500 × 9.81 × 0.9962 = **219.9 N**

**Step 2 — Aerodynamic Drag Force (Fa):**

Fa = ½ × ρ × Cd × A × V²
Fa = 0.5 × 1.225 × 0.3 × 2.0 × (16.67)²
Fa = 0.5 × 1.225 × 0.3 × 2.0 × 277.9 = **102.1 N**

**Step 3 — Gradient Force (Fg):**

Fg = W × g × sin α = 1500 × 9.81 × 0.0872 = **1283.1 N**

**Step 4 — Total Tractive Force (Ft):**

Ft = Fr + Fa + Fg = 219.9 + 102.1 + 1283.1 = **1605.1 N**

**Step 5 — Motor Power Rating (P):**

P = Ft × V = 1605.1 × 16.67 = 26,757 W ≈ **26.76 kW**

Considering transmission efficiency η = 0.9:
**P_motor = 26.76 / 0.9 ≈ 29.7 kW**

**Step 6 — Battery Capacity for Given Range:**

Time t = 100/60 = 1.667 h
Energy E = P × t = 29.7 × 1.667 = **49.5 kWh**

**Result:** Motor rating ≈ **30 kW**, Battery ≈ **50 kWh**.

---

## Q2. Battery Performance Parameters

**Definition:** Battery performance parameters are quantitative measures that describe how effectively a battery stores, delivers, and retains electrical energy in an EV application.

**Key Parameters:**

1. **Cell/Battery Voltage (V):** Potential difference between terminals. Nominal voltage of Li-ion = 3.6–3.7 V/cell. EV packs typically 48 V, 96 V, 400 V.

2. **Capacity (Ah):** Total charge a battery can deliver at rated current. C = I × t. E.g., 100 Ah battery delivers 100 A for 1 hour.

3. **Energy Density:**
   - Gravimetric (Wh/kg) – energy per unit mass
   - Volumetric (Wh/L) – energy per unit volume
   - Li-ion: 150–250 Wh/kg.

4. **Power Density (W/kg):** Rate of energy delivery. Important for acceleration.

5. **C-Rate:** Charging/discharging rate relative to capacity. 1C = full discharge in 1 hour; 2C = 30 min.

6. **State of Charge (SOC %):** Available capacity as % of rated capacity. SOC = (Q_remaining / Q_rated) × 100.

7. **Depth of Discharge (DOD %):** DOD = 100 − SOC. Higher DOD reduces cycle life.

8. **State of Health (SOH %):** Ratio of current full-charge capacity to original capacity. Indicates ageing.

9. **Cycle Life:** Number of charge–discharge cycles before capacity falls below 80%. Li-ion ≈ 1000–2000 cycles.

10. **Internal Resistance (Ω):** Causes voltage drop and heat. Lower is better.

11. **Self-Discharge Rate:** Loss of charge during storage (Li-ion ≈ 2–5%/month).

12. **Efficiency:** η = Energy out / Energy in (Li-ion ≈ 90–95%).

**Estimation Example:**

For 48 V, 100 Ah Li-ion battery:

- Energy = 48 × 100 = 4800 Wh = 4.8 kWh
- If discharged at 50 A → C-rate = 0.5C
- If mass = 30 kg → Energy density = 4800/30 = 160 Wh/kg

These parameters jointly decide range, acceleration, life, and safety of EV.

---

## Q3. Battery Thermal Management System (BTMS)

**Definition:** BTMS is a system that maintains battery cells within optimal temperature range (15–35°C) to ensure safety, performance, and longevity.

**Need for BTMS:**

- Li-ion cells degrade above 45°C
- Below 0°C, lithium plating reduces capacity
- Uneven temperature → cell imbalance
- Thermal runaway risk above 80°C

**Major Functions:**

1. **Cooling System:**
   - **Air cooling (passive/active):** Simple, low cost, used in 2W & e-rickshaw
   - **Liquid cooling:** Coolant circulated through plates; used in Tesla, Tata Nexon
   - **Refrigerant cooling:** Direct expansion of AC refrigerant; high efficiency
   - **Phase Change Material (PCM):** Absorbs heat by melting; passive

2. **Heating System:** PTC heaters or coolant heaters warm cells in cold climate.

3. **Thermal Protection:**
   - Thermal fuses, fire-retardant separators
   - Pressure relief vents
   - Ceramic coatings to delay thermal runaway

4. **Control Unit:**
   - Temperature sensors (NTC thermistors) on each module
   - ECU receives data, controls pump/fan/valve
   - Maintains uniform temperature (ΔT < 5°C between cells)

5. **Safety Features:**
   - Over-temperature shutdown
   - Cell isolation
   - Fire suppression in advanced packs

6. **Maintenance Aspects:**
   - Coolant level inspection
   - Filter and pump check
   - Sensor calibration
   - Periodic flushing of coolant lines

**Block Diagram:** Battery pack → Sensors → BTMS Controller → Cooling/Heating loop → Heat exchanger → Radiator/Chiller.

**Conclusion:** BTMS is essential for safety, range, and life of EV batteries.

---

## Q4. Motors (Prime Mover): Classification, Construction, Working & Control

**Definition:** A motor (prime mover) in EV converts electrical energy from battery into mechanical energy to drive wheels.

**Classification:**

1. **DC Motors**
   - Brushed DC (Series, Shunt, Compound)
   - Brushless DC (BLDC)
   - Permanent Magnet DC (PMDC)

2. **AC Motors**
   - Induction Motor (3-phase, squirrel cage)
   - Permanent Magnet Synchronous Motor (PMSM)
   - Switched Reluctance Motor (SRM)
   - Synchronous Reluctance Motor

**Construction (General):**

- **Stator:** Stationary part with windings/permanent magnets
- **Rotor:** Rotating part (squirrel cage, wound, PM)
- **Shaft, bearings, end shields**
- **Cooling:** air/liquid jacket
- **Sensors:** Hall, encoder

**Working Principle:**

Based on Lorentz force F = BIL. Current-carrying conductor in magnetic field experiences force, producing torque.

- DC motor: Commutator reverses current
- BLDC: Electronic commutation via inverter
- Induction: Rotating magnetic field induces rotor current
- PMSM: Rotor synchronized with stator field
- SRM: Reluctance torque due to rotor alignment

**Control Methods:**

1. **Speed Control:**
   - DC: Armature voltage / field control
   - AC: V/f control, vector (FOC) control

2. **Torque Control:** Direct Torque Control (DTC), FOC

3. **Power Electronic Converters:**
   - DC chopper for DC motors
   - 3-phase inverter (VSI) with PWM for AC motors

4. **Regenerative Braking Control:** Motor acts as generator, returns energy to battery.

**Block Diagram:** Battery → Converter/Inverter → Motor → Transmission → Wheels. Controller takes input from throttle, brake, sensors.

**Conclusion:** PMSM and BLDC dominate modern EVs due to high efficiency and power density.

---

## Q5. Energy Storage System (ESS) Types & Packs Classification

**Definition:** ESS stores energy in chemical, electrical, mechanical, or thermal form and delivers it for EV propulsion.

**Types of ESS:**

1. **Electrochemical (Batteries):**
   - **Lead-Acid:** Cheap, heavy, used in e-rickshaw (35 Wh/kg)
   - **Nickel-Metal Hydride (NiMH):** Used in hybrid (Toyota Prius)
   - **Lithium-Ion:** High energy density (150–250 Wh/kg), modern EVs
   - **Sodium-ion, Solid-state:** Emerging

2. **Ultracapacitors (Supercapacitors):**
   - High power density, low energy density
   - Fast charge/discharge
   - Used for acceleration, regeneration buffer

3. **Fuel Cells:**
   - PEM fuel cell converts H₂ + O₂ → Electricity + H₂O
   - Used in FCEVs (Toyota Mirai)

4. **Flywheel ESS:** Kinetic energy storage; used in F1 KERS

5. **Hybrid ESS:** Battery + Ultracapacitor combination

**Battery Pack Classification:**

1. **Based on Chemistry:** Lead-acid, Li-ion (LFP, NMC, NCA, LCO, LMO)

2. **Based on Structure:**
   - **Cell:** Basic unit (3.7 V, 2–5 Ah)
   - **Module:** Group of cells in series/parallel
   - **Pack:** Group of modules + BMS + cooling + casing

3. **Based on Cell Format:**
   - Cylindrical (18650, 21700) – Tesla
   - Prismatic – BYD
   - Pouch – Hyundai Kona

4. **Based on Connection:**
   - Series (increase voltage)
   - Parallel (increase capacity)
   - Series–Parallel hybrid

5. **Based on Application:** Traction pack, auxiliary 12 V pack, fuel-cell auxiliary pack.

**Conclusion:** Li-ion packs with hybrid topology dominate modern EVs.

---

## Q6. Numerical — Battery Rating / Range Calculation (e-Rickshaw, Lead-acid vs Li-ion)

**Given:**

- e-Rickshaw average power consumption P = 1.5 kW
- Average speed V = 25 km/h
- Required range R = 80 km
- Lead-acid battery: 48 V, 100 Ah, DOD = 60%, η = 85%
- Li-ion battery: 48 V, 100 Ah, DOD = 90%, η = 95%

**Step 1 — Energy Required per Trip:**

Time t = R/V = 80/25 = 3.2 h
Energy E = P × t = 1.5 × 3.2 = **4.8 kWh**

**Step 2 — Lead-Acid Battery Capacity Required:**

Usable energy = Total × DOD × η
4.8 = (48 × Ah × 0.60 × 0.85)/1000
Ah = (4.8 × 1000)/(48 × 0.60 × 0.85)
**Ah_Lead = 196 Ah**

**Step 3 — Li-Ion Battery Capacity Required:**

4.8 = (48 × Ah × 0.90 × 0.95)/1000
Ah = (4.8 × 1000)/(48 × 0.90 × 0.95)
**Ah_Li = 117 Ah**

**Step 4 — Range Comparison (for same 100 Ah, 48 V):**

Lead-acid usable = 48 × 100 × 0.6 × 0.85 = 2.448 kWh
Range = 2.448 / 1.5 × 25 = **40.8 km**

Li-ion usable = 48 × 100 × 0.9 × 0.95 = 4.104 kWh
Range = 4.104 / 1.5 × 25 = **68.4 km**

**Conclusion:** For same Ah rating, Li-ion provides ~67% more range than lead-acid. Li-ion is preferred despite higher cost due to longer cycle life and lower weight.

---

## Q7. BLDC Motor — Construction, Working, Advantages & Disadvantages

**Definition:** BLDC (Brushless DC) motor is a synchronous motor with permanent magnets on rotor and electronic commutation instead of mechanical brushes.

**Construction:**

1. **Stator:**
   - Slotted laminated steel core
   - 3-phase windings (star/delta connected)
   - Trapezoidal back-EMF design

2. **Rotor:**
   - Permanent magnets (NdFeB / ferrite)
   - Surface-mounted (SPM) or Interior (IPM) construction
   - 2–8 pole pairs

3. **Hall Sensors:** 3 sensors at 120° to detect rotor position

4. **Electronic Controller:** 3-phase inverter (6 MOSFETs/IGBTs) with commutation logic

**Sketch description:** Stator with 3 windings (A, B, C); rotor inside with N-S magnets; Hall sensors mounted on stator; controller switches phases in 6-step sequence.

**Working:**

1. Hall sensors detect rotor position
2. Controller energizes appropriate stator coils
3. Magnetic field of stator attracts rotor magnets
4. Continuous switching (every 60°) maintains rotation
5. Commutation sequence: AB → AC → BC → BA → CA → CB

**Torque equation:** T = K_t × I, where K_t = torque constant.

**Advantages:**

- High efficiency (85–95%)
- High power-to-weight ratio
- Long life (no brushes to wear)
- Low maintenance
- High starting torque
- Smooth & silent operation
- Excellent speed–torque characteristics

**Disadvantages:**

- Higher cost (rare-earth magnets + electronics)
- Complex controller required
- Demagnetization risk at high temperature
- EMI/noise from switching

**Applications:** e-Scooters, e-Bikes, EV hub motors, drones, fans.

---

## Q8. Li-Ion Battery Construction, Working & Characteristic Curve

**Definition:** Li-ion battery is a rechargeable electrochemical cell in which lithium ions move between electrodes during charge and discharge.

**Construction:**

1. **Positive Electrode (Cathode):** Lithium metal oxide (LiCoO₂, LiFePO₄, NMC) coated on aluminium foil

2. **Negative Electrode (Anode):** Graphite coated on copper foil

3. **Electrolyte:** Lithium salt (LiPF₆) in organic solvent

4. **Separator:** Porous polypropylene/polyethylene membrane

5. **Casing:** Cylindrical (18650, 21700), prismatic, or pouch

6. **Terminals:** Positive and negative current collectors

**Working:**

*During Discharge:*

- Li⁺ ions move from anode → cathode through electrolyte
- Electrons flow from anode → cathode through external load
- Reaction at anode: LiC₆ → C₆ + Li⁺ + e⁻
- Reaction at cathode: CoO₂ + Li⁺ + e⁻ → LiCoO₂

*During Charge:* Reverse process — external voltage drives Li⁺ back to anode.

**Characteristic Curves:**

1. **Discharge Curve (V vs Capacity):**
   - Starts at 4.2 V (full charge)
   - Flat plateau at ~3.6–3.7 V (nominal)
   - Sharp drop near 3.0 V (cut-off)

2. **Power Efficiency Curve:**
   - High efficiency (>95%) at 0.2–0.5C
   - Drops at high C-rates due to I²R losses
   - Efficiency vs SOC remains stable in 20–80% range

3. **Cycle Life Curve:** Capacity vs cycles — gradual decline; 80% at ~1000–2000 cycles.

**Specifications:**

- Nominal voltage: 3.6–3.7 V/cell
- Energy density: 150–250 Wh/kg
- Cycle life: 1000–2000
- Efficiency: 90–95%

**Advantages:** High energy density, long life, low self-discharge, no memory effect.

**Disadvantages:** Costly, thermal runaway risk, ageing, requires BMS.

---

## Q9. Structural Configuration of Motor Layout (Short Note)

**Definition:** Motor layout refers to physical placement and arrangement of electric motor(s) in EV with respect to wheels and transmission.

**Types of Motor Layouts:**

1. **Single Central Motor with Differential:**
   - One motor drives both wheels through mechanical differential
   - Similar to ICE layout
   - Used in Tata Nexon EV, MG ZS

2. **Dual Motor (One per Axle):**
   - Front + Rear motor for AWD
   - Each drives one axle through differential
   - Used in Tesla Model S, Mahindra XUV400 (variant)

3. **In-Wheel/Hub Motor Layout:**
   - Motor integrated inside wheel hub
   - No mechanical drive shaft, no differential
   - Used in e-Scooters, e-Rickshaws, Lordstown

4. **Wheel-Side (Geared) Motor:**
   - Motor close to wheel with reduction gearbox
   - Compact, allows independent control

5. **Front-Wheel / Rear-Wheel / 4-Wheel Drive Configurations:**
   - FWD: Compact, used in city cars
   - RWD: Better traction, sportier
   - AWD: Best handling, costly

**Sketch:** Diagrams of FWD, RWD, AWD, and Hub-motor layouts.

**Selection Factors:**

- Vehicle type (2W/3W/4W)
- Traction & efficiency requirement
- Cost and packaging
- Maintenance accessibility

**Advantages of Hub Motor:** No transmission losses, regenerative braking on each wheel, torque vectoring.

**Disadvantages:** Increased unsprung mass affects ride comfort.

---

## Q10. Battery Control Unit (BCU), Units of Battery, Fuel Cell Energy Storage

**A) Battery Control Unit (BCU):**

**Definition:** BCU is an electronic control unit that monitors, regulates, and protects battery operation. It is a subsystem of BMS.

**Functions:**

- Voltage/current/temperature monitoring
- SOC and SOH estimation
- Cell balancing (active/passive)
- Charge/discharge control
- Communication with VCU via CAN bus
- Fault diagnosis & protection

**Types of BCU:**

1. **Centralized:** One master BCU for entire pack — simple but heavy wiring
2. **Modular:** One BCU per module + master controller — flexible
3. **Distributed:** BCU on each cell + master — most accurate, costly
4. **Master–Slave:** Slave units monitor; master computes & communicates

**B) Units of Battery:**

- **Cell:** Smallest unit (3.7 V, 2–5 Ah Li-ion)
- **Module:** Group of cells (series–parallel), e.g., 12 V, 50 Ah
- **Pack:** Multiple modules + BMS + cooling + casing (e.g., 48 V, 400 V EV pack)

**C) Fuel Cell Energy Storage:**

**Definition:** Electrochemical device converting chemical energy of fuel (H₂) directly into electricity.

**Construction:**

- Anode, Cathode, Electrolyte (PEM), Bipolar plates, Catalyst (Pt)

**Working:**

- H₂ → 2H⁺ + 2e⁻ at anode
- Electrons flow externally (electricity)
- H⁺ passes through electrolyte
- ½O₂ + 2H⁺ + 2e⁻ → H₂O at cathode

**Types:** PEMFC, SOFC, AFC, PAFC, MCFC, DMFC

**Advantages:** Zero emission, high efficiency (60%), quick refuelling

**Disadvantages:** Costly Pt catalyst, H₂ storage difficulty, infrastructure

---

# SECTION B: Drive-train, Differential, Vehicle Dynamics

---

## Q1. Mechanical Differential vs Electric Differential

| Sr. No. | Parameter | Mechanical Differential | Electric Differential |
|---|---|---|---|
| 1 | Definition | Mechanical gear system distributing torque between two wheels | Electronic control system independently regulating speed/torque of two motors |
| 2 | Construction | Bevel gears, sun gear, planetary gears, casing | Two separate motors + electronic controller + sensors |
| 3 | Working principle | Equal torque, different speeds on a turn | Independent motor speed control via VCU |
| 4 | Components | Mechanical (gears, shafts, bearings) | Electronic (motors, inverter, ECU, sensors) |
| 5 | Weight | Heavy (15–25 kg) | Lighter (no gearbox) |
| 6 | Efficiency | 90–93% | 95–98% |
| 7 | Losses | Friction, gear meshing | Only electrical (I²R) |
| 8 | Maintenance | High (lubrication, wear) | Low (electronic) |
| 9 | Response time | Slow (mechanical lag) | Very fast (ms) |
| 10 | Torque vectoring | Not possible (limited slip only) | Easily possible per wheel |
| 11 | Traction control | Requires extra device | Inbuilt |
| 12 | Regenerative braking | Not supported per wheel | Independent on each wheel |
| 13 | Cost | Low | High |
| 14 | Packaging | Bulky, central | Compact, distributed |
| 15 | Applications | ICE cars, Tata Nexon EV | Tesla, Mahindra XUV400, Hub-motor EVs |
| 16 | Noise | Mechanical noise | Silent |
| 17 | Failure mode | Gear damage, oil leak | Electronic fault |

**Conclusion:** Electric differential gives precise torque vectoring, regenerative braking and better handling — making it ideal for modern EVs, while mechanical differential remains common in low-cost EVs.

---

## Q2. Brake System in EV and Its Types

**Definition:** Brake system in EV converts kinetic energy of moving vehicle into another form (heat or electricity) to decelerate the vehicle safely.

**Types:**

**1. Mechanical (Friction) Braking:**

- Conventional disc/drum brakes
- Hydraulic actuation
- Components: Master cylinder, brake pads, callipers, rotor
- Kinetic energy dissipated as heat
- Always present as fail-safe

**Diagram:** Wheel + Disc + Calliper + Pad assembly with hydraulic line.

**2. Regenerative Braking:**

- Motor acts as generator during deceleration
- Kinetic energy → Electrical energy → Battery
- Inverter rectifies AC and charges battery
- Energy recovery up to 70%
- Controlled by VCU based on brake-pedal input

**Diagram:** Wheel → Motor/Generator → Inverter → Battery (with arrows showing energy flow during braking).

*Equation:* P_regen = T × ω; Energy recovered = ½ m (V₁² − V₂²) × η

**3. Hybrid (Blended) Braking:**

- Combines regenerative + mechanical
- ECU decides ratio based on speed, SOC, brake force
- At low speed and high deceleration → mechanical dominates
- At cruising → regenerative dominates
- Used in most modern EVs (Tata, Tesla, Hyundai)

**4. Electromagnetic / Eddy Current Brake:**

- Magnetic field induces eddy currents in disc
- Used in buses, trains as auxiliary

**5. Anti-lock Braking (ABS):**

- Sensors detect wheel lock
- ECU modulates brake pressure
- Maintains steering control

**Advantages of EV Brake System:**

- Energy recovery (range +10–20%)
- Reduced brake-pad wear
- Smooth, controlled deceleration
- Lower maintenance

**Disadvantages:**

- Regen ineffective at very low speed
- Battery SOC must allow charging
- Complex control

**Conclusion:** Hybrid braking with ABS is the standard in modern EVs.

---

## Q3. Driving Resistances — Rolling, Aerodynamic, Grading, Acceleration (with Equations)

**Total Driving Resistance (F_total)** is the sum of all forces opposing vehicle motion, requiring tractive force to overcome.

**1. Rolling Resistance (F_r):**

Caused by tyre deformation at contact patch.

F_r = μ_r × W × cos α = μ_r × m × g × cos α

- μ_r = coefficient of rolling resistance (0.01–0.02)
- Depends on tyre pressure, road, speed
- Power loss: P_r = F_r × V

**2. Aerodynamic Drag (F_a):**

Caused by air pressure on frontal area.

F_a = ½ × ρ × C_d × A × V²

- ρ = air density (1.225 kg/m³)
- Cd = drag coefficient (0.25–0.35)
- A = frontal area (m²)
- V = relative velocity (m/s)
- Increases with square of speed

**3. Aerodynamic Lift (F_L):**

F_L = ½ × ρ × C_L × A × V²

- CL = lift coefficient
- Reduces tyre grip at high speed

**4. Gradient (Grading) Resistance (F_g):**

Component of weight along the slope.

F_g = W × sin α = m × g × sin α

- α = road inclination
- Positive (uphill) opposes motion; negative (downhill) aids

**5. Road / Surface Resistance:** Caused by rough road; usually combined with rolling resistance.

**6. Acceleration Resistance (F_acc):**

Inertia force during acceleration.

F_acc = m × a × (1 + δ)

- δ = rotating mass factor (0.05–0.15) for wheels, motor, gearbox

**Total Tractive Force:**

F_t = F_r + F_a + F_g + F_acc

**Tractive Power:**

P = F_t × V

**Free-body diagram:** Vehicle on inclined road with arrows F_r, F_a, F_g, F_acc and W = mg.

**Conclusion:** All these resistances must be overcome by motor through wheels. F_a dominates at high speed, F_g at gradients, F_acc during acceleration.

---

## Q4. Electric Drive-Train Topologies (2W/3W/4W)

**Definition:** Electric drive-train is the chain of components — battery, controller, motor, transmission — that delivers power from energy source to wheels.

**Major Topologies:**

**A) Two-Wheeler (2W) Drive-train:**

1. Hub motor in rear wheel (most common in e-scooters)
2. Mid-drive motor with chain/belt to rear wheel
3. Direct gear-drive in e-bicycles

*Components:* Battery (48–72 V), Controller, BLDC/PMSM motor, Throttle, Display

**Diagram:** Battery → Controller → Hub motor in rear wheel.

**B) Three-Wheeler (3W) Drive-train:**

1. Single motor with mechanical differential to rear wheels (e-rickshaw)
2. Dual hub motors on rear wheels (electric differential)

*Components:* Battery (48 V Pb/Li), Controller, BLDC motor, Differential, Rear axle, Mechanical brake

**C) Four-Wheeler (4W) Drive-train:**

1. **Single Motor + Mechanical Differential** (FWD/RWD): Tata Nexon EV
2. **Two Motors (Front + Rear)** AWD: Tesla Model S
3. **Four Hub Motors** — one per wheel: Rivian, prototypes
4. **Series Hybrid** (HEV): ICE → generator → battery → motor
5. **Parallel Hybrid:** ICE + Motor both drive wheels
6. **Series–Parallel Hybrid:** Both modes possible (Toyota Prius)

**Comparison Table:**

| Type | Motor count | Differential | Complexity | Example |
|---|---|---|---|---|
| 2W | 1 (hub) | None | Low | Ola S1 |
| 3W | 1 or 2 | Mechanical/Electric | Medium | Mahindra Treo |
| 4W single | 1 | Mechanical | Medium | Tata Nexon |
| 4W AWD | 2 | Electric | High | Tesla |
| 4W Hub | 4 | Electric | Very high | Concept |

**Conclusion:** Drive-train topology is selected based on vehicle type, performance, cost and packaging.

---

## Q5. Power Flow Control in Electric Drive-Train Topologies

**Definition:** Power flow control refers to managing direction and magnitude of energy flow between battery, motor, and wheels under different operating modes.

**Operating Modes:**

**1. Acceleration / Traction Mode:**

- Battery → Inverter → Motor → Wheels
- Battery discharges
- Motor consumes power

**2. Cruising Mode:**

- Steady power flow, low draw
- Auxiliary systems also fed

**3. Regenerative Braking Mode:**

- Wheels → Motor (as generator) → Rectifier → Battery
- Energy recovered (up to 70%)
- Battery charges

**4. Coasting Mode:**

- No power flow between battery and motor
- Vehicle moves on inertia

**5. Standstill Charging Mode:**

- External grid → On-board charger → Battery
- Bidirectional with V2G capability

**Diagram (block):**

Battery ⇄ Bidirectional DC-DC ⇄ Inverter ⇄ Motor ⇄ Wheels
Arrows showing forward (traction) and reverse (regen).

**Power Flow in Different Topologies:**

**A) Series Hybrid:**

ICE → Generator → Rectifier → Battery → Inverter → Motor → Wheels
(Power flows only via electric path; ICE never directly drives wheels)

**B) Parallel Hybrid:**

ICE + Motor → Common shaft → Wheels
Battery ↔ Motor; ICE → mechanical → wheels

**C) Series–Parallel Hybrid (Toyota Prius):**

ICE → Power Split Device → Wheels (mechanical) and Generator → Battery → Motor → Wheels

**D) Pure EV (BEV):**

Battery ⇄ Inverter ⇄ Motor ⇄ Wheels
Single bidirectional path

**Control Strategies:**

- Rule-based control
- Optimization-based (DP, ECMS)
- Fuzzy logic / AI-based
- Maximize efficiency, minimize battery wear

**Conclusion:** Effective power flow control improves range, efficiency, and battery life.

---

## Q6. Power Train Components & Sizing Calculation

**Definition:** Power train includes all components that generate and deliver power to wheels.

**Components:**

1. **Battery Pack:** Energy source (e.g., 48 V – 400 V)
2. **Battery Management System (BMS):** Monitors, balances, protects
3. **Power Converter / Inverter:** Converts DC to 3-phase AC
4. **Electric Motor:** Converts electrical to mechanical
5. **Transmission/Gearbox:** Single-speed reduction (8:1 to 10:1)
6. **Differential:** Splits torque between wheels
7. **Drive Shaft & Axles:** Transfer torque
8. **Wheels & Tyres:** Contact with road
9. **Vehicle Control Unit (VCU):** Coordinates all subsystems

**Sizing Calculation Example:**

*Given:* m = 1200 kg, V_max = 100 km/h = 27.78 m/s, α = 5°, A = 2 m², Cd = 0.3, μ_r = 0.015, range = 150 km

**Step 1 — Forces at max speed:**

- F_r = 0.015 × 1200 × 9.81 × cos 5° = 175.9 N
- F_a = 0.5 × 1.225 × 0.3 × 2 × 27.78² = 283.6 N
- F_g = 1200 × 9.81 × sin 5° = 1026 N
- Total = 1485 N

**Step 2 — Motor Power:**

P = F × V / η = 1485 × 27.78 / 0.9 = 45.8 kW
**Motor rating ≈ 50 kW**

**Step 3 — Torque at wheel:**

Wheel radius r = 0.3 m
T_wheel = F × r = 1485 × 0.3 = 445.5 N·m
With gear ratio 8:1: T_motor = 55.7 N·m

**Step 4 — Battery Capacity:**

At cruise (60 km/h), P ≈ 15 kW
Time = 150/60 = 2.5 h
E = 15 × 2.5 / 0.9 = **41.7 kWh**
**Battery rating ≈ 45 kWh, ~400 V, 110 Ah**

**Step 5 — Inverter Rating:** ≥1.2 × motor power = 60 kVA

**Conclusion:** Proper sizing balances cost, weight, and performance.

---

## Q7. Numerical — Aerodynamic Drag Force, Power & Distance (Calm vs Windy)

**Given:** m = 1200 kg, A = 2.2 m², Cd = 0.3, ρ = 1.225 kg/m³, vehicle speed V_v = 60 km/h = 16.67 m/s, head wind V_w = 20 km/h = 5.56 m/s, energy available E = 5 kWh

**Case 1 — Calm Air (V_w = 0):**

Relative velocity V_rel = V_v = 16.67 m/s

F_d = ½ × ρ × Cd × A × V_rel²
F_d = 0.5 × 1.225 × 0.3 × 2.2 × (16.67)²
F_d = 0.5 × 1.225 × 0.3 × 2.2 × 277.9
**F_d = 112.4 N**

Power required P = F_d × V_v = 112.4 × 16.67 = **1873 W ≈ 1.87 kW**

Time t = E/P = 5000/1873 = 2.67 h
Distance d = V × t = 60 × 2.67 = **160.2 km**

**Case 2 — Windy (head wind 20 km/h):**

V_rel = V_v + V_w = 16.67 + 5.56 = 22.23 m/s

F_d = 0.5 × 1.225 × 0.3 × 2.2 × (22.23)²
F_d = 0.5 × 1.225 × 0.3 × 2.2 × 494.2
**F_d = 199.8 N**

Power required (against vehicle motion) P = F_d × V_v = 199.8 × 16.67 = **3331 W ≈ 3.33 kW**

Time t = 5000/3331 = 1.5 h
Distance d = 60 × 1.5 = **90.1 km**

**Comparison Table:**

| Parameter | Calm | Windy |
|---|---|---|
| V_rel | 16.67 m/s | 22.23 m/s |
| Drag force | 112.4 N | 199.8 N |
| Power | 1.87 kW | 3.33 kW |
| Distance | 160.2 km | 90.1 km |

**Observation:** Head wind nearly doubles drag and reduces range by ~44%.

**Conclusion:** Aerodynamic drag depends on square of relative wind velocity; head wind drastically reduces EV range.

---

## Q8. Fuel Efficiency Analysis & Significant Features for EV

**Definition:** Fuel efficiency of EV is the measure of useful work (distance) obtained per unit energy consumed, expressed as km/kWh or Wh/km, instead of km/L.

**Equivalent Metrics:**

- **MPGe (Miles Per Gallon equivalent):** 33.7 kWh = 1 gallon gasoline
- **kWh/100 km:** European metric
- **Wh/km:** Indian metric (commonly 100–150 Wh/km for cars)

**Factors Affecting EV Fuel Efficiency:**

1. **Vehicle Mass:** Heavier vehicle needs more energy
2. **Aerodynamic Drag:** Cd × A — lower is better
3. **Rolling Resistance:** Tyre pressure, road
4. **Driving Style:** Aggressive acceleration reduces efficiency
5. **Speed:** Optimum at 40–60 km/h
6. **Auxiliary Loads:** AC, lights, heater
7. **Battery State:** Temperature, age, SOC
8. **Motor & Drive-train Efficiency:** Higher η = better mileage
9. **Regenerative Braking:** Recovers 10–20% energy
10. **Ambient Temperature:** Cold reduces battery efficiency

**Significant Features of EV Fuel Efficiency:**

1. **Energy Recovery:** Regenerative braking returns kinetic energy
2. **Higher Tank-to-Wheel Efficiency:** 70–85% vs 20–30% for ICE
3. **Zero Idle Consumption:** No energy during stops
4. **Variable Speed Efficiency:** Wide flat efficiency curve
5. **Low Maintenance Energy Use:** No oil, fewer parts
6. **Direct Torque:** No gear losses (single-speed)
7. **Lower Per-km Cost:** ₹1–1.5/km vs ₹6–8/km (petrol)
8. **No Emissions:** TTW (Tank-to-Wheel) efficiency clean
9. **Eco-driving Modes:** Software-controlled efficiency

**Analysis Approach:**

- Drive cycle testing (MIDC, WLTP, ARAI)
- Real-world energy logging
- Range estimation models

**Efficiency Calculation:**

Range R (km) = Battery Capacity (kWh) × η / Specific Consumption (kWh/km)

Example: 30 kWh × 0.9 / 0.15 = 180 km

**Conclusion:** EV fuel efficiency depends on design + driving conditions; well-designed EVs achieve 5–7 km/kWh.

---

## Q9. Dynamic Equation of Vehicle Movement / Roll, Pitch, Yaw

**A) Dynamic Equation:**

A moving vehicle is subjected to several forces. Newton's second law gives:

F_t − F_r − F_a − F_g = m × a × (1 + δ)

Where:

- F_t = Tractive force (motor output)
- F_r = Rolling resistance = μ·m·g·cosα
- F_a = Aerodynamic drag = ½ρ·Cd·A·V²
- F_g = Gradient force = m·g·sinα
- m·a = Inertia force (acceleration)
- δ = Rotational inertia factor (0.05–0.15)

Rearranged:

a = (F_t − F_r − F_a − F_g) / (m × (1 + δ))

Power balance:

P_t = (F_r + F_a + F_g) × V + m × a × V × (1 + δ)

**B) Effects of Rolling, Pitch & Yaw (6 DOF Motion):**

A road vehicle has 6 degrees of freedom — 3 translational + 3 rotational.

**Translational:** Longitudinal (X), Lateral (Y), Vertical (Z)

**Rotational:**

**1. Roll (about X-axis, longitudinal):**

- Side-to-side tilting (when cornering)
- Caused by lateral acceleration during turn
- Anti-roll bars and stiff suspension reduce it
- Excessive roll → rollover risk

**2. Pitch (about Y-axis, lateral):**

- Front-back tilting (nose dives during braking, lifts during acceleration)
- Caused by longitudinal acceleration/deceleration
- Suspension damping controls it
- Affects passenger comfort

**3. Yaw (about Z-axis, vertical):**

- Rotation around vertical axis (steering response)
- Caused by steering input or asymmetric forces
- Excessive yaw → spin / loss of control
- Controlled by ESP, yaw rate sensor

**Diagrams:** Vehicle with three perpendicular axes; arrows showing roll (around longitudinal), pitch (around lateral), yaw (around vertical).

**Importance for EVs:**

- Low CG of battery pack reduces roll
- Independent torque vectoring controls yaw
- Active suspension manages pitch during regen braking
- Stability programs use these inputs

**Conclusion:** Understanding 6-DOF dynamics is vital for ride comfort, handling, and safety design.

---

## Q10. Basic Concept of Electric Traction with Examples

**Definition:** Electric traction is the use of electric power for driving vehicles. It involves generation, conversion, and utilization of electrical energy in vehicles such as trains, trams, buses, and EVs.

**Need for Electric Traction:**

- Zero local emissions
- Higher efficiency than ICE
- Lower running cost
- Quick starting torque
- Regenerative braking possible
- Reduced fossil-fuel dependence

**Systems of Electric Traction:**

1. **Self-contained (Battery):** Power source onboard — BEVs, e-rickshaws
2. **Externally fed:** Power received from overhead lines or third rail — trams, metros, electric trains
3. **Hybrid:** ICE + battery + motor — HEVs

**Methods of Electric Traction:**

1. **DC System:** 600–3000 V DC — Mumbai suburban, metros
2. **Single-Phase AC:** 25 kV AC, 50 Hz — Indian Railways
3. **Three-Phase AC:** Limited use (older Swiss railways)
4. **Composite System:** Mix of above

**Components of Electric Traction System:**

- Source (battery / overhead line)
- Pantograph / current collector
- Transformer & rectifier
- Power converter / inverter
- Traction motor (DC series, induction, PMSM)
- Control gear (chopper, VFD)
- Wheels & coupling

**Speed–Time Curve of Traction:**

Phases — Acceleration → Free running → Coasting → Braking (similar in EV)

**Advantages:**

- High starting torque
- Regenerative braking
- Cleanliness, less maintenance
- Operates on diverse terrain

**Disadvantages:**

- High initial cost
- Power supply infrastructure needed
- Limited range (battery)

**Examples:**

1. **Indian Railways (WAG-12 locomotive):** 25 kV AC, 9000 kW
2. **Delhi Metro:** 25 kV AC overhead
3. **Tata Nexon EV:** 30.2 kWh battery, PMSM motor
4. **BEST electric bus (Mumbai):** 250 kWh battery
5. **e-Rickshaw:** 48 V, 100 Ah Pb-acid, BLDC motor

**Conclusion:** Electric traction is the future of transport due to efficiency, sustainability, and performance benefits.

---

# SECTION C: Vehicle Body, Suspension, Testing

---

## Q1. Retrofitting — Meaning & Problems in Two-Wheeler Retrofitting

**Definition:** Retrofitting refers to conversion of an existing IC-engine vehicle into an electric vehicle by replacing the engine and fuel system with electric motor, battery, controller, and accessories.

**Need for Retrofitting:**

- Avoids buying new vehicle (lower cost)
- Reduces emissions in existing fleet
- Faster transition to electric mobility
- Lower upfront capital
- Promotes circular economy

**Components Replaced in Two-Wheeler Retrofitting:**

- Petrol engine → Electric motor (BLDC hub motor or mid-drive)
- Fuel tank → Battery pack (Li-ion / Lead-acid)
- Carburettor / EFI → Controller / Inverter
- Throttle cable → Electronic throttle
- Addition of BMS, charger, DC-DC converter
- Display, kill switch, reverse switch

**Retrofitting Procedure:**

1. Vehicle inspection & feasibility study
2. Engine and fuel system removal
3. Motor mounting on swingarm/hub
4. Battery placement (under seat / footboard)
5. Wiring of controller, BMS, throttle
6. Testing — performance, range, safety
7. Certification & registration (ARAI / ICAT)

**Problems Associated with Two-Wheeler Retrofitting:**

1. **Space Constraint:** Limited room to mount large battery; restricts range.

2. **Weight Distribution:** Battery weight (15–25 kg) alters centre of gravity, affecting handling and braking.

3. **Frame Strength:** Original frame designed for ICE; may not safely support battery+motor loads.

4. **Mounting Challenges:** No standard fixtures for motor and battery on existing 2W chassis.

5. **Range Limitation:** Small battery (~1.5–2 kWh) gives 40–60 km only.

6. **Performance Mismatch:** Original gearing, brakes, suspension not optimised for instant torque of electric motor.

7. **Safety & Thermal Issues:** Battery heating, short-circuit, IP-rating concerns.

8. **Cost vs Benefit:** Retrofit kits ₹30,000–₹50,000; new e-scooter often offers better value.

9. **Regulatory Compliance:** Must obtain CMVR approval from ARAI/ICAT — costly and time-consuming.

10. **Standardization:** No universal kit; varies model-to-model.

11. **Warranty & Insurance:** Original warranty void; insurance premiums may rise.

12. **Reliability:** Component compatibility issues affect long-term performance.

13. **Charging Infrastructure:** Customer needs home charging arrangement.

14. **Service Network:** Limited skilled mechanics for retrofitted EVs.

**Government Initiatives:**

- ARAI/ICAT certification for approved kits
- State subsidies in Delhi, Maharashtra for retrofitting
- FAME-II support for approved retrofitters

**Conclusion:** Retrofitting is a sustainable bridge to EV transition but requires careful engineering, certification, and component selection.

---

## Q2. National / International Testing, Regulation, Licensing & Approval Organizations

**Definition:** EV testing and approval is governed by various national and international bodies that frame standards, certify vehicles, and ensure safety, performance, and emission norms.

**National (Indian) Organizations:**

1. **ARAI (Automotive Research Association of India), Pune:**
   - Nodal agency for vehicle certification
   - Conducts homologation tests
   - Type approval, CMVR compliance
   - Drafts AIS standards

2. **ICAT (International Centre for Automotive Technology), Manesar:**
   - Type approval & R&D
   - Powertrain, emission, safety testing
   - Works under NATRiP

3. **CIRT (Central Institute of Road Transport), Pune:** Bus & commercial vehicle testing.

4. **VRDE (Vehicles Research & Development Establishment), Ahmednagar:** Defence vehicle testing under DRDO.

5. **NATRAX (National Automotive Test Tracks), Indore:** High-speed and durability testing.

6. **GARC (Global Automotive Research Centre), Chennai:** EV battery testing.

7. **BIS (Bureau of Indian Standards):** Develops IS standards for batteries, chargers, components.

8. **CMVR (Central Motor Vehicles Rules):** Legal framework for vehicle approval in India.

9. **MoRTH (Ministry of Road Transport & Highways):** Policy maker; issues notifications.

10. **FAME-II / NEMMP / PLI:** Incentive and policy programs for EVs.

**International Organizations:**

1. **UNECE (United Nations Economic Commission for Europe):**
   - WP.29 regulations (R100, R136 for EVs)
   - Battery, charging, crash standards

2. **ISO (International Organization for Standardization):**
   - ISO 6469 (EV safety)
   - ISO 15118 (V2G communication)
   - ISO 17409 (charging)

3. **IEC (International Electrotechnical Commission):**
   - IEC 61851 (EV conductive charging)
   - IEC 62196 (connectors)
   - IEC 62660 (Li-ion testing)

4. **SAE (Society of Automotive Engineers, USA):** SAE J1772, J3068, J2954 (wireless charging).

5. **EPA (Environmental Protection Agency, USA):** Emission certification.

6. **NHTSA (National Highway Traffic Safety Administration, USA):** Crash standards FMVSS.

7. **Euro NCAP:** Crash safety star ratings.

8. **JARI (Japan Automobile Research Institute):** Japan certification.

9. **GB Standards (China):** GB/T 18488 (motor), GB/T 31484 (battery).

10. **CHAdeMO / CCS / GB/T / Type 2:** Global charging protocols.

**Licensing Authorities (India):**

- **State RTO:** Vehicle registration, driving licence
- **Central Vehicle Certification:** Through ARAI/ICAT

**Conclusion:** A coordinated effort of national (ARAI, ICAT, BIS) and international (ISO, IEC, SAE, UNECE) bodies ensures EV safety, interoperability, and quality globally.

---

## Q3. Body Loads Based on EV Configurations

**Definition:** Body loads are the various static and dynamic forces acting on the EV body structure that must be considered during design.

**Types of Body Loads:**

**1. Static Loads:**

- **Vehicle weight (kerb weight + payload)**
- **Battery pack weight** (200–500 kg for cars)
- **Powertrain weight** (motor, gearbox, inverter)
- **Passenger and luggage weight**

**2. Dynamic Loads:**

- **Acceleration / deceleration force**
- **Braking force**
- **Cornering force** (lateral)
- **Bump/pothole impact (vertical)**
- **Suspension transferred loads**

**3. Aerodynamic Loads:**

- Drag force on front
- Lift force on roof
- Side wind (yaw) force

**4. Crash Loads:**

- Frontal impact (56 kph, full-frontal)
- Side impact, rear impact
- Roof crush, pole impact
- Battery intrusion protection

**5. Vibration Loads:**

- Road-induced vibrations
- Motor harmonics
- Battery pack mounting stresses

**6. Thermal Loads:** Battery and motor heat causing structural expansion.

**Variations by EV Configuration:**

**A) Two-Wheeler:**

- Mainly point loads at front fork, rear swingarm, battery mount
- Bending of frame tube
- Lower aerodynamic but high vibration sensitivity

**Diagram:** Skeleton of 2W with arrows showing load points.

**B) Three-Wheeler (e-Rickshaw):**

- Battery under seat (concentrated load)
- Passenger load on rear deck
- Chassis bears bending and torsion
- Cornering load distribution unequal

**C) Four-Wheeler (Car):**

- Battery floor pack distributes weight evenly
- Lower CG improves stability
- Front + rear crash zones
- Loads on subframes for motor and suspension

**D) Bus / Truck:**

- Heavy battery on roof or chassis rail
- Higher torsion and bending
- Multi-point suspension distribution

**Load Path Analysis:**

- Loads flow from wheels → suspension → subframe → body frame
- Battery integrated in floor (skateboard chassis) increases structural rigidity

**Methods of Analysis:**

- **FEA (Finite Element Analysis):** Static, modal, crash simulations
- **Multi-body Dynamics (MBD)**
- **Topology Optimization** for lightweighting

**Design Requirements:**

- High strength-to-weight ratio
- Crash energy absorption
- Battery protection zone
- NVH control

**Conclusion:** EV body must be designed for all combined static, dynamic, crash, and thermal loads while protecting the battery pack.

---

## Q4. Front / Rear Suspension Systems Design for EV Configurations

**Definition:** Suspension is a system of springs, dampers, and linkages that connects the vehicle body to wheels, isolating road shocks and ensuring stability.

**Functions:**

- Support vehicle weight
- Absorb road shocks
- Maintain tyre–road contact
- Provide stable handling
- Comfort to passengers
- Protect battery from vibration (critical for EV)

**Types of Front Suspension:**

**1. MacPherson Strut:**

- Single strut combining spring + damper
- Compact, low cost
- Used in most small EV cars (Tata Tiago EV, Nexon EV)
- *Sketch:* Wheel hub connected to lower wishbone and strut on top

**2. Double Wishbone:**

- Upper and lower control arms
- Better handling, used in sports EVs
- More complex and costly

**3. Telescopic Fork (2W):**

- Two telescopic tubes with coil + oil damper
- Used in e-bikes, e-scooters

**4. Trailing Link / Leading Link (3W):**

- Used in e-rickshaw front wheel

**Types of Rear Suspension:**

**1. Multi-Link Suspension:**

- Multiple control arms
- Premium EVs (Tesla, MG ZS EV)
- Excellent ride and handling

**2. Twist Beam Axle:**

- Simple H-beam, semi-independent
- Compact, frees space for battery
- Used in entry-level EVs

**3. Trailing Arm + Coil Spring (3W):**

- Used in e-rickshaw

**4. Swingarm with Mono-shock (2W):**

- Single shock absorber
- Common in modern e-scooters (Ola, Ather)

**5. Independent Trailing Arm:** For premium 4W EVs.

**6. Air Suspension:**

- Air-filled bladders, electronically controlled
- Used in luxury EVs (Mercedes EQS, BMW i7)
- Adjustable ride height

**EV-Specific Design Considerations:**

1. **Battery Protection:** Suspension geometry must protect underfloor battery from road shocks.
2. **Weight Distribution:** Account for heavy floor-mounted battery.
3. **Lower Centre of Gravity:** Helps reduce roll & pitch.
4. **Unsprung Mass:** Hub motors increase unsprung mass — needs stiffer damping.
5. **Regenerative Braking:** Suspension must handle additional torque reactions.
6. **NVH Control:** Bushings, mounts to isolate motor vibrations.

**Diagram (Sketch):** Cross-sections of MacPherson (front), multi-link (rear) with labels: coil spring, damper, control arm, knuckle, anti-roll bar.

**Comparison Table:**

| Type | Cost | Comfort | Handling | EV usage |
|---|---|---|---|---|
| MacPherson | Low | Avg | Avg | Small EV cars |
| Double wishbone | High | Good | Best | Sports EV |
| Multi-link | High | Best | Best | Premium EV |
| Twist beam | Low | Avg | Avg | Hatchback EV |
| Air | Very high | Excellent | Adjustable | Luxury EV |

**Conclusion:** Suspension design in EVs balances comfort, handling, weight, and battery safety.

---

## Q5. Homologation of Vehicles — Meaning & Procedure

**Definition:** Homologation is the official approval process by which a vehicle is certified to meet the technical and safety standards of a country before it can be sold or registered.

**Need for Homologation:**

- Ensures regulatory compliance
- Guarantees road safety
- Confirms emission norms
- Avoids substandard imports
- Mandatory under CMVR for India

**Authorities in India:**

- **ARAI, Pune**
- **ICAT, Manesar**
- **CIRT, VRDE, GARC**

**Types of Homologation:**

1. **Type Approval:** Single prototype tested, applies to all units (mass production)
2. **CoP (Conformity of Production):** Continuous audit to ensure each unit matches approved type
3. **NOC for Imported Vehicles:** Individual approval

**Tests Performed during Homologation:**

**A) Safety Tests:**

- Frontal & side crash test
- Brake test (AIS 015, AIS 074)
- Steering effort
- Lighting & visibility
- Horn & wipers

**B) Performance Tests:**

- Acceleration & top speed
- Gradeability
- Range (for EVs)
- Maximum payload

**C) Emission Tests:** (For ICE/Hybrid; EVs exempt but tested for noise)

**D) EV-Specific Tests:**

- Battery safety (AIS 048, AIS 156)
- Motor performance (AIS 041)
- Charger standards (AIS 138)
- Electrical insulation
- Thermal management
- EMI/EMC compatibility (AIS 004)

**E) Component Tests:**

- Tyres, lights, mirrors
- Seat belts, airbags
- Anti-theft devices

**Homologation Procedure (Step-by-Step):**

1. **Application Submission:** Manufacturer applies to ARAI/ICAT with technical specifications
2. **Document Review:** Drawings, BOM, test plan, COP plan
3. **Sample Submission:** Vehicle/component samples for tests
4. **Test Execution:** Performance, safety, EV-specific tests
5. **Component Approval:** Individual parts certified
6. **Whole Vehicle Type Approval (WVTA):** Complete vehicle approved
7. **Issue of Certificate:** ARAI/ICAT issues type approval certificate
8. **CoP Audit:** Periodic audits to verify mass-production consistency
9. **Re-certification:** On design change, renewal needed

**Documents Required:**

- Vehicle technical specifications
- Manufacturer details
- Drawings
- Test reports of subsystems
- Quality control documents
- Production process flow

**Examples of Standards Applied:**

- AIS 038 Rev. 2 (EV safety)
- AIS 048 (Traction battery)
- AIS 049 (Motor & controller)
- AIS 156 (Battery safety after thermal events)

**Importance:**

- Legal road usage permission
- Builds customer trust
- Enables export approvals
- Government subsidies (FAME-II eligibility)

**Conclusion:** Homologation is essential to ensure EVs meet safety, performance, and environmental standards before they reach the market.

---

## Q6. Types of EV Frame Configurations / Chassis-Frame Building Problems

**Definition:** Frame (chassis) is the structural backbone of the vehicle supporting body, powertrain, battery, suspension, and load.

**Types of EV Frame Configurations:**

**1. Ladder Frame:**

- Two longitudinal rails + cross members
- Strong, used for SUVs, trucks
- Heavy, low fuel economy
- Example: Mahindra eVerito (modified ladder)

**2. Monocoque (Unibody):**

- Body and frame integrated
- Light, rigid, safer
- Used in most modern EV cars (Tata Nexon, MG ZS EV)

**3. Skateboard Chassis (EV-Specific):**

- Flat platform with battery embedded in floor
- Motor on axles
- Used by Tesla, GM Ultium, Hyundai E-GMP
- Maximizes interior space, lowers CG

**4. Spaceframe / Tubular Frame:**

- Steel/aluminium tube structure
- Sports EVs, Rivian, prototypes

**5. Backbone Frame:**

- Single central tube; used in some 3W

**6. Subframe (Cradle):**

- Auxiliary frame for motor/suspension mounting

**7. Sandwich Floor Frame (BEV-specific):**

- Battery pack acts as load-bearing structural floor (CTC - Cell to Chassis)
- Example: BYD Blade, Tesla 4680

**Diagram:** Sketches of ladder, monocoque, and skateboard chassis with labels.

**Chassis Frame Building Problems for EVs:**

1. **Battery Integration:**
   - Heavy and bulky battery pack
   - Requires structural reinforcement under floor
   - Crash protection essential

2. **Weight Distribution:**
   - Battery adds 300–500 kg
   - CG shifts; affects handling
   - Increases load on suspension mounts

3. **Crashworthiness:**
   - Battery cells must not rupture in crash
   - Side, frontal, pole impact protection
   - Designing crumple zones around battery

4. **Material Selection:**
   - High-strength steel, aluminium, composites
   - Balance between strength and weight
   - Cost vs benefit

5. **Manufacturing Complexity:**
   - Joining dissimilar metals
   - Welding aluminium, bonding composites
   - New tooling and processes

6. **Thermal Management Integration:**
   - Cooling channels routed within chassis
   - Avoid hotspots near battery

7. **NVH (Noise, Vibration, Harshness):**
   - No engine noise — other noises become noticeable
   - Vibration isolation of motor

8. **Modularity:**
   - Frame must accommodate different battery sizes, motor configs
   - Same platform for SUV/sedan/hatchback

9. **Cost:**
   - High-strength materials and tooling expensive
   - Skateboard chassis costly to develop

10. **Repairability & Recyclability:**
    - Composite frames difficult to repair
    - Battery-integrated chassis hard to dismantle

11. **Regulatory Compliance:**
    - AIS standards for crash, EMI, fire safety
    - Type approval challenges

**Conclusion:** EV chassis design must overcome challenges of weight, crash safety, battery integration, and cost; skateboard chassis with monocoque structure has emerged as the optimal solution.

---

## Q7. Driving Dynamics & Comfort + Anatomy & Terminology of Car Package

**A) Driving Dynamics:**

**Definition:** Driving dynamics refers to the response and behaviour of a vehicle to driver inputs (acceleration, braking, steering) and external disturbances (road, wind).

**Three Aspects:**

1. **Longitudinal Dynamics:**
   - Acceleration, braking, gradient
   - Governs traction, drive-train sizing
   - Equation: F_t − F_resist = m·a

2. **Lateral Dynamics:**
   - Cornering, steering response
   - Yaw rate, side slip angle
   - Centripetal force = m·v²/r

3. **Vertical Dynamics:**
   - Pitch, roll, bounce due to road
   - Handled by suspension, damping

**B) Comfort:**

**Definition:** Comfort is the perception of ease, smoothness, and absence of stress during driving.

**Comfort Parameters:**

1. **Ride Comfort:** Suspension absorbs vibrations (frequency 1–8 Hz)
2. **NVH:** Cabin quietness (motor whine, road noise)
3. **Climate Control:** AC, heater, ventilation
4. **Ergonomics:** Seat position, controls reach, visibility
5. **Acoustics:** Sound insulation
6. **Seat Comfort:** Cushion, lumbar support
7. **Cabin Space:** Headroom, legroom
8. **Lighting & Display:** Touchscreens, ambient lights

**Factors Affecting Comfort:** Tyre pressure, suspension tuning, body stiffness, NVH treatment.

**C) Anatomy of Car Package:**

**Definition:** Car package is the arrangement of all components, occupants, and luggage within the vehicle volume.

**Major Anatomy Areas:**

1. **Engine/Motor Compartment**
2. **Passenger Compartment (Cabin)**
3. **Luggage Compartment (Boot)**
4. **Underbody (battery, exhaust in ICE)**
5. **Front & Rear Crumple Zones**

**D) Key Terminology of Car Package:**

1. **Wheelbase (L):** Distance between front and rear axle
2. **Track Width:** Distance between left and right wheels
3. **Overall Length / Width / Height**
4. **Front Overhang / Rear Overhang**
5. **Ground Clearance:** Distance from ground to underbody
6. **Approach / Departure Angle:** For off-road capability
7. **Hip Point (H-Point):** Theoretical pivot of seated occupant's hip
8. **SgRP (Seating Reference Point):** Hip point for design reference
9. **R-Point:** Same as H-point but for design dummy
10. **Eye Ellipse:** Eye position envelope of driver
11. **A, B, C Pillars:** Roof-supporting pillars
12. **Cowl Point:** Bottom of windshield
13. **Belt Line:** Lower edge of window
14. **Crash Zones:** Front, rear absorption areas
15. **Step-In Height:** Floor-to-ground distance at door
16. **Couple Distance:** Between front and rear hip points
17. **Cargo Volume:** Boot capacity (litres)
18. **Daylight Opening (DLO):** Window area

**E) Importance in EV:**

- Battery pack changes packaging
- Skateboard layout creates more cabin space
- Lower H-point possible due to flat floor
- Frunk (front trunk) available

**Diagram:** Side view of car with labels — wheelbase, overhang, H-point, eye ellipse, pillars.

**Conclusion:** Successful EV design integrates driving dynamics, comfort, and proper packaging to deliver a refined and safe driving experience.

---

## Q8. Indian AIS Standards for e-Vehicles / Crash Testing & Test Tracks

**A) Indian AIS Standards (Automotive Industry Standards):**

**Definition:** AIS standards are technical and safety norms framed by ARAI in consultation with MoRTH for road vehicles in India.

**Major AIS Standards for EVs:**

1. **AIS 038 Rev. 2 (2020):** Electric Power Train Vehicles — Construction & functional safety

2. **AIS 039:** Measurement of energy consumption and range for BEVs

3. **AIS 040:** Maximum speed measurement for EVs

4. **AIS 041:** Power measurement of electric motor

5. **AIS 048:** Traction battery safety (replaced by AIS 156)

6. **AIS 049:** EV Electrical safety (insulation, isolation, protection against electric shock)

7. **AIS 102 Part 1 & 2:** Battery operated vehicles (L-category like 2W, 3W)

8. **AIS 123:** Hybrid Electric Vehicles

9. **AIS 138 Part 1 & 2:** EV Conductive AC/DC charging systems

10. **AIS 156:** Specific requirements for batteries — thermal propagation, fire safety, post-incident behaviour (updated after EV fire incidents in 2022)

11. **AIS 004 (Part 3):** EMC testing for EVs

12. **AIS 167:** Standards for swappable batteries

13. **AIS 099:** CMVR Type Approval for L-category EVs

**B) Crash Testing:**

**Definition:** Crash testing is the controlled collision of a vehicle to assess its safety, structural integrity, and occupant protection.

**Types of Crash Tests:**

1. **Frontal Impact (Full-Frontal at 48–56 km/h)**
2. **Offset Frontal (40% offset at 64 km/h)**
3. **Side Impact / Pole Impact**
4. **Rear Impact**
5. **Roof Crush Test**
6. **Pedestrian Protection Test**

**EV-Specific Crash Tests:**

1. **Battery Pack Integrity:** Post-crash leakage, fire, voltage
2. **Cell Short Circuit Test**
3. **Thermal Propagation Test (AIS 156)**
4. **Electrical Isolation Test:** No high voltage exposure after crash
5. **Vibration & Shock Test**
6. **Drop Test:** Battery pack from 1 m height

**Parameters Measured:**

- Head Injury Criterion (HIC)
- Chest Acceleration
- Neck Forces
- Battery temperature, voltage post-crash
- Vehicle deformation

**Indian Crash Test Programs:**

- **Bharat NCAP (B-NCAP) — launched 2023:** Star rating like Euro NCAP

**C) Crash Testing of Tracks:**

**Definition:** Specialized facilities to conduct crash and durability tests.

**Major Indian Test Tracks:**

1. **NATRAX, Indore:**
   - Asia's largest high-speed track
   - 11.3 km perimeter, 16 km total
   - Crash labs, banked curves, gradeability tracks

2. **ARAI, Pune:** Crash lab with sled facility, full-vehicle pendulum

3. **ICAT, Manesar:** Crash and safety labs

4. **GARC, Chennai (Indu Nagar):** EV battery test track

5. **NATRiP Track at Pithampur, MP:** General testing

6. **Test Track Features:**
   - High-speed oval
   - Wet/dry handling courses
   - Brake & ABS testing surfaces
   - Gradient slopes (5%, 10%, 20%)
   - Cross-country track for SUVs
   - EV charging zones

**International Tracks:** Nürburgring, Millbrook (UK), Idiada (Spain), JATCO Japan.

**Conclusion:** Indian AIS standards, crash testing protocols, and modern test tracks together ensure EV safety, quality, and global competitiveness.

---

## Q9. Aesthetics & Ergonomics for EV Configurations

**A) Aesthetics:**

**Definition:** Aesthetics refers to the visual appeal and styling of the vehicle — proportions, surface treatment, colours, graphics, and overall character.

**Aesthetic Elements:**

1. **Proportions:** Length-to-width ratio, overhangs, wheelbase
2. **Surfaces:** Smooth, sculpted, character lines
3. **Front Fascia:** Closed grille (EV-specific identity), LED DRLs
4. **Headlamps & Taillamps:** Signature lighting, OLED
5. **Wheel Design:** Aero-optimised alloys
6. **Colour & Finish:** Two-tone, matte, gradient
7. **Body Style:** Sedan, SUV, coupe, hatchback
8. **Graphics & Badging:** EV badges, blue accents
9. **Glasshouse & DLO:** Large windows
10. **Roofline:** Coupé style, panoramic sunroof
11. **Aerodynamic Features:** Spoilers, diffusers, air curtains

**EV-Specific Aesthetic Trends:**

- Closed grille (no engine cooling needed)
- Flush door handles
- Aerodynamic underbody
- Futuristic interior with large touchscreens
- Minimalist dashboard
- Ambient lighting
- Floating roof, two-tone

**B) Ergonomics:**

**Definition:** Ergonomics is the science of designing vehicle interiors and controls for comfort, safety, efficiency, and ease of use.

**Ergonomic Considerations:**

1. **Driver Posture:**
   - H-Point and SgRP placement
   - Seat angle (95–105°)
   - Steering wheel reach
   - Pedal position

2. **Visibility:**
   - Eye ellipse for SAE-95 percentile
   - A-pillar obstruction angle (<6°)
   - Mirror placement
   - Heads-up display (HUD)

3. **Reach & Operability:**
   - Distance to gearshift, infotainment
   - Touchscreen height (avoid neck strain)
   - Voice control

4. **Seat Comfort:**
   - Lumbar support
   - Adjustable cushion, headrest
   - Ventilated/heated seats

5. **Cabin Climate:** AC vents, defroster, automatic climate

6. **Noise & Vibration:** Quiet cabin (EVs benefit from no engine noise)

7. **Display & Controls:**
   - Cluster readability
   - Steering-mounted controls
   - Capacitive vs physical buttons

8. **Storage & Stowage:** Cup holders, door pockets, glove box

9. **Ingress/Egress:** Step height, door angle (especially in SUVs and EV skateboard floors)

10. **Safety Ergonomics:** Seatbelt placement, airbag clearance

**EV-Specific Ergonomic Advantages:**

- Flat floor (skateboard) → more legroom
- No transmission tunnel
- Quieter cabin
- Frunk for extra storage
- Larger touchscreen due to simpler dashboard

**Variations by EV Configuration:**

- **2W:** Saddle ergonomics, handlebar reach
- **3W (e-Rickshaw):** Passenger seat layout, boarding height
- **4W Hatchback:** Compact cabin, optimised package
- **4W SUV:** High seating, large boot
- **Bus:** Multiple ergonomic zones for driver & passengers

**Standards:** SAE J826 (H-point manikin), AIS 119 (driver controls).

**Conclusion:** Aesthetic and ergonomic design together create user delight, brand identity, and safe operation — essential for EV adoption.

---

## Q10. EV Design & Packaging — Hip Point / Seating Reference Point

**Definition:** Hip Point (H-Point) or Seating Reference Point (SgRP) is the theoretical pivot point of an occupant's torso and thigh when seated, used as a key reference in automotive design.

**Significance:**

- Anchor point for entire interior layout
- Determines seat, steering, pedal positions
- Influences visibility, headroom, legroom
- Basis for SAE manikin (J826)

**Definitions:**

1. **H-Point:** Located at the hip joint of seated occupant (measured with H-point machine)
2. **SgRP (Seating Reference Point):** Designated H-point of design dummy at fully rear seat position
3. **R-Point:** Same as SgRP, used in regulatory drawings
4. **A-Point:** Above SgRP, accommodation reference

**Measurement:**

Using SAE J826 H-Point manikin — a mechanical 50th percentile male dummy placed on the seat. The pivot at hip joint becomes the H-Point.

**Standards:**

- SAE J826: H-point machine
- AIS 119: Driver's field of view
- ISO 6549: Three-dimensional H-point reference

**Key Design Reference Points (Diagram):**

1. **H-Point (Hip Point):** Pivot of torso–thigh
2. **A-Point:** Accelerator pedal heel reference
3. **PRP (Pedal Reference Point):** Pedal heel
4. **BOFRP (Ball of Foot Reference Point):** Ball of foot on pedal
5. **Eye Ellipse:** Position of driver's eyes (envelope)
6. **Head Contour:** Headroom envelope

**Sketch Description:** Side view of seated occupant showing:

- H-point at hip
- BOFRP at pedal
- Eye ellipse above
- A-pillar to right
- Roof headroom above

**Design Parameters Derived from H-Point:**

1. **Seat Cushion Length & Angle**
2. **Backrest Angle (Torso Angle, typically 22–25°)**
3. **Hip-to-Heel Distance**
4. **Hip-to-Steering Wheel Distance**
5. **Hip-to-Roof Headroom**
6. **Hip-to-Eye Position**
7. **Couple Distance (front to rear H-point)**

**Effect of H-Point on EV Packaging:**

1. **Battery Pack Placement:**
   - Floor-mounted battery raises floor
   - H-point raised to maintain hip-to-heel angle
   - Cabin height may increase

2. **Skateboard Platform:**
   - Higher floor = higher H-point
   - Compromise between battery thickness and cabin height

3. **Visibility & Comfort:**
   - Higher H-point can improve visibility (SUV-like)
   - But reduces sportiness

4. **Underseat Clearance:** Battery, wiring, cooling routing

5. **Ergonomic Trade-offs:**
   - Lower H-point = sporty but tight cabin
   - Higher H-point = comfortable, easier ingress

**H-Point Examples:**

- Sports car: 250 mm from ground
- Sedan: 350–450 mm
- SUV: 600–700 mm
- EV with skateboard battery: typically raised by 50–80 mm vs ICE

**Importance in Design:**

- Drives entire package
- Determines occupant comfort
- Impacts vehicle proportions
- Crucial for crash protection geometry

**Conclusion:** H-point / SgRP is the foundation of vehicle interior design; in EVs, battery integration influences its placement and demands careful packaging.

---

# SECTION D: Charging Systems, BMS, Standards

---

## Q1. Typical Structure of Battery Management System (BMS) — Necessity & Functions

**Definition:** BMS is an electronic system that supervises a rechargeable battery (cell or pack) by monitoring its state, calculating data, balancing cells, protecting it, and communicating with vehicle systems.

**Necessity of BMS:**

1. **Safety:** Prevents over-charge, over-discharge, short circuit, thermal runaway
2. **Performance:** Ensures optimum operating range, balanced cells
3. **Longevity:** Increases battery life by avoiding stress
4. **Accurate Estimation:** Provides reliable SOC, SOH information
5. **Regulatory Compliance:** AIS 156 mandates BMS in Indian EVs
6. **Cost Saving:** Prevents premature replacement
7. **Integration:** Communicates with VCU, charger, telematics

**Structure of BMS:**

A BMS typically consists of these subsystems:

**1. Sensing Unit:**

- Voltage sensors (per cell)
- Current sensor (Hall-effect, shunt)
- Temperature sensors (NTC thermistors)

**2. Microcontroller / DSP Unit:**

- Acquires sensor data
- Runs SOC, SOH algorithms
- Decision-making logic

**3. Cell Balancing Circuit:**

- Passive (resistive bleed)
- Active (capacitive/inductive energy transfer)

**4. Protection Circuit:**

- Over/under voltage cut-off
- Over-current protection (fuse, MOSFET)
- Over-temperature shutdown
- Short-circuit protection

**5. Communication Module:**

- CAN bus (most common)
- LIN, RS-485, Bluetooth
- Communicates with VCU, charger, infotainment

**6. Power Management:**

- DC-DC converter for BMS supply
- Wake/sleep modes

**7. Memory & Data Logging:**

- EEPROM/Flash for event logs
- Diagnostics codes (DTC)

**Architecture Types:**

1. **Centralized BMS:** One unit for entire pack — simple, low cost
2. **Modular BMS:** Per-module controllers + master — flexible
3. **Distributed BMS:** Per-cell mini-BMS + master — most accurate
4. **Master–Slave BMS:** Master + multiple slave units

**Block Diagram of BMS:**

Cells → Sensors → Analog Front End (AFE) → Microcontroller → Communication (CAN) → VCU
Branches: Balancing circuit, Protection circuit, Cooling control

**Significant Functions of BMS:**

1. **Voltage Monitoring:** Each cell continuously
2. **Current Monitoring:** Charge/discharge current
3. **Temperature Monitoring:** Cell, module, pack
4. **SOC Estimation:** Coulomb counting, OCV, Kalman filter
5. **SOH Estimation:** Capacity fade, internal resistance
6. **Cell Balancing:** Maintain equal voltage among cells
7. **Protection:** OV, UV, OC, OT, SC
8. **Thermal Management Control:** Coolant pump/fan signals
9. **Communication:** CAN bus to VCU, charger
10. **Data Logging & Diagnostics:** Stores fault history
11. **Pre-charge & Contactor Control:** Soft-start, isolation
12. **Insulation Monitoring:** High-voltage safety
13. **Charge Control:** CC-CV charging
14. **Calibration & Updates:** OTA firmware

**Functions Summary Table:**

| Function | Purpose |
|---|---|
| Monitoring | Real-time data |
| Balancing | Cell equalization |
| Protection | Safety against fault |
| Estimation | SOC, SOH |
| Communication | System integration |
| Control | Charge/discharge regulation |

**Conclusion:** BMS is the brain of EV battery pack — without it, safe and efficient battery operation is impossible.

---

## Q2. Charger Architectures (On-board, Off-board, AC, DC)

**Definition:** Charger architecture describes the design, location, and power conversion path of equipment that transfers electrical energy from grid to EV battery.

**Classification of Chargers:**

**A) Based on Location:**

1. **On-Board Charger (OBC):**
   - Mounted inside vehicle
   - Receives AC from grid
   - Converts AC to DC for battery
   - Typically 3.3 kW (Level 1), 7.4 kW (Level 2), up to 22 kW
   - Components: EMI filter, PFC stage, DC-DC converter, controller
   - Slow but flexible (plug into any AC socket)

   **Block Diagram:** Grid (AC) → EMI filter → PFC rectifier → DC-DC isolation → Battery

2. **Off-Board Charger:**
   - External charging station
   - Converts AC to high-voltage DC outside vehicle
   - Directly feeds DC into battery via fast-charge port
   - Used for fast/ultra-fast charging (50–350 kW)
   - Example: DC fast chargers at highways (CCS2, CHAdeMO)

   **Block Diagram:** Grid → Step-down transformer → Rectifier → DC-DC → DC connector → Battery

**B) Based on Current Type:**

1. **AC Chargers:**
   - Use grid AC; vehicle's OBC converts to DC
   - Slower (3–22 kW)
   - Examples: Type 1 (J1772), Type 2 (Mennekes), Bharat AC-001
   - Suitable for home, office, mall

2. **DC Chargers:**
   - Direct DC supply bypassing OBC
   - Fast (50–350 kW)
   - Examples: CCS2, CHAdeMO, GB/T, Bharat DC-001
   - Highway, public stations

**C) Based on Power Flow:**

1. **Unidirectional Charger:** Grid → Battery only
2. **Bidirectional Charger:** Battery ↔ Grid (V2G, V2H, V2L)

**D) Based on Charging Stages (Levels):**

Covered in next question (Q3).

**Components of Charger Architecture:**

1. **EMI Filter:** Suppress switching noise
2. **Power Factor Correction (PFC) Stage:** Boost converter / totem-pole
3. **AC-DC Rectifier:** Bridge rectifier
4. **DC-DC Isolation Stage:** LLC, phase-shift converter, dual active bridge
5. **High-Frequency Transformer:** Isolation
6. **Output Filter:** Smooth DC
7. **Microcontroller:** PWM control, communication
8. **Communication Module:** CAN, PLC for ISO 15118
9. **Connectors & Cables**

**Charger Topologies:**

- Single-stage AC-DC
- Two-stage AC-DC + DC-DC
- Three-phase totem-pole PFC (modern OBC)
- Resonant LLC (high efficiency)

**Comparison:**

| Feature | On-Board (AC) | Off-Board (DC) |
|---|---|---|
| Location | Inside vehicle | External station |
| Power | 3–22 kW | 50–350 kW |
| Charging time | 4–8 hrs | 15–60 min |
| Cost | Low | High |
| Complexity | Moderate | High |
| Battery management | Vehicle BMS | Communication with BMS |
| Use case | Home/office | Highway, public |

**Modern Trends:**

- SiC/GaN-based bidirectional chargers
- V2G enabled OBC
- 800 V architecture for ultra-fast charging
- Wireless charging (SAE J2954)

**Conclusion:** AC on-board chargers serve daily slow charging while DC off-board fast chargers enable long-distance EV mobility.

---

## Q3. Level 1, Level 2 and Level 3 Chargers

**Definition:** EV chargers are categorized into levels based on input voltage, current, and charging speed.

**A) Level 1 Charger (Slow AC Charging):**

- **Voltage:** 120 V AC (USA) / 230 V AC (India, Europe)
- **Current:** 12–16 A (single phase)
- **Power:** 1.4 – 1.9 kW (US); 2.3–3.3 kW (India)
- **Connector:** Standard household plug (Type 1 / IEC 60309 in some regions)
- **Charging time:** 8–20 hours for full EV charge
- **Location:** Home, plug-and-play

**Advantages:**

- Cheapest, no infrastructure
- Convenient for overnight charging
- Easy retrofit anywhere

**Disadvantages:**

- Very slow
- Strains household wiring
- Limited to small EVs and 2W/3W

**Example:** e-Scooter charging at home from 5 A socket.

**B) Level 2 Charger (Medium AC Charging):**

- **Voltage:** 208–240 V AC (single phase) or 380 V (three phase)
- **Current:** 16–80 A
- **Power:** 3.3 – 22 kW
- **Connector:** Type 1 (J1772), Type 2 (Mennekes), Bharat AC-001 (15 A x 3)
- **Charging time:** 3–8 hours
- **Location:** Home wall-box, workplace, public AC points, malls

**Advantages:**

- Faster than Level 1
- Affordable infrastructure
- Wide compatibility

**Disadvantages:**

- Requires dedicated wiring (32 A circuit)
- Costlier installation

**Example:** Tata Nexon EV home wall-box (7.2 kW).

**C) Level 3 Charger (Fast DC Charging):**

- **Voltage:** 400 – 1000 V DC
- **Current:** 100–500 A
- **Power:** 50 – 350 kW (and beyond)
- **Connector:** CCS1, CCS2, CHAdeMO, GB/T, Tesla Supercharger, Bharat DC-001
- **Charging time:** 15–60 minutes (10–80% SOC)
- **Location:** Highway, public fast-charging stations

**Advantages:**

- Very fast charging
- Suitable for long trips
- Compatible with most modern EVs

**Disadvantages:**

- Expensive to install (₹15–30 lakh per unit)
- High demand on grid
- Battery stress due to high current

**Example:** Tata Power 50 kW DC charger on highways; Tesla Supercharger V3 (250 kW).

**Sub-Categories of Level 3:**

1. **DC Fast Charging (DCFC):** 50–150 kW
2. **Ultra-Fast Charging:** 150–350 kW
3. **High-Power Charging (HPC):** ≥ 350 kW for trucks, buses

**Comparison Table:**

| Parameter | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Type | AC | AC | DC |
| Voltage | 120/230 V | 240/400 V | 400–1000 V |
| Current | 12–16 A | 16–80 A | 100–500 A |
| Power | 1.4–3.3 kW | 3.3–22 kW | 50–350 kW |
| Time (full charge) | 8–20 h | 3–8 h | 15–60 min |
| Connector | Household plug | Type 1/2 | CCS/CHAdeMO/GB-T |
| Location | Home | Home/Public | Highway/Public |
| Cost | Low | Medium | High |
| Conversion | Inside vehicle | Inside vehicle | Inside charger |

**Indian Bharat EV Charging Standards:**

- **Bharat AC-001:** 3 x 15 A (Level 2 AC)
- **Bharat DC-001:** 15/30/50/100 kW DC fast charging

**Conclusion:** Level 1 for overnight home charging, Level 2 for daily routine, Level 3 for fast highway use — together forming a complete charging ecosystem.

---

## Q4. Requirements for Charging System

**Definition:** Charging system requirements are the technical, electrical, safety, and user-experience criteria that an EV charging infrastructure must satisfy.

**Major Requirements:**

**A) Electrical Requirements:**

1. **Input Voltage Compatibility:** Must work with grid voltages (230 V AC single-phase, 415 V AC three-phase, 11 kV/22 kV HT for fast chargers)

2. **Output Voltage Range:** 200–1000 V DC for batteries; matches different EV configurations

3. **Power Rating:** Wide range from 1.4 kW (Level 1) to 350 kW (Level 3)

4. **Power Factor:** ≥ 0.95 lagging at full load (with PFC stage)

5. **Total Harmonic Distortion (THD):** < 5% at input

6. **Efficiency:** ≥ 94% for AC, ≥ 96% for DC fast chargers

7. **Galvanic Isolation:** Between grid and vehicle for safety

8. **Bidirectional Capability:** V2G, V2H, V2L (future-ready)

**B) Safety Requirements:**

1. **Earth Leakage Protection (RCCB / GFCI):** 30 mA personal safety
2. **Over-current Protection (MCB / fuse)**
3. **Over-voltage & Under-voltage cut-off**
4. **Surge Protection (SPD)**
5. **Temperature Sensing & Auto Shutdown**
6. **Insulation Monitoring (DC chargers)**
7. **Emergency Stop Button**
8. **Cable Lock / Anti-theft**
9. **Fire-resistant Enclosure (IP54/IP65)**
10. **Lightning Protection**

**C) Communication Requirements:**

1. **EV ↔ Charger Communication:**
   - CAN bus
   - PLC (Power Line Communication) per ISO 15118
   - Pilot signal (PWM)

2. **Charger ↔ CMS (Charge Management System):**
   - OCPP 1.6 / 2.0.1 (Open Charge Point Protocol)
   - 4G/5G/Ethernet/Wi-Fi

3. **User Interface:** Touchscreen, RFID, mobile app

**D) Functional Requirements:**

1. **Multiple Charging Modes:** Slow / Fast / Ultra-fast
2. **Plug & Play Operation**
3. **Multiple Connector Support:** CCS2 + CHAdeMO + Type 2
4. **Authentication:** RFID, OTP, QR, mobile app
5. **Payment Gateway:** UPI, card, wallet
6. **Smart Scheduling:** Off-peak charging, grid-friendly
7. **Remote Monitoring:** Status, fault, energy used
8. **OTA Updates:** Firmware

**E) Environmental Requirements:**

1. **Operating Temperature:** –10 °C to +55 °C
2. **Humidity:** Up to 95 %
3. **IP Rating:** IP54 minimum for outdoor
4. **Vibration & Shock Tolerance**
5. **Corrosion Resistance:** Coastal areas

**F) Mechanical Requirements:**

1. **Robust enclosure (steel / aluminium)**
2. **Cable management arm**
3. **Vandal-proof design**
4. **Easy maintenance access**
5. **Compact footprint**

**G) Regulatory & Standards Requirements:**

1. **AIS 138 (India)**
2. **IEC 61851** (Conductive charging)
3. **IEC 62196** (Connectors)
4. **ISO 15118** (V2G communication)
5. **CE / BIS certification**

**H) Economic Requirements:**

1. **Cost-effective installation**
2. **Low operating cost**
3. **High utilization rate**
4. **Compatibility with renewable energy (solar + storage)**

**Conclusion:** A well-designed EV charging system must simultaneously meet electrical, safety, communication, functional, environmental, and regulatory requirements to ensure reliable and user-friendly operation.

---

## Q5. Grid Voltages, Frequencies & Wiring; Real Power, Apparent Power, Power Factor

**A) Grid Voltages & Frequencies:**

**Definition:** Grid voltage and frequency are the standardised parameters at which AC electricity is supplied by utilities to consumers.

**1. Indian Grid:**

- Single-phase: 230 V, 50 Hz, 2-wire (Phase + Neutral)
- Three-phase: 415 V (Line-Line), 50 Hz, 4-wire (3 Phase + Neutral)
- HT supply: 11 kV, 22 kV, 33 kV (industrial / fast chargers)

**2. Global Voltages & Frequencies:**

| Region | Voltage | Frequency |
|---|---|---|
| India | 230 V / 415 V | 50 Hz |
| USA | 120 V / 240 V | 60 Hz |
| Europe | 230 V / 400 V | 50 Hz |
| Japan | 100 V / 200 V | 50/60 Hz |
| China | 220 V / 380 V | 50 Hz |

**3. Voltage Tolerance:** ±6% per IS standards.

**B) Grid Wiring:**

1. **Single-Phase Wiring:**
   - Phase + Neutral + Earth
   - Used for residential, light commercial
   - Up to 7.4 kW EV chargers

2. **Three-Phase Wiring:**
   - 3 Phases (R, Y, B) + Neutral + Earth
   - Star or Delta configuration
   - Used for fast chargers, industrial

3. **Wiring Components:**
   - Cables (Cu/Al), MCB, RCCB, fuses
   - Distribution board
   - Metering panel
   - Earthing system

4. **Wiring Standards:**
   - IS 732 (Electrical wiring)
   - IS 3043 (Earthing)
   - National Electrical Code (NEC)

**C) Power Concepts in AC Circuits:**

In AC system, three types of power exist:

**1. Real Power (P):**

- Actual useful power dissipated in load
- Unit: Watts (W) or kW
- Formula: P = V × I × cos φ (single-phase)
- P = √3 × VL × IL × cos φ (three-phase)
- Measured by energy meter (kWh)

**2. Reactive Power (Q):**

- Power stored/returned by inductive or capacitive elements
- Unit: VAR (Volt-Ampere Reactive)
- Formula: Q = V × I × sin φ
- Doesn't do useful work but loads the grid

**3. Apparent Power (S):**

- Total power drawn from source
- Unit: VA (Volt-Ampere) or kVA
- Formula: S = V × I (single-phase)
- S = √3 × VL × IL (three-phase)
- Vector sum: S = √(P² + Q²)

**Power Triangle:**

```
       S
      /|
     / | Q
    /  |
   /φ__|
       P
```

- P = horizontal (real)
- Q = vertical (reactive)
- S = hypotenuse (apparent)

**4. Power Factor (PF or cos φ):**

- Ratio of real to apparent power
- PF = P / S = cos φ
- Ranges from 0 to 1
- Lagging (inductive), Leading (capacitive)
- Unity (resistive)

**Significance:**

- Higher PF = better utilization
- Low PF = more current for same power → losses
- Utilities penalize PF < 0.9
- Power factor correction by capacitors / PFC stage in chargers

**D) Numerical Example:**

Given: Three-phase EV charger, V = 415 V, I = 32 A, PF = 0.95

- Apparent Power S = √3 × 415 × 32 = 22,997 VA ≈ 23 kVA
- Real Power P = S × PF = 23 × 0.95 = 21.85 kW
- Reactive Power Q = √(S² − P²) = √(23² − 21.85²) = √(529 − 477.4) = √51.6 ≈ 7.18 kVAR

**E) Importance in EV Charging:**

1. EV chargers need high PF (>0.95) → use Active PFC
2. THD must be low to avoid grid pollution
3. Three-phase preferred for >7 kW
4. Grid harmonics from chargers regulated by IEEE 519
5. Energy billing in kWh (real power)

**Conclusion:** Understanding grid parameters, wiring, and power concepts is essential for designing, installing, and operating EV charging systems efficiently and economically.

---

## Q6. Hazard / Safety Management of Batteries During & After Operations

**Definition:** Safety management refers to the planned approach to identify, prevent, control, and mitigate hazards associated with EV batteries throughout their lifecycle.

**Major Battery Hazards:**

**1. Thermal Hazards:**

- Overheating during charge/discharge
- Thermal runaway (>80 °C in Li-ion)
- Fire and smoke

**2. Electrical Hazards:**

- Short-circuit (internal/external)
- Overcharging / over-discharge
- Insulation failure → shock

**3. Mechanical Hazards:**

- Crash, puncture
- Drop, vibration
- Casing damage

**4. Chemical Hazards:**

- Electrolyte leakage (corrosive)
- Toxic gas (HF, CO) release
- Cell venting

**5. Environmental Hazards:**

- High humidity, temperature
- Water ingress
- Fire spread to surroundings

**Safety Management Measures:**

**A) During Operation:**

1. **BMS Protection:**
   - Cell voltage limits (2.8–4.2 V)
   - Current limits
   - Temperature limits (0–55 °C)

2. **Thermal Management:**
   - Cooling system (liquid/air)
   - Heaters in cold conditions
   - Temperature uniformity ΔT < 5 °C

3. **Cell Balancing:** Prevent cell over-stress

4. **Insulation Monitoring (IMD):** Detects HV leakage

5. **Pre-charge Circuit:** Soft engagement of contactors

6. **Pyrotechnic Fuses (Pyro-fuse):** Quick isolation in crash

7. **Crash Sensors:** Disconnect HV bus immediately

8. **Venting & Pressure Relief:** Prevents pack rupture

9. **Fire-resistant Pack Casing:** Steel/aluminium with ceramic lining

10. **Functional Safety (ISO 26262):** ASIL-D rated BMS

11. **Driver Alerts:** Dashboard warnings for abnormal events

**B) After Operation / Post-Incident:**

1. **Post-Crash Isolation:** Auto HV disconnect

2. **Cooling Down Period:** Wait before handling

3. **Fire-Fighting:**
   - Class D extinguishers
   - Lots of water (cooling)
   - Lithium-specific extinguishing agents
   - Fire blankets

4. **Quarantine Area:** Separate damaged batteries 15 m away

5. **Safe Transportation:** UN 3480 / UN 3481 packaging

6. **Diagnostics:** Read BMS logs to know cause

7. **End-of-Life Handling:**
   - Discharge to <30% SOC
   - Disassembly in controlled environment
   - Recycling (hydrometallurgy, pyrometallurgy)

8. **Documentation:** Incident report, root-cause analysis

**C) Storage Safety:**

1. Store at 30–50% SOC
2. Cool (15–25 °C), dry environment
3. Fire-resistant cabinets
4. Distance between packs ≥ 1 m
5. Smoke detectors, sprinklers

**D) Personnel Safety (PPE):**

- Insulated gloves (Class 0 / 1 kV)
- Face shield, apron, safety shoes
- Voltage-rated tools
- Lockout-tagout procedures
- Training & certification

**E) Regulatory Compliance:**

1. **AIS 156:** Thermal propagation, battery safety after thermal event
2. **AIS 048:** Traction battery safety
3. **UN 38.3:** Lithium battery transport safety
4. **IEC 62133:** Cell-level safety
5. **ISO 26262:** Functional safety
6. **BIS IS 16893:** Indian battery safety

**F) Failure Modes & Mitigation Table:**

| Hazard | Cause | Mitigation |
|---|---|---|
| Thermal runaway | Internal short, overcharge | BMS cut-off, cooling |
| Fire | Cell rupture | Fire-resistant casing |
| Shock | Insulation failure | IMD, earthing |
| Leakage | Casing crack | Sealed packaging |
| Explosion | Venting blocked | Pressure relief |

**Recent Incidents Driving Improvements:**

- Ola/Pure EV 2W fires (India 2022) → led to AIS 156 update
- Tesla Model S fires → improved thermal isolation

**Conclusion:** Safety management of EV batteries is a holistic effort combining design, control, regulation, and operational discipline to protect users, vehicles, and environment.

---

## Q7. AIS Charging Standards (with EVCI Guidelines)

**Definition:** AIS (Automotive Industry Standards) charging standards are framed by ARAI/MoRTH to regulate the safety, performance, and interoperability of EV charging systems in India.

**Major AIS Charging Standards:**

**1. AIS 138 Part 1: AC Conductive Charging**

- Indian variant of IEC 61851
- Covers charging modes 1, 2, 3
- Connectors: Type 2 IEC 62196, Bharat AC-001
- Power: 3.3 kW to 22 kW
- Communication: Pilot signal (PWM)
- Safety: RCD, earthing, overload protection

**2. AIS 138 Part 2: DC Conductive Charging**

- Covers fast DC charging (Modes 4)
- Connectors: CCS2, CHAdeMO, Bharat DC-001, GB/T
- Power: 50–350 kW
- Communication: CAN bus / PLC
- Safety: Pre-charge, IMD, contactor monitoring

**3. AIS 029: Traction Battery — Requirements for Electric Vehicles (related to charging interface safety)**

**4. AIS 156: Battery Safety post-thermal incidents** — includes charging-related thermal management.

**5. AIS 167:** Standards for swappable battery systems and chargers

**6. AIS 173:** Common charging connector (under draft)

**Indian Bharat EV Charging Standards (under AIS 138):**

**A) Bharat AC-001:**

- Voltage: 230 V (single-phase) or 415 V (three-phase)
- Current: 15 A per phase
- Power: 3 × 3.3 = 10 kW (three-phase) or 3.3 kW (single-phase)
- Connector: IEC 60309 or Type 2
- Use: 2W, 3W, small 4W

**B) Bharat DC-001:**

- Voltage: 48 V – 200 V – 380 V – 750 V DC
- Power: 15, 30, 50, 100 kW
- Connector: GB/T 20234
- Communication: CAN per ISO 15118
- Use: Small to medium EVs

**EVCI (Electric Vehicle Charging Infrastructure) Guidelines:**

Issued by **MoP (Ministry of Power)** in 2018, revised 2022:

**1. Public Charging Stations (PCS):**

- One PCS every 3 km in cities
- One PCS every 25 km on highways
- One DC fast charger every 100 km for long-distance

**2. Minimum Configuration:**

- 1 × CCS (≥50 kW)
- 1 × CHAdeMO (≥50 kW)
- 1 × Type 2 AC (≥22 kW)
- 1 × Bharat DC-001 (15 kW)
- 1 × Bharat AC-001 (10 kW)

**3. Tariff Regulations:**

- De-licensed activity (no license required)
- Service charge: < ₹2.50/kWh (DISCOM electricity)
- Open-access power supply allowed
- Renewable energy preferred

**4. Land & Civil Requirements:**

- Government land at concessional rates
- Adequate parking space
- Safety signage, fire equipment

**5. Grid Connectivity:**

- Dedicated transformer (HT for >100 kW)
- Smart metering
- Grid quality compliance (PF, THD)

**6. Operational Guidelines:**

- 24x7 operation
- Helpline & support
- Real-time status on apps
- Multiple payment options

**7. Safety & Compliance:**

- AIS 138 compliance mandatory
- BIS standards for cables
- Periodic audits

**8. Battery Swapping Stations:**

- Defined under EVCI 2022
- Standardised swappable battery interface (AIS 167)

**9. Subsidies & Incentives:**

- 70–100% capital subsidy in some states
- FAME-II support for charger setup

**10. Role of Stakeholders:**

- **MoP:** Policy framework
- **MoRTH:** Vehicle approval
- **DISCOMs:** Power supply
- **CPOs (Charge Point Operators):** Tata Power, Ather Grid, Statiq, ChargeZone

**Conclusion:** AIS charging standards combined with EVCI guidelines provide a structured, safe, and interoperable framework for nationwide EV charging infrastructure in India.

---

## Q8. BIS Charging Standards

**Definition:** Bureau of Indian Standards (BIS) develops Indian Standards (IS codes) for EV components, chargers, and infrastructure, ensuring quality, safety, and interoperability.

**Role of BIS in EV Charging:**

1. Drafts and notifies IS standards
2. Issues BIS certification (ISI mark)
3. Tests products through BIS-recognised labs
4. Harmonizes Indian standards with IEC/ISO
5. Provides Quality Control Orders (QCO) under MoP/MoHIPE

**Important BIS Standards for EV Chargers & Batteries:**

**1. IS 17017 Series — EV Conductive Charging (harmonised with IEC 61851):**

- **IS 17017-1:** General requirements for EV charging
- **IS 17017-2-1:** Conductive charging interface for AC chargers
- **IS 17017-2-2:** Conductive charging interface for DC chargers
- **IS 17017-2-3:** Vehicle connectors, plugs, sockets
- **IS 17017-21-1:** EV/EVSE AC communication
- **IS 17017-21-2:** EV/EVSE DC communication
- **IS 17017-22:** AC charging stations
- **IS 17017-23:** DC charging stations
- **IS 17017-24:** Digital communication between charging station and BMS

**2. IS/IEC 62196 — Plugs, Socket-outlets & Connectors for EVs:**

- Part 1: General requirements
- Part 2: AC connectors (Type 1, Type 2)
- Part 3: DC connectors (CCS, CHAdeMO, GB/T)

**3. IS 15118 (ISO 15118 equivalent) — V2G Communication Protocol**

**4. IS 17855 — Specification for Power Electronics Converter (Charger Modules)**

**5. Battery Standards:**

- **IS 16893 (Part 1–8):** Lithium-ion battery safety — adapted from IEC 62133
- **IS 16270:** Secondary cells & batteries safety
- **IS 16046:** Safety requirements for portable Li-ion
- **IS 17855:** Specifications for EV battery pack and system

**6. IS 9000 / IS 15498:** Environmental testing for chargers (vibration, shock, climate)

**7. IS 13252 (Safety of IT equipment):** Applicable for charger electronics

**8. IS 9540-1, 2:** Energy storage system safety

**9. IS 17387 — EV Charging Equipment Conformity (in line with EVCI guidelines)**

**Charger Performance Requirements (per BIS):**

1. **Efficiency:** ≥ 90% at full load
2. **Power Factor:** ≥ 0.95
3. **THD:** < 5%
4. **EMI/EMC compliance:** As per CISPR 22 / IS 6873
5. **IP rating:** IP54 indoor, IP55+ outdoor
6. **Operating temperature:** −10 °C to +50 °C
7. **Communication protocol compliance**
8. **Safety: insulation, grounding, leakage protection**

**Testing Requirements:**

- Type testing of complete charger
- Cable and connector endurance (10,000 mating cycles)
- Climatic testing (cold, heat, humidity)
- Short-circuit, overload tests
- Surge withstand (IS 17017-1 Annex B)
- Insulation resistance & dielectric strength
- Functional safety
- Communication conformance

**Certification Procedure:**

1. Application to BIS
2. Document submission (test reports, drawings)
3. Factory inspection
4. Product testing at recognized lab
5. Grant of ISI mark
6. Annual surveillance audits

**Recognized BIS Labs:**

- BIS Sahibabad
- ARAI Pune
- ICAT Manesar
- CPRI Bangalore
- ERTL Mumbai

**Relationship with AIS Standards:**

- **AIS** by ARAI/MoRTH → focuses on vehicle-level approval
- **BIS** under MoCAF&PD → focuses on product/component certification
- Both work in parallel; AIS adopts many BIS norms

**Recent Developments:**

- BIS notified IS 17017 series in 2018; updated periodically
- Mandatory ISI mark for EV chargers under QCO (2023 onwards)
- Harmonization with IEC and EU standards in progress

**Conclusion:** BIS standards (IS 17017, IS 16893, IS 17855 etc.) ensure that EV chargers and batteries sold in India meet international safety, performance, and interoperability levels.

---

## Q9. End-of-Life (EOL) Management of EVs and Their Batteries

**Definition:** End-of-Life management is the systematic process of handling, dismantling, recycling, and disposing of EVs and their batteries when they are no longer fit for primary use, ensuring environmental safety and resource recovery.

**Need for EOL Management:**

1. Growing EV population and aging batteries
2. Recovery of critical materials (Li, Co, Ni, Cu, Al)
3. Environmental protection (electrolyte, metals are hazardous)
4. Circular economy and sustainability
5. Compliance with regulations (Battery Waste Management Rules 2022, India)

**EOL Stages:**

**Stage 1 — Vehicle EOL:**

1. **Deregistration:** Owner submits documents to RTO
2. **Authorized Vehicle Scrapping Facility (AVSF):** Vehicle handed over
3. **Depollution:** Removal of battery, fluids, refrigerants
4. **Component Recovery:** Reusable parts segregated (motor, electronics, lights)
5. **Body Shredding:** Frame shredded; metals separated
6. **Material Recycling:** Steel, Al, Cu, plastics recycled
7. **Certificate of Destruction (CoD):** Issued to owner

**Stage 2 — Battery EOL (when capacity < 70–80%):**

1. **Removal from Vehicle:** Trained technicians disconnect HV
2. **Diagnostic Assessment:** BMS data, capacity measurement
3. **Pathway Decision:**
   - Reuse (Second-Life Application)
   - Recycle (Material Recovery)
   - Dispose (only if irreparable)

**Battery End-of-Life Pathways:**

**A) Second-Life / Reuse Applications:**

After EV use, batteries with 70–80% capacity can serve in less demanding applications for another 5–10 years:

- Stationary energy storage (homes, offices)
- Grid storage (peak shaving, renewable integration)
- Telecom tower backup
- Solar + battery systems
- EV charging station buffer
- Streetlight/LED projects

Examples: Nissan-Sumitomo 4R Energy, BMW/Vattenfall, Toyota Sweep Energy, Tata-Nunam (India).

**B) Recycling Processes:**

1. **Pre-treatment:**
   - Discharging cells (resistive load)
   - Disassembly into modules, cells
   - Removal of casings, BMS, wiring

2. **Mechanical Processing:**
   - Crushing in inert/nitrogen atmosphere
   - Separation by magnetic, eddy current, gravity
   - Black mass extraction (cathode/anode powder)

3. **Hydrometallurgy:**
   - Acid leaching (H₂SO₄ + H₂O₂)
   - Solvent extraction
   - Precipitation of Li, Co, Ni salts
   - High purity recovery (>95%)

4. **Pyrometallurgy:**
   - High-temperature smelting (>1200 °C)
   - Recovers Co, Ni, Cu as alloy
   - Li lost in slag (lower efficiency)

5. **Direct Recycling:**
   - Cathode material recovered intact
   - Most efficient, research stage

6. **Bio-leaching:**
   - Microorganisms extract metals
   - Eco-friendly, slow

**Materials Recovered:**

| Material | Recovery rate |
|---|---|
| Cobalt | >90 % |
| Nickel | >90 % |
| Copper | >95 % |
| Aluminium | >95 % |
| Lithium | 50–80 % |
| Graphite | 60–80 % |

**C) Safe Disposal (only for non-recyclable parts):**

- Hazardous waste landfills
- Strict environmental controls

**Regulatory Framework (India):**

1. **Battery Waste Management Rules, 2022:**
   - Extended Producer Responsibility (EPR)
   - Producers responsible for collection & recycling
   - Mandatory targets year-wise

2. **E-Waste Management Rules**

3. **Hazardous Waste Rules, 2016**

4. **CPCB Guidelines:** Storage, transportation, recycling

5. **Vehicle Scrapping Policy 2021:** Mandatory scrapping after 15 years (commercial) or 20 years (private)

**Key Players in India:**

- Attero Recycling
- Tata Chemicals (Nunam)
- Lohum Cleantech
- Recyclekaro
- Exigo Recycling
- BatX Energies

**Challenges in EOL Management:**

1. Diverse cell chemistries — different processes
2. Battery design not standardised (hard to disassemble)
3. Safety hazards during dismantling
4. Lack of certified recyclers
5. High cost of recovery vs raw material price
6. Logistics for collection
7. Awareness among users

**Future Trends:**

- Standardized battery design for recyclability
- Battery passport (digital lifecycle data)
- AI-driven sorting & disassembly
- Closed-loop manufacturing (raw → battery → recycle → raw)
- Government incentives for recyclers
- Urban mining

**Benefits:**

- Reduced mining dependency
- Lower CO₂ footprint
- Resource security
- Employment generation
- Circular economy

**Conclusion:** Effective EOL management of EVs and batteries is essential for sustainable electric mobility. Reuse, recycling, and responsible disposal — supported by regulations and technology — ensure the EV revolution is truly green.

---

## Q10. Charging Methods, Charging Standards, EVCI Guidelines & Charging Infrastructure

**A) Charging Methods:**

**Definition:** Charging method refers to the technique by which electrical energy is transferred from source to EV battery.

**1. Conductive Charging (Wired):**

- Direct electrical connection via cable & connector
- Most common method
- Subcategories:
  - AC charging (slow / medium)
  - DC charging (fast / ultra-fast)

**2. Inductive (Wireless) Charging:**

- Energy transfer via magnetic field (resonant coils)
- No physical cable
- SAE J2954 standard
- Stationary or dynamic (in-motion)
- Used in buses, future autonomous EVs
- Efficiency 85–92%

**3. Battery Swapping:**

- Discharged battery swapped with charged one in 2–5 min
- Standardized swappable battery (AIS 167)
- Companies: Sun Mobility, Bounce, Yulu in India
- Suitable for 2W and 3W

**4. Conductive Pantograph (Top-Down):**

- Overhead pantograph connects to bus roof
- Used in e-buses at bus stops (ABB, Volvo)

**5. Solar Direct Charging:**

- DC from solar panels directly to battery
- Renewable, off-grid possible

**6. Vehicle-to-Vehicle (V2V) Charging:**

- EV charges another EV via portable inverter

**B) Charging Standards (Global & Indian):**

**Connector Types:**

| Connector | Type | Region | Power |
|---|---|---|---|
| Type 1 (J1772) | AC, single-phase | USA, Japan | up to 7.4 kW |
| Type 2 (Mennekes) | AC, single/three-phase | EU, India | up to 22 kW |
| CCS1 | AC+DC combo | USA | up to 350 kW |
| CCS2 | AC+DC combo | EU, India | up to 350 kW |
| CHAdeMO | DC | Japan | up to 400 kW |
| GB/T | AC & DC | China | up to 250 kW |
| Tesla NACS | AC/DC | USA, becoming SAE J3400 | up to 250 kW |
| Bharat AC-001 | AC | India | 10 kW |
| Bharat DC-001 | DC | India | 15/30/50/100 kW |

**Charging Modes per IEC 61851 / AIS 138:**

- **Mode 1:** Standard AC socket, no protection — banned in India
- **Mode 2:** Standard socket with in-cable control box (IC-CPD), max 16 A
- **Mode 3:** Dedicated AC EVSE with Type 2 connector
- **Mode 4:** DC fast charging with off-board charger

**Communication Standards:**

- ISO 15118 (V2G, Plug-and-Charge)
- OCPP 1.6 / 2.0.1 (Open Charge Point Protocol)
- OCPI (roaming between operators)
- IEC 61850 (smart grid integration)

**C) EVCI (Electric Vehicle Charging Infrastructure) Guidelines:**

**Issued by MoP (Ministry of Power), India:**

**Key Provisions:**

1. **Public Charging Stations (PCS):**
   - 1 station every 3 km in city grid
   - 1 station every 25 km on highways
   - 1 fast charger every 100 km for heavy vehicles

2. **De-licensed Activity:** No electricity license needed for PCS

3. **Tariffs:**
   - Electricity at single-part tariff for PCS
   - Service charge cap as per state regulator

4. **Open Access:** Allowed for PCS

5. **Land Allotment:**
   - Government land on lease at 1₹ per kWh revenue share
   - Priority for highways, urban areas

6. **Subsidies under FAME-II:**
   - Up to 70% capex support for PCS
   - 100% for highways under special scheme

7. **Connectors Required at PCS:**
   - CCS2 (≥50 kW)
   - CHAdeMO (≥50 kW)
   - Type 2 AC (22 kW)
   - Bharat DC-001 (15 kW)
   - Bharat AC-001 (10 kW)

8. **Safety Standards:** Compliance with AIS 138, IS 17017

9. **Smart Charging:** Demand response, load management

10. **Battery Swapping Policy 2022:** Standardisation, subsidies

**D) Charging Infrastructure Components:**

1. **Power Source:** Grid / Solar / Storage
2. **Distribution Transformer**
3. **LT/HT Switchgear**
4. **EV Supply Equipment (EVSE):** AC or DC charger
5. **Cables and Connectors**
6. **Metering & Billing System:** Smart meter, payment gateway
7. **Communication Network:** OCPP, 4G/5G, Wi-Fi
8. **Central Management System (CMS):** Cloud-based monitoring
9. **User Interface:** Mobile app, RFID, QR code
10. **Safety Equipment:** Fire extinguishers, signage, lighting
11. **Civil Infrastructure:** Canopy, parking, kerb stops

**E) Types of Charging Infrastructure:**

1. **Home Charging:** Single-phase wall-box
2. **Workplace Charging:** AC slow chargers
3. **Public Charging Stations:** Mix of AC & DC
4. **Highway Fast-Charging Hubs:** Multiple 50–350 kW DC chargers
5. **Battery Swapping Stations**
6. **Fleet Depot Charging:** Buses, taxis, last-mile
7. **Captive Charging (Industrial)**
8. **Inductive Charging Bays:** Future

**F) Indian EV Charging Ecosystem Players:**

- **CPOs:** Tata Power EZ Charge, Ather Grid, Statiq, ChargeZone, Jio-bp, BPCL, IOCL, HPCL, ChargePoint
- **OEMs:** Tata, Mahindra, Hyundai, MG, Ather, Ola
- **Battery Swap:** Sun Mobility, Bounce, Battery Smart, Yulu

**G) Future Trends:**

1. Ultra-fast 350 kW charging (800 V architecture)
2. V2G — bidirectional energy
3. Megawatt charging for heavy trucks (MCS 1.25 MW)
4. Wireless dynamic charging on highways
5. AI-driven smart charging
6. Renewable + storage powered PCS
7. Universal connector standardisation

**Conclusion:** A robust mix of charging methods, harmonised standards, supportive EVCI guidelines, and comprehensive charging infrastructure forms the backbone of EV adoption in India and globally.

---

## Quick Revision — Marks Distribution Strategy (For 9-Mark Answers)

For each 9-mark answer in your exam, structure as:

| Section | Marks | Content |
|---|---|---|
| Definition/Introduction | 1 | 2–3 lines, clear definition |
| Diagram (if needed) | 2 | Neat labelled sketch |
| Classification / Types | 2 | Bullet points / table |
| Working / Procedure / Equation | 2 | Step-by-step explanation |
| Advantages / Disadvantages / Applications | 1 | Bulleted lists |
| Conclusion | 1 | 2–3 line wrap-up |

**Total = 9 marks**

**Time per question (9 marks): ~12–14 minutes**

All the best for your exam! Practice diagrams especially for: BMS structure, BLDC motor, Li-ion battery, Suspension systems, Charger architecture, and Drive-train topologies.
