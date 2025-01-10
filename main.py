from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
from dotenv import load_dotenv
from astrapy import DataAPIClient
import pandas as pd
import os

# Load environment variables
load_dotenv()

# Astra DB Configuration from .env
DB_API_ENDPOINT = os.getenv("DB_API_ENDPOINT")
APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
TABLE_NAME = os.getenv("TABLE_NAME")

# Initialize the client
client = DataAPIClient(APPLICATION_TOKEN)
db = client.get_database_by_api_endpoint(DB_API_ENDPOINT)
collection = db.get_collection(TABLE_NAME)

app = Flask(__name__)
CORS(app, origins=['*'])

BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "Text input is required"}), 400

    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
        payload = {
            "input_value": text,
            "output_type": "chat",
            "input_type": "chat",
        }
        headers = {
            "Authorization": "Bearer " + APPLICATION_TOKEN,
            "Content-Type": "application/json",
        }
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_data():
    documents = collection.find({}, projection={"$vectorize": 1, "likes": 1, "comments": 1, "shares": 1, "views": 1,
                                                "clicks": 1, "impressions": 1})
    return list(documents)

def calculate_engagement(data):
    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0)
    df["comments"] = pd.to_numeric(df["comments"], errors="coerce").fillna(0)
    df["shares"] = pd.to_numeric(df["shares"], errors="coerce").fillna(0)
    df["views"] = pd.to_numeric(df["views"], errors="coerce").fillna(0)
    df["clicks"] = pd.to_numeric(df["clicks"], errors="coerce").fillna(0)
    df["impressions"] = pd.to_numeric(df["impressions"], errors="coerce").fillna(0)

    df["engagement"] = df["likes"] + df["comments"]
    df["total_reach"] = df["shares"] + df["views"] + df["clicks"] + df["impressions"]
    grouped_df = df.groupby("$vectorize").agg(
        total_engagement=("engagement", "sum"),
        total_posts=("$vectorize", "count"),
        total_reach=("total_reach", "sum")
    )
    grouped_df["average_engagement"] = grouped_df["total_engagement"] / grouped_df["total_posts"]
    total_engagement_all = grouped_df["total_engagement"].sum()
    grouped_df["engagement_percentage"] = (grouped_df["total_engagement"] / total_engagement_all) * 100
    return grouped_df

@app.route("/performance", methods=["GET"])
def get_engagement():
    data = fetch_data()
    engagement_stats = calculate_engagement(data)
    final_output = []
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    for i, (index, row) in enumerate(engagement_stats.iterrows()):
        prev_index = i - 1 if i > 0 else None
        prev_row = engagement_stats.iloc[prev_index] if prev_index is not None else None
        final_output.append({
            "name": days_of_week[i % len(days_of_week)],
            "engagement": row["total_engagement"],
            "impressions": row["total_reach"],
            "reach": row["total_reach"],
            "prevEngagement": prev_row["total_engagement"] if prev_row is not None else None,
            "prevImpressions": prev_row["total_reach"] if prev_row is not None else None,
            "prevReach": prev_row["total_reach"] if prev_row is not None else None
        })
    return jsonify(final_output)

@app.route("/engagement", methods=["GET"])
def get_engagement2():
    try:
        # Fetch data from Astra DB
        collection = db.get_collection(TABLE_NAME)
        documents = collection.find({}, projection={"$vectorize": 1, "likes": 1, "comments": 1, "shares": 1, "views": 1,
                                                    "clicks": 1, "impressions": 1})

        all_data = [doc for doc in documents]

        # Convert data to DataFrame
        df = pd.DataFrame(all_data)

        # Ensure numeric values
        for col in ["likes", "comments", "shares", "views", "clicks", "impressions"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Compute engagement metrics
        df["engagement"] = df["likes"] + df["comments"]
        df["total_reach"] = df["shares"] + df["views"] + df["clicks"] + df["impressions"]

        grouped_df = df.groupby("$vectorize").agg(
            total_engagement=("engagement", "sum"),
            total_posts=("$vectorize", "count"),
            total_reach=("total_reach", "sum")
        )
        grouped_df["average_engagement"] = grouped_df["total_engagement"] / grouped_df["total_posts"]
        total_engagement_all = grouped_df["total_engagement"].sum()
        grouped_df["engagement_percentage"] = (grouped_df["total_engagement"] / total_engagement_all) * 100

        return jsonify(grouped_df.reset_index().to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)