# 🐍 Mastered Object-Oriented Programming in Python

Welcome to my Python OOP showcase! After diving deep into the core concepts of **Object-Oriented Programming (OOP)**, I applied these principles to build clean, maintainable, and interactive Python applications—moving from fundamental data structures to dynamic 2D game loops.

---

## 🛠️ Core OOP Pillars & Concepts Covered

Throughout this journey, I focused on learning how to architect software using industry-standard OOP principles:

* **Abstraction:** Hiding complex internal logic behind clean, easy-to-use interfaces (e.g., exposing a `.jump()` or `.update_physics()` method while hiding raw coordinate math).
* **Encapsulation:** Shielding object attributes from external interference and bundling state management cleanly within dedicated class definitions.
* **Inheritance:** Establishing hierarchical relationships to reuse logic across common entities without duplicating code.
* **Polymorphism:** Allowing different classes to share common method signatures (`.draw()`, `.update()`, `.is_colliding()`) so the application engine can process them uniformly.
* **Composition & Aggregation:** Structuring entities to contain instances of other objects (like a Game Controller managing collections of `Obstacle`, `Particle`, and `Player` instances).
* **Design Patterns:** Applying practical architectures such as the **Factory Pattern** for dynamic obstacle generation and **State Management** for menu/gameplay loops.

---

## 🚀 Key Projects Built

### 1. 🏦 Digital Bank Simulator
A secure, interactive command-line application designed to demonstrate robust **Encapsulation** and **State Management**.

* **Key Concepts Featured:**
  * **Encapsulation:** Private attributes (e.g., account balance, pin numbers) protected against direct external manipulation.
  * **Custom Exception Handling:** Built-in validation rules for handling invalid deposits, insufficient funds, or wrong credentials.
  * **Domain Modeling:** Separate abstractions for `Customer`, `Account`, and `TransactionHistory` entities.

---

### 2. 🔷 OOP Geometry Dash (2D Rhythm Platformer)
A complete, interactive 2D desktop game built strictly with Python's standard `tkinter` graphics engine—applying OOP principles to real-time physics, game loops, and UI rendering.

* **Key Concepts Featured:**
  * **Class Inheritance Hierarchy:** A foundational `GameObject` base class extended by `Player`, `Spike`, `JumpPad`, `Particle`, and `ScorePopup`.
  * **Polymorphic Rendering:** The central game engine updates and draws arrays of obstacles and particles seamlessly regardless of their specific concrete class.
  * **Factory Design Pattern (`LevelFactory`):** Dynamically filters and instantiates difficulty-based obstacle layouts (`EASY`, `MEDIUM`, `HARD`) with auto-scaled speeds and spike spacing.
  * **Real-time Vector & Rotation Math:** Trigonometric corner calculations inside the `Player` class to render continuous 2D cube rotations during jump arcs.
  * **Full Game State Machine:** Manages state transitions across `MENU`, `PLAYING`, `PAUSED`, `GAMEOVER`, and `WIN` screens, complete with an interactive victory modal and full-screen resolution scaling (`F11`).
