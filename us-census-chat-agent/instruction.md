\### instruction.md



\### How to Run the US Census Chat Agent



\#### Prerequisites

\- Python 3.9 or higher installed

\- A Snowflake account with access to the US Open Census dataset

\- An OpenAI API key

\- Internet connection



\---



\### Step 1: Clone the Repository

\- Open terminal or PowerShell

\- Run:

&#x20; - git clone <your-repo-url>

&#x20; - cd us-census-chat-agent



\---



\### Step 2: Setup Backend Environment

\- Navigate to backend folder:

&#x20; - cd backend

\- Create virtual environment:

&#x20; - python -m venv .venv

\- Activate virtual environment:

&#x20; - Windows: .venv\\Scripts\\activate

&#x20; - Mac/Linux: source .venv/bin/activate

\- Install dependencies:

&#x20; - pip install -r requirements.txt



\---



\### Step 3: Configure Environment Variables

\- Create a file named `.env` inside the backend folder

\- Add the following variables:

&#x20; - OPENAI\_API\_KEY=your\_openai\_key

&#x20; - OPENAI\_MODEL=gpt-4.1-mini

&#x20; - SNOWFLAKE\_USER=your\_user

&#x20; - SNOWFLAKE\_PASSWORD=your\_password

&#x20; - SNOWFLAKE\_ACCOUNT=your\_account

&#x20; - SNOWFLAKE\_WAREHOUSE=COMPUTE\_WH

&#x20; - SNOWFLAKE\_DATABASE=US\_OPEN\_CENSUS\_DATA\_\_NEIGHBORHOOD\_INSIGHTS\_\_FREE\_DATASET

&#x20; - SNOWFLAKE\_SCHEMA=PUBLIC



\---



\### Step 4: Verify Snowflake Access

\- Log in to Snowflake web console

\- Ensure the dataset exists:

&#x20; - US\_OPEN\_CENSUS\_DATA\_\_NEIGHBORHOOD\_INSIGHTS\_\_FREE\_DATASET

\- Ensure tables such as:

&#x20; - 2019\_CBG\_B01

\- If not available:

&#x20; - Add dataset from Snowflake Marketplace



\---



\### Step 5: Run Backend Server

\- From backend folder, run:

&#x20; - uvicorn app.api.main:app --reload

\- Expected output:

&#x20; - Server running at http://127.0.0.1:8000



\---



\### Step 6: Run Frontend

\- Open a new terminal window

\- Navigate to frontend folder:

&#x20; - cd frontend

\- Start simple HTTP server:

&#x20; - python -m http.server 8000

\- Open browser and go to:

&#x20; - http://localhost:8000



\---



\### Step 7: Test the Application

\- Enter a query in the chat box:

&#x20; - population of California

&#x20; - population of New York

\- Verify:

&#x20; - Response appears in UI

&#x20; - SQL query is generated

&#x20; - Data is returned



\---



\### Step 8: Troubleshooting



\- Backend not starting:

&#x20; - Check virtual environment is activated

&#x20; - Check dependencies installed



\- Snowflake query fails:

&#x20; - Verify credentials in `.env`

&#x20; - Check database and schema names

&#x20; - Ensure table exists



\- Frontend not working:

&#x20; - Ensure backend is running

&#x20; - Ensure correct port (8000)

&#x20; - Check browser console for errors



\- Same result for all queries:

&#x20; - Likely missing WHERE clause in SQL builder

&#x20; - Check geography parsing logic



\---



\### Step 9: Stop the Application

\- Stop backend:

&#x20; - Press Ctrl + C in terminal

\- Stop frontend:

&#x20; - Press Ctrl + C in frontend terminal



\---



\### Notes

\- Always run backend before frontend

\- Ports must match between frontend and backend

\- Use port 8000 for both if possible

