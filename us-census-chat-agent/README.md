\### US Census Chat Agent



An interactive chat-based web application that answers natural language questions about US population data using the Snowflake US Open Census dataset.

\---



\### Features



\- Natural language → SQL query generation  

\- Live querying from Snowflake Marketplace dataset  

\- Chat-style web interface (frontend + backend)  

\- Metric-based query understanding (population, income, etc.)  

\- Transparent responses:

&#x20; - Generated SQL  

&#x20; - Query results  

&#x20; - Debug notes  



\### File Structure



```text

us-census-chat-agent/

├─ app/

│  ├─ api/

│  │  ├─ main.py

│  │  ├─ routes.py

│  │  ├─ schemas.py

│  │  └─ deps.py

│  ├─ core/

│  │  ├─ config.py

│  │  ├─ guardrails.py

│  │  ├─ logging.py

│  │  └─ memory.py

│  ├─ llm/

│  │  ├─ intent\_parser.py

│  │  ├─ answer\_generator.py

│  │  └─ prompts.py

│  ├─ data/

│  │  ├─ snowflake\_client.py

│  │  ├─ sql\_builder.py

│  │  ├─ metric\_catalog.py

│  │  └─ geography\_catalog.py

│  └─ services/

│     └─ chat\_service.py

├─ frontend/

│  ├─ index.html

│  ├─ app.js

│  └─ style.css

├─ tests/

│  ├─ test\_guardrails.py

│  ├─ test\_sql\_builder.py

│  ├─ test\_intent\_parser.py

│  └─ test\_chat\_api.py

├─ .env.example

├─ requirements.txt

├─ README.md

├─ instruction.md

└─ reflection.md



\### File Descriptions



\*\*API Layer\*\*

\- `main.py` → Entry point that initializes the FastAPI application and starts the server  

\- `routes.py` → Defines API endpoints for handling chat requests and responses  

\- `schemas.py` → Contains request and response data models for API validation  

\- `deps.py` → Manages shared dependencies such as services and configurations  



\*\*Core Utilities\*\*

\- `config.py` → Loads environment variables and application configuration settings  

\- `guardrails.py` → Applies validation and safety checks to user inputs and outputs  

\- `logging.py` → Configures structured logging for debugging and monitoring  

\- `memory.py` → Handles session-based memory for maintaining conversation context  



\*\*LLM Layer\*\*

\- `intent\_parser.py` → Extracts user intent and relevant parameters from natural language queries  

\- `answer\_generator.py` → Generates natural language responses from query results  

\- `prompts.py` → Stores prompt templates used for LLM interactions  



\*\*Data Layer\*\*

\- `snowflake\_client.py` → Manages connection and query execution with Snowflake  

\- `sql\_builder.py` → Converts parsed user intent into executable SQL queries  

\- `metric\_catalog.py` → Maps user-friendly metrics (e.g., population) to dataset columns  

\- `geography\_catalog.py` → Maps geographic entities (state, county, etc.) to query filters  



\*\*Service Layer\*\*

\- `chat\_service.py` → Orchestrates the full pipeline from user query → SQL → response  



\*\*Frontend\*\*

\- `index.html` → Provides the web-based chat interface layout  

\- `app.js` → Handles user input and communicates with the backend API  

\- `style.css` → Defines the styling and layout of the frontend UI  



\*\*Testing\*\*

\- `test\_guardrails.py` → Tests input validation and safety mechanisms  

\- `test\_sql\_builder.py` → Verifies correctness of SQL generation logic  

\- `test\_intent\_parser.py` → Tests accuracy of intent extraction from user queries  

\- `test\_chat\_api.py` → Tests end-to-end API behavior  



\*\*Root Files\*\*

\- `.env.example` → Template for required environment variables  

\- `requirements.txt` → Lists all Python dependencies for the project  

\- `README.md` → Provides project overview, setup, and usage instructions  

\- `instruction.md` → Explains how to run the project locally  

\- `reflection.md` → Analyzes strengths and limitations of the chatbot  

