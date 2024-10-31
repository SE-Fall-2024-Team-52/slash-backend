# Installation Steps

Follow these steps to set up the project:

1. **Install Requirements**

   ```sh
   pip install -U -r requirements.txt
   ```

2. **Set Up PostgreSQL Database**

   - Ensure you have a PostgreSQL database running.
   - Create a `.env` file in the root directory by referring to the `.env.example` file.
   - Add your PostgreSQL username and password to the `.env` file.
   - If necessary, update the host in `/database/database.py`.

3. **Run the Application**
   ```sh
   flask run
   ```
