# Smart Distribution Center Management System

## Project Overview

The **Smart Distribution Center Management System** is an AI-oriented project focused on addressing inefficiencies in distribution-center operations such as goods movement, manual inventory handling, non-optimal picking paths, and delayed operational decisions.

The project models a distribution center as a **search environment**, where locations are treated as states and movements are treated as actions. AI search concepts are proposed for routing, task selection, and resource scheduling.

---

## Problem Statement


The project addresses the following problems:

- Inefficient goods movement
- Manual inventory handling
- Non-optimal picking paths
- Delayed operational decisions
- Route selection and movement cost
- Task allocation
- Operational constraints

AI search concepts are proposed for **routing, task selection, and resource scheduling**.

---

## Problem Context

A distribution center contains:

- Storage locations
- Aisles
- Picking points
- Dispatch areas

Route or task choices that ignore distance, cost, and constraints can increase travel time and effort.

The project therefore models the distribution center as a **search environment**, where:

- Locations represent states
- Movements represent actions

---

## Problem Understanding

The problem has been divided into four major AI tasks:

1. Graph / state-space representation
2. Path search
3. Heuristic route selection
4. Constraint handling for slot and task conflicts

This follows the Unit 1 problem formulation using:

- Initial state
- Successor function
- Goal test
- Path cost

Literature has also been reviewed to support future real-time inventory integration.

---

## Objectives

- Represent locations and movements as a searchable graph.
- Find efficient picking and movement routes using search techniques.
- Use heuristics to prioritize promising routes.
- Model scheduling and slot restrictions as constraints.
- Compare route quality using path cost and search effort.
- Provide a base for later IoT, inventory-data, and digital-twin extensions.

---

## Target Users / Stakeholders

### Warehouse / Distribution Center Manager
Monitors operations and resources.

### Inventory Staff
Locates, picks, and moves items.

### Dispatch / Logistics Team
Coordinates outgoing orders.

### System Administrator / Developer
Maintains data and algorithms.

### Future AMR / AGV Integration
Future deployment may connect the routing layer with AMR/AGV controllers.

---

## Literature Review

Four research papers were reviewed during the initial research phase.

### 1. Araújo, Vale, Longras, Dias & Rocha (2026)

**"Warehouse Layout Improvement and Routing Optimization…"**

The research focuses on:

- ABC classification
- Layout restructuring
- Nearest-neighbour routing

These findings support the project's routing and layout focus.

### 2. Ho, Tang, Lee, Tam & Chow (2026)

**"Toward Industry 5.0: An IoT-Enabled Digital Twin…"**

The research integrates:

- Replenishment
- Picking
- Packing
- Scenario simulation
- Energy-aware sustainability
- Resilience

These concepts support future smart-warehouse extensions.

### 3. Arvind, Shrinidhi, Deepa & Maheedhar (2025)

**"Intelligent Warehousing…"**

The research combines:

- Machine Learning
- RFID / IoT
- Edge computing
- Robotics
- KNN routing

These findings support future smart-inventory extensions.

### 4. Tsarouhas & Papaevangelou (2024)

**"Critical Steps and Conditions…"**

The research highlights:

- Digital Transformation
- Quality 4.0
- HRM
- Logistics 4.0
- Industry 4.0 adoption

### Literature Review Summary

Together, the reviewed studies support:

- Routing efficiency
- Layout efficiency
- Smart-warehouse integration
- IoT
- Digital-twin extensions
- Sustainable warehouse management

---

## AI Concepts Identified for Application

### Unit 1

The following concepts have been identified:

- State-space / graph representation
- BFS
- DFS
- Heuristic Search
- Greedy Best-First Search
- A* Search
- Constraint Satisfaction Problem (CSP)

### A* Search

A* has been selected as the main **cost-aware route candidate** using:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` represents the cost of reaching a node
- `h(n)` represents the heuristic estimate

### CSP

Constraint Satisfaction Problem is identified for:

- Slot scheduling
- Task scheduling
- Allocation
- Constraint handling

### AO*

AO* was reviewed but was not prioritized.

### Unit 2

The following concepts have also been studied:

- Game-tree / state-transition thinking
- Minimax
- Alpha-Beta pruning

These are considered for a **controlled strategic decision simulation**.

They are conceptual and are not being treated as ordinary warehouse-routing algorithms because ordinary warehouse routing is not adversarial.

---

## Work Completed During Month 1

During Month 1, the team:

- Finalized the project theme as an AI-oriented **Smart Distribution Center Management System**.
- Identified key problems including route selection, movement cost, task allocation, and operational constraints.
- Converted the distribution center into a graph/state-space model with locations as nodes and feasible movements as edges.
- Compared Unit 1 uninformed and informed search methods.
- Selected A* as the main cost-aware routing candidate using `g(n)` and `h(n)`.
- Identified CSP for allocation and scheduling under variables, domains, and constraints.
- Reviewed four research papers.
- Connected research findings to routing/layout efficiency, smart-warehouse integration, IoT, and digital-twin extensions.
- Studied Unit 2 Minimax and Alpha-Beta for a future strategic decision simulation.

---

## Challenges Faced

The main challenge was translating a real distribution-center environment into a clean AI search model while retaining operational constraints.

Another challenge was separating core algorithms from comparison and future concepts.

- BFS / DFS provide baselines.
- A* is considered more suitable for weighted routing.
- Minimax is limited to a defined strategic simulation rather than ordinary warehouse routing.

---

## Team Contribution

The team jointly contributed to:

- Problem identification
- Requirements discussion
- AI concept mapping
- Literature review
- Project planning
- Problem understanding
- Algorithm study
- System abstraction
- Documentation

Individual names and exact task ownership can be added in the project metadata.

---

## Current Progress

### Overall Progress: 25%

The following work has been completed:

- Problem understanding
- Scope definition
- Stakeholder identification
- Literature review
- AI mapping
- Initial architecture planning

Implementation and testing remain.

---

## Plan for Next Review

The next stage of the project will focus on:

- Implementing the distribution-center graph/state representation.
- Developing and testing baseline search and A* routing with a suitable heuristic.
- Defining path-cost metrics and comparing search strategies.
- Building the first CSP scheduling/allocation model.
- Building a small Minimax/Alpha-Beta strategic simulation.
- Integrating the algorithms.
- Collecting initial results and screenshots.
- Retaining IoT, inventory, and digital-twin features as future extensions.

---

## Project Information

| Field | Details |
|---|---|
| Program | B.Tech CSE |
| Course | Artificial Intelligence |
| Course Code | CCSAI0301 |
| Faculty | Dr. Mohd. Nazim |
| Assignment Type | Group Assignment / PBL Project |
| Group | 3 |
| Reporting Period | Month 1 |
| Overall Progress | Approximately 25% |
| SDG | SDG 9 – Industry, Innovation and Infrastructure |
| Submission Date | 12/09/2026 |

---

## Team

**Group 3**

- Aashini Singh
- Amulya Pratap Singh
- Aditya Upadhyay
- Ananya Rastogi
- Abhirag Verma

---

