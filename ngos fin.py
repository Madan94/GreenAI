import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Example project data with ESG scores and ROI
# Investment already in INR (₹)
data = {
    'Project': ['TIST Program', 'City Forest Credits', 'Arbor Day Foundation', 'Trees Forever'],
    'ESG_Score': [85, 80, 90, 88],  # ESG score out of 100
    'ROI': [0.50, 0.40, 0.60, 0.55],  # ROI as a percentage (12.5%, 10.8%, etc.)
    'Investment_INR': [857665, 2144162, 1286497, 1715330],  # Investment in INR
}

# Convert investment to crore rupees
data['Investment_Crore'] = [inv / 1e7 for inv in data['Investment_INR']]

# Create DataFrame
df = pd.DataFrame(data)

# Rank projects based on ESG score and ROI (weighted sum)
df['Rank_Score'] = df['ESG_Score'] * 0.6 + df['ROI'] * 0.4  # Adjust weights as necessary
df = df.sort_values(by='Rank_Score', ascending=False)

# Scenario analysis function to adjust ESG and ROI weights
def scenario_analysis(df, esg_weight, roi_weight):
    df['Scenario_Score'] = df['ESG_Score'] * esg_weight + df['ROI'] * roi_weight
    return df.sort_values(by='Scenario_Score', ascending=False)

# Scenario with 70% weight on ESG and 30% on ROI
df_scenario = scenario_analysis(df, esg_weight=0.7, roi_weight=0.3)

# Fetch recommended investment (first-ranked project)
recommended_project = df.iloc[0]

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Create a grid of 2x2 subplots

# 1. Bar chart for project rankings based on scenario analysis
axs[0, 0].bar(df_scenario['Project'], df_scenario['Scenario_Score'], color='blue')
axs[0, 0].set_title('Project Rankings (70% ESG, 30% ROI)')
axs[0, 0].set_xlabel('Projects')
axs[0, 0].set_ylabel('Scenario Score')
axs[0, 0].tick_params(axis='x', rotation=45)

# 2. Scatter plot of ESG Score vs ROI
axs[0, 1].scatter(df['ESG_Score'], df['ROI'], color='green', s=100, label='Projects')
for i, project in enumerate(df['Project']):
    axs[0, 1].text(df['ESG_Score'].iloc[i], df['ROI'].iloc[i], project, fontsize=9)
axs[0, 1].set_title('ESG Score vs ROI of Projects')
axs[0, 1].set_xlabel('ESG Score')
axs[0, 1].set_ylabel('ROI')
axs[0, 1].grid(True)

# Updated Venn Diagram Code
# Categorize projects
set_environment = set(df[df['ESG_Score'] > 85]['Project'])  # High ESG Score
set_social = set(df[df['ROI'] > 0.12]['Project'])  # High ROI
set_governance = set(df[df['Investment_Crore'] < 3000]['Project'])  # Low Investment

# Calculate overlaps
env_only = len(set_environment - set_social - set_governance)
soc_only = len(set_social - set_environment - set_governance)
gov_only = len(set_governance - set_environment - set_social)
env_soc = len(set_environment & set_social - set_governance)
env_gov = len(set_environment & set_governance - set_social)
soc_gov = len(set_social & set_governance - set_environment)
all_three = len(set_environment & set_social & set_governance)

# Create Venn Diagram as a subplot
axs[1, 0].set_xlim(0, 1)
axs[1, 0].set_ylim(0, 1)

# Draw circles
circle_env = plt.Circle((0.4, 0.6), 0.3, color='lightblue', alpha=0.5, label='Environment')
circle_soc = plt.Circle((0.6, 0.6), 0.3, color='lightgreen', alpha=0.5, label='Social')
circle_gov = plt.Circle((0.5, 0.4), 0.3, color='lightcoral', alpha=0.5, label='Governance')

# Add circles to plot
axs[1, 0].add_artist(circle_env)
axs[1, 0].add_artist(circle_soc)
axs[1, 0].add_artist(circle_gov)

# Add text for counts
axs[1, 0].text(0.35, 0.7, f'Env Only\n{env_only}', ha='center', fontsize=10)
axs[1, 0].text(0.65, 0.7, f'Soc Only\n{soc_only}', ha='center', fontsize=10)
axs[1, 0].text(0.5, 0.3, f'Gov Only\n{gov_only}', ha='center', fontsize=10)
axs[1, 0].text(0.5, 0.7, f'Env + Soc\n{env_soc}', ha='center', fontsize=10)
axs[1, 0].text(0.4, 0.5, f'Env + Gov\n{env_gov}', ha='center', fontsize=10)
axs[1, 0].text(0.6, 0.5, f'Soc + Gov\n{soc_gov}', ha='center', fontsize=10)
axs[1, 0].text(0.5, 0.6, f'All Three\n{all_three}', ha='center', fontsize=12, fontweight='bold')

# Add Recommended Investment information under the Venn diagram
recommended_text = (
    f"Recommended Investment:\n"
    f"Project: {recommended_project['Project']}\n"
    f"ESG Score: {recommended_project['ESG_Score']}\n"
    f"Investment: ₹{recommended_project['Investment_Crore']:,.2f} Cr"
)
axs[1, 0].text(0.5, -0.2, recommended_text, transform=axs[1, 0].transAxes,
               fontsize=12, ha='center', bbox=dict(facecolor='lightgrey', alpha=0.5))

# Set title and hide axes for Venn diagram
axs[1, 0].set_title('Custom Venn Diagram for ESG Categories')
axs[1, 0].axis('off')

# 4. Project Ranking bar chart (default rank based on ESG and ROI)
axs[1, 1].bar(df['Project'], df['Rank_Score'], color='skyblue')
axs[1, 1].set_title('Project Rankings (ESG + ROI)')
axs[1, 1].set_xlabel('Projects')
axs[1, 1].set_ylabel('Rank Score')
axs[1, 1].tick_params(axis='x', rotation=45)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
