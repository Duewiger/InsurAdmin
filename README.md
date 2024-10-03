# InsurAdmin

**InsurAdmin** is an insurance management application developed with **Django** for the backend and **Django Template Language** for the frontend. Users can create accounts, manage their insurance policies, and consult the insurance assistant.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Technology Stack](#technology-stack)
3. [Installation and Setup](#installation-and-setup)
4. [Roadmap](#roadmap)
5. [Contributing](#contributing)
6. [License](#license)

---

## Key Features

- **Account and Policy Management**: Users can create accounts and manage their insurance policies, including documents.
- **Insurance Assistant**: Users can ask questions about insurance and automate tasks (e.g., canceling policies).
- **Email and SMS Communication**: Integration with **Twilio**.
- **Automation**: Future updates will allow the assistant to execute scripts for policy management.
- **OpenAI Integration**: AI-driven responses and document processing.
- **Security**: MFA, `django-recaptcha`, and Django's built-in security features.

---

## Technology Stack

### Backend (Django)
- **Framework**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Security**: Axes, CSRF, CORS policies
- **Email**: Twilio, SMTP

---

## Installation and Setup

To set up the project locally:

### Backend (Django)
1. Clone the repository:
    ```bash
    git clone https://github.com/Duewiger/InsurAdmin.git
    cd InsurAdmin
    ```
2. Create a `.env` file based on `.env.example`.
3. Set up Docker and run the containers:
    ```bash
    docker-compose up --build
    ```
4. Migrate the database:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

---

## Roadmap

- **API Performance Optimization**
  - Implement caching (Memcached, Redis) to reduce API response times.
  - Centralize API logic for better reusability.
- **UI/UX Improvements**: Revamp the frontend for a more appealing design.
- **Automation**: Automatic cancellation, creation, and organization of insurance policies.
- **Mobile Version**: Develop a mobile-friendly frontend using Flet.
- **Integration**: Web scraping and Google Maps API to gather contact data for insurers and brokers.
- **Unit Testing & CI/CD**
  - Establish comprehensive unit tests.
  - Implement CI/CD pipelines with GitHub Actions.

---

## Contributing

Contributions to InsurAdmin are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a Pull Request.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.