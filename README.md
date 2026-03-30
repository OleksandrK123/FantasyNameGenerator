Fantasy Name Generator ⚔️
A Django-based web application that generates unique fantasy names for various races (Elves, Orcs, Mages, etc.) using a custom algorithm that combines prefixes, roots, and suffixes.

🚀 Tech Stack
Backend: Django 5.x

Database: PostgreSQL (running in a Docker container)

Environment: Docker & Docker Compose

API: Django REST Framework (for AJAX and external access)

🛠️ Features
Name Generation: Procedural generation for multiple races (Elf, Orc, Mage, Demon, Legendary, Dwarf).

History Tracking: Stores the last 50 generated names in the PostgreSQL database.

Favorites: Authenticated users can save their favorite names to a personal list.

AJAX-Powered: Generate names and filter history instantly without page reloads.

Clean UI: Organized layout with categories and a "Legendary" name chance mechanic.
