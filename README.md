# Social Track Backend

The **Social Track Backend** is the server-side component of the Social Track project. It processes social media engagement data, handles database operations, and integrates AI-driven insights using Langflow. Built with **Flask** and **DataStax Astra DB**, it is designed to provide a scalable and efficient solution for social media performance analysis.

## Features

- **Data Management**: Efficiently stores and retrieves social media engagement data using Astra DB.
- **AI-Powered Insights**: Uses Langflow for generating GPT-based insights based on social media performance.
- **API Endpoints**: Exposes several APIs for interaction with the frontend and data processing.
- **Scalable Architecture**: Built to handle large datasets and high query volumes.

## Technologies Used

- **Flask**: Lightweight web framework for Python.
- **DataStax Astra DB**: Cloud-native database for managing social media engagement data.
- **Langflow**: Tool for creating workflows to integrate GPT-based AI insights.
- **Python**: Core programming language for backend development.

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Virtual environment tools (e.g., `venv` or `virtualenv`)
- Astra DB account

### Steps

1. **Clone the Repository**:

```bash
git clone https://github.com/SagarBhoi404/social-track-backend.git
cd social-track-backend
```

2. **Set Up a Virtual Environment**:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```


4. **Add Environment Variables**:

Create and add variables in `.env` file, set the following environment variables:

```bash
ASTRA_DB_ID=<your-database-id>
ASTRA_DB_REGION=<your-region>
ASTRA_DB_KEYSPACE=<your-keyspace>
ASTRA_DB_APPLICATION_TOKEN=<your-application-token>
TABLE_NAME=<your-table-name>
DB_API_ENDPOINT=<your-db-api-endpoint>
```

6. **Run the Application**:

```bash
flask run
```

The backend will be running at `http://localhost:5000` by default.


## API Endpoints

### 1. Fetch Engagement Data
- **Endpoint**: `/api/engagement`
- **Method**: `GET`
- **Description**: Retrieves social media engagement data from Astra DB.

### 2. Analyze Post Performance
- **Endpoint**: `/api/performance`
- **Method**: `POST`
- **Description**: Returns performance metrics.

### 3. Generate AI Insights
- **Endpoint**: `/api/analyze`
- **Method**: `POST`
- **Parameter**: `text`
- **Description**: Uses Langflow and GPT integration to generate AI-driven insights.

## Frontend GitHub Repository

The frontend code for the Social Track project can be found at the following GitHub repository:  
[https://github.com/SagarBhoi404/social-track-frontend](https://github.com/SagarBhoi404/social-track-frontend)

## Screenshots
- **Langflow Structure**

- **Astra Database Structure**