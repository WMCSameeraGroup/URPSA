

## Methodology

### Overview

The **Unbiased Reaction Path Search Algorithm (URPSA)** is an automated method for discovering reaction pathways through the systematic exploration of possible interactions between molecular fragments. The process is designed to minimize reliance on human intuition by providing a structured approach to identifying new pathways.

> The workflow of the URPSA is illustrated in the diagram below.  
> _![Workflow of the URPSA](assets/diagram.png)_

The process begins by placing user-defined molecular fragments randomly on the surface of a sphere. These fragments are then gradually moved toward the center to encourage interactions. At each step, the system checks for atomic repulsions and discards any unphysical configurations.

Next, the **single point energy** of the configuration is calculated using an external quantum chemistry package, *Gaussian16*. Bond formation between fragments is analyzed based on interatomic distances, and newly formed fragments are identified.

High-energy pathways are filtered out using a user-defined energy threshold, ensuring that only feasible routes are considered. Low-energy pathways are preserved for further analysis.

The entire process is automated through **Python**, while quantum mechanical calculations are carried out by *Gaussian16*.

---

### Random Orientation Generation

The calculation begins by randomly placing user-defined fragments (atoms or molecules) on the surface of a sphere of a given radius. Each fragment has an equal probability of being positioned at any point on the surface.

> _Note: Overlapping placements are automatically discarded in a later step._

The goal of spherical placement is to expose the potential energy surface (PES) to diverse orientations, thereby increasing the chances of discovering non-trivial interactions.

---

### Push Fragments Toward the Centre

Each fragment is moved inward toward the center of the coordinate system by a linear distance. This is performed by calculating the position vector of the fragment's center of mass and reducing it by a user-defined step size, effectively pushing fragments closer to encourage interaction.

---

### Check for Small Inter-Atomic Distances

Unphysical overlaps between atoms of different fragments are checked and eliminated. If any two atoms from separate fragments are closer than a specified multiple of their combined covalent radii, the pathway is discarded.

---

### Single Point Energy Calculation

For each iteration, a **single point energy** calculation is performed to assess the energy of the system at that configuration.

---

### Filter Out High-Energy Pathways

If the energy of a configuration exceeds that of the initial state by more than a specified threshold, the pathway is discarded. This step ensures only energetically feasible structures are retained.

**Energy gap expression:**

```math
\text{Energy gap} = \text{Energy}_{\text{current}} - \text{Energy}_{\text{initial}}
```

---

### Fragment Identification

When fragments interact, new bonds may form, resulting in newly connected substructures. A distance-based algorithm is used to identify such fragments. Two atoms are considered bonded if:

```math
d_{ij} < f \times (r_i + r_j)
```

Where:

- \( d_{ij} \) is the distance between atoms \( i \) and \( j \),
- \( r_i \), \( r_j \) are covalent radii,
- \( f \) is a tolerance factor, typically around 1.1[^1].

[^1]: Zimmerman, P. M. *J. Comput. Chem.*, 2013.

---

### Fragment Count Check

If only a single fragment remains after interaction, it implies that all fragments have reacted to form one connected structure. At this point, further pushing is not possible. The resulting structure is then treated as the **observed product** and recorded, along with any constraints applied during the process.

---

### Final Optimization Without Constraints

The identified product is re-optimized without any geometric constraints to ensure it relaxes to its nearest energy minimum. A new input file is generated for this geometry optimization, allowing the system to converge to a true local minimum on the PES.

---
