# Vehicle Management System

A Django-based vehicle management application for organising vehicle records and supporting operational fleet workflows.

## Overview

The project demonstrates how a relational web application can model vehicles and their associated management workflows using Django.

## Features

- Vehicle record management
- Structured relational data models
- Django admin management
- Server-rendered web interface
- Extensible architecture for fleet operations

## Technology Stack

- Python
- Django
- SQLite for local development
- HTML/CSS/JavaScript

## Getting Started

```bash
git clone https://github.com/Eunice-ctrlz/Vehicle-Management.git
cd Vehicle-Management
python -m venv .venv
```

Activate the virtual environment and install the project's dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

## Production Considerations

For production use, move secrets into environment variables, use PostgreSQL or another production database, configure `DEBUG=False`, add automated tests and deploy behind a production WSGI server/reverse proxy.

## Roadmap

- Driver management
- Vehicle maintenance schedules
- Fuel and expense tracking
- Trip and mileage records
- Fleet analytics
- REST API
- Automated testing and CI/CD

## Author

**Eunice Muturi**

GitHub: https://github.com/Eunice-ctrlz
