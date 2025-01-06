from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

# Example project data
data = {
    'Project': ['TIST Program', 'City Forest Credits', 'Arbor Day Foundation', 'Trees Forever'],
    'ESG_Score': [85, 80, 90, 88],
    'ROI': [0.50, 0.40, 0.60, 0.55],
    'Investment_INR': [857665, 2144162, 1286497, 1715330],
}

# Prepare data
data['Investment_Crore'] = [inv / 1e7 for inv in data['Investment_INR']]
df = pd.DataFrame(data)
df['Rank_Score'] = df['ESG_Score'] * 0.6 + df['ROI'] * 0.4
df = df.sort_values(by='Rank_Score', ascending=False)

# Route to send all data to HTML
@app.route("/")
def index():
    top_project = df.iloc[0]  # Top-ranked project
    all_projects = df.to_dict(orient="records")  # All projects as a list of dictionaries

    print("Top Project:", top_project.to_dict())
    print("All Projects:", all_projects)

    return render_template(
        "index.html",
        top_project=top_project.to_dict(),
        all_projects=all_projects
    )

# Route to generate chart and return it as a base64 image
@app.route("/chart")
def chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['Project'], df['Rank_Score'], color='skyblue')
    ax.set_title("Project Rankings (ESG + ROI)")
    ax.set_xlabel("Projects")
    ax.set_ylabel("Rank Score")

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)
    
    return f"<img src='data:image/png;base64,{plot_url}'/>"

if __name__ == "__main__":
    app.run(debug=True)
