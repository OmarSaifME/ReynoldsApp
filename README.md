\# ReynoldsApp — CFD Assistant



A lightweight desktop tool for CFD preprocessing, built with Python and Tkinter.  

Designed to reduce cognitive friction during solver setup and mesh verification.



\## Features



\- 🛩️ \*\*Angle of Attack\*\* – Compute velocity components and force vectors for Fluent boundary conditions

\- 📊 \*\*Reynolds Number\*\* – Convert between Re and flow velocity with fluid property inputs

\- 📐 \*\*Grid Convergence Index (GCI)\*\* – Quantify discretization error for mesh refinement studies (Roache method)



All outputs include one‑click copy buttons for easy pasting into Fluent or your notes.



\---



\## Download



Get the latest standalone `.exe` from the \[Releases](https://github.com/yourusername/reynoldsapp/releases) page.  

No Python installation required.



\---



\## Run from Source



Clone the repository and install dependencies:



```bash

git clone https://github.com/yourusername/reynoldsapp.git

cd reynoldsapp

pip install -r requirements.txt

python gui/re\_app\_gui.py

