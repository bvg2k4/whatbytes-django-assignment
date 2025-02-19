## **Setup Instructions**
1. Clone the repository:
   ```bash
   git clone <your-repo-link>
   cd auth_system
2.Install dependencies:
   ```bash
   pip install -r requirements.txt
3.Run migrations:
   ```bash
   python manage.py migrate
4.Create a superuser:
   ```bash
   python manage.py createsuperuser
5.Start the server:
   ```bash
   python manage.py runserver
