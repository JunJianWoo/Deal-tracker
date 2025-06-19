# DealTracker

Collects deals on tech goods from online sources to streamline finding good deals and making informed purchase decisions.

Features:
- Find deals from online sources
- Filter by price range, discount percent, and vendor
- Find similar products on deals
- View the previous deals and pricings for a product

## Steps

### Execute backend

- Change directory to backend folder: `cd backend`
- Download dependencies: `pip install -r requirements.txt`
- Create a MySQL database and modify the DATABASE_URI in .env file: `DATABASE_URI=mysql://<your-username>:<your-password>@<host>:<port>/<database_name>`
- Run the backend `python app.py`

### Execute frontend

- On a separate terminal, change directory to frontend folder: `cd frontend`
- Download dependencies: `npm install`
- Run the frontend: `npm run dev`
- Navigate to the website link shown
