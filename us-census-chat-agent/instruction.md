### instruction.md

### How to Run the US Census Chat Agent

#### Prerequisites

- Python 3.9 or higher installed
- A Snowflake account with access to the US Open Census dataset
- An OpenAI API key
- Internet connection

---

### Step 1: Clone the Repository

- Open terminal or PowerShell
- Run:
  - `git clone <your-repo-url>`
  - `cd us-census-chat-agent`

---

### Step 2: Setup Backend Environment

- Navigate to project root (already in `us-census-chat-agent`)
- Create virtual environment:
  - `python -m venv .venv`
- Activate virtual environment:
  - Windows: `.venv\Scripts\activate`
  - Mac/Linux: `source .venv/bin/activate`
- Install dependencies:
  - `pip install -r requirements.txt`

---

### Step 3: Configure Environment Variables

- Create a file named `.env` in the root folder
- Add the following variables:

  - `OPENAI_API_KEY=your_openai_key`
  - `OPENAI_MODEL=gpt-4.1-mini`
  - `SNOWFLAKE_USER=your_user`
  - `SNOWFLAKE_PASSWORD=your_password`
  - `SNOWFLAKE_ACCOUNT=your_account`
  - `SNOWFLAKE_WAREHOUSE=COMPUTE_WH`
  - `SNOWFLAKE_DATABASE=US_OPEN_CENSUS_DATA__NEIGHBORHOOD_INSIGHTS__FREE_DATASET`
  - `SNOWFLAKE_SCHEMA=PUBLIC`

---

### Step 4: Verify Snowflake Access

- Log in to Snowflake web console
- Ensure the dataset exists:
  - `US_OPEN_CENSUS_DATA__NEIGHBORHOOD_INSIGHTS__FREE_DATASET`
- Ensure tables such as:
  - `2019_CBG_B01`
- If not available:
  - Add dataset from Snowflake Marketplace

---

### Step 5: Run Backend Server

- From project root, run:
  - `uvicorn app.api.main:app --reload`
- Expected output:
  - Server running at `http://127.0.0.1:8000`

---

### Step 6: Run Frontend

- Open a new terminal window
- Navigate to frontend folder:
  - `cd frontend`
- Start simple HTTP server:
  - `python -m http.server 8000`
- Open browser and go to:
  - `http://localhost:8000`

---

### Step 7: Test the Application

- Enter a query in the chat box:
  - `population of California`
  - `population of New York`
- Verify:
  - Response appears in UI
  - SQL query is generated
  - Data is returned

---

### Step 8: Troubleshooting

- Backend not starting:
  - Check virtual environment is activated
  - Check dependencies installed

- Snowflake query fails:
  - Verify credentials in `.env`
  - Check database and schema names
  - Ensure table exists

- Frontend not working:
  - Ensure backend is running
  - Ensure correct port (8000)
  - Check browser console for errors

- Same result for all queries:
  - Likely missing WHERE clause in SQL builder
  - Check geography parsing logic

---

### Step 9: Stop the Application

- Stop backend:
  - Press `Ctrl + C` in terminal
- Stop frontend:
  - Press `Ctrl + C` in frontend terminal

---

### Notes

- Always run backend before frontend
- Ports must match between frontend and backend
- Use port 8000 for both if possible
