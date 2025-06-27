# client-crud-system

Client Registration System with Flask and MySQL
This project is a simple web-based system for client registration and management, developed with Python using the Flask microframework for the backend and HTML/CSS for the frontend. It implements essential CRUD (Create, Read, Update, Delete) operations for managing client records in a MySQL database.


🚀 Features:

 - Client Registration: Add new clients to the database with fields for name, email, phone, and address.

 - Client Listing: View all registered clients in a clear and organized table on the homepage.

 - Client Editing: Select a client from the list to update their information.

 - Client Deletion: Remove unwanted clients from the system.

 - User-Friendly Interface: Simple and responsive design with CSS for an enhanced user experience.

 - Flash Messages: Provides visual feedback to the user regarding the success of operations or encountered errors.

🛠️ Technologies Used

Backend:
- Python 3.x
- Flask (Web Microframework)
- mysql-connector-python (Python connector for MySQL)

Frontend:
- HTML5
- CSS3

Database:
- MySQL


🚀 How to Use
1- Homepage (/):
- You will see a form to Register New Client. Fill in the fields and click "Register Client".
- Below, the "Registered Clients" section will display a list of all clients.

2- Delete Client:
- In the client list, click the "Delete" button next to the client you wish to remove.

3- Edit Client:
- In the client list, select the desired client by clicking the radio button next to their ID.
- After selecting, click the "Edit Selected Client" button below the table.
- You will be redirected to the edit page, with the client's data pre-filled.
- Make the necessary changes and click "Update Client" to save.
- Use the "Cancel" button to return to the homepage without saving.

📄 License
This project is open-source and licensed under the MIT License.
