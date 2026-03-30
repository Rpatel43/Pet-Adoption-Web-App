# Pet Adoption Web App
A full-stack platform connecting adoptable pets with users. Built with a focus on seamless user experience and robust data management.

## Features
* **User Authentication:** Secure login for adopters and shelter admins.
* **Pet Listings:** Dynamic browsing with filtering by species, age, and breed.
* **Adoption Requests:** Integrated form submission for adoption applications.
* **Responsive Design:** Fully optimized for mobile and desktop viewing.

## Tech Stack
* **Frontend:** React (TypeScript), Vite, Tailwind CSS
* **Backend:** Python (Flask), SQLAlchemy
* **DevOps:** Docker, GitHub Actions (CI/CD)
* **Design:** [Figma](https://www.figma.com/design/0H0O1hAC6xJz2soKSml86l/CSE2102-Site-Prototype?node-id=0-1&t=XUrpxJiLNF33jHGe-1) | **Project Management:** [Trello](https://trello.com/b/0zbMYZli/cse2102-team29)

## Getting repo locally and getting db
1. clone repo
2. `pip install -r requirements.txt`
3. `generate key: 'export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32)")`
4. `flask init-database`
5. `flask run --host=0.0.0.0`

# docker
1. `docker build -t team29/pet-adopt-api:latest .`
2. `docker run --rm -p 5000:5000 \ -e SECRET_KEY=${SECRET_KEY} \ team29/pet-adopt-api:latest`
3. OR, if secret key isn't needed (the way we do it locally): `docker run --rm -p 5000:5000 team29/pet-adopt-api:latest`

# to run the frontend
1. `cd frontend`
2. `npm run dev`
