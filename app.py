import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# Set page configuration
st.set_page_config(page_title="RFM Analysis Dashboard", layout="wide")

# Custom color palette
colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'background': '#f0f2f6',
    'text': '#2c3e50',
    'accent1': '#2ca02c',
    'accent2': '#d62728',
    'accent3': '#9467bd'
}

# ASCII Art Banner
banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ███████╗███╗   ███╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗    ║
║   ██╔══██╗██╔════╝████╗ ████║    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝    ║
║   ██████╔╝█████╗  ██╔████╔██║    ███████║██╔██╗ ██║███████║██║   ╚████╔╝     ║
║   ██╔══██╗██╔══╝  ██║╚██╔╝██║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝      ║
║   ██║  ██║██║     ██║ ╚═╝ ██║    ██║  ██║██║ ╚████║██║  ██║███████╗██║       ║
║   ╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝       ║
║                                                                              ║
║   Customer Segmentation Dashboard                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Display the banner
st.text(banner)

# Custom CSS to improve the look and feel
st.markdown(f"""
<style>
    .reportview-container {{
        background: {colors['background']};
    }}
    .main {{
        background: white;
        padding: 3rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    h1, h2, h3 {{
        color: {colors['primary']};
    }}
    p {{
        color: {colors['text']};
    }}
    .stButton>button {{
        color: white;
        background-color: {colors['primary']};
        border-radius: 5px;
    }}
    .stButton>button:hover {{
        background-color: {colors['secondary']};
    }}
    pre {{
        background-color: {colors['background']};
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 10px;
        white-space: pre-wrap;
        word-wrap: break-word;
    }}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("RFM Analysis Dashboard")
st.write("""
This dashboard presents a comprehensive customer segmentation analysis based on RFM (Recency, Frequency, Monetary) metrics. RFM analysis is a powerful marketing technique used to understand and segment customers based on their purchasing behavior.

**How to use this dashboard:**

1. **Overview**: Start by examining the average RFM metrics and customer segment distribution at the top of the page.
2. **Visualizations**: Explore the various charts and graphs to gain insights into customer behavior and segmentation.
3. **Top Customers**: Check the table of top 10 customers based on their RFM scores.
4. **Customer Lookup**: Use the interactive tool at the bottom to look up individual customer details.

The insights gained from this analysis can help in tailoring marketing strategies, improving customer retention, and maximizing customer lifetime value.
""")

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_excel('data/Online Retail.xlsx')
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['TotalAmount'] = data['Quantity'] * data['UnitPrice']
    data.dropna(inplace=True)
    return data

# Load data
data = load_data()

# Sidebar for data overview
st.sidebar.header("Data Overview")
st.sidebar.write(f"Total Records: {len(data):,}")
st.sidebar.write(f"Date Range: {data['InvoiceDate'].min().date()} to {data['InvoiceDate'].max().date()}")

# RFM Calculation
@st.cache_data
def calculate_rfm(data):
    reference_date = data['InvoiceDate'].max() + timedelta(days=1)
    rfm = data.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'count',
        'TotalAmount': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    rfm['Monetary'] = pd.to_numeric(rfm['Monetary'], errors='coerce').abs()
    return rfm

rfm = calculate_rfm(data)

# RFM Scoring function
def rfm_score(x, p, d):
    if p == 'Recency':
        if x <= d[p][0.25]:
            return 4
        elif x <= d[p][0.50]:
            return 3
        elif x <= d[p][0.75]:
            return 2
        else:
            return 1
    else:
        if x <= d[p][0.25]:
            return 1
        elif x <= d[p][0.50]:
            return 2
        elif x <= d[p][0.75]:
            return 3
        else:
            return 4

# Calculate RFM Scores
quantiles = rfm.quantile(q=[0.25, 0.5, 0.75])
rfm['R'] = rfm['Recency'].apply(rfm_score, args=('Recency', quantiles))
rfm['F'] = rfm['Frequency'].apply(rfm_score, args=('Frequency', quantiles))
rfm['M'] = rfm['Monetary'].apply(rfm_score, args=('Monetary', quantiles))

rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

# Customer Segmentation
def segment_customers(row):
    if row['RFM_Score'] in ['444', '434', '443', '433']:
        return 'Best Customers'
    elif row['RFM_Score'] in ['441', '442', '432', '423', '424']:
        return 'Loyal Customers'
    elif row['RFM_Score'] in ['311', '422', '421', '412', '411']:
        return 'Lost Customers'
    elif row['RFM_Score'] in ['211', '212', '221']:
        return "Lost Cheap Customers"
    else:
        return 'Other'

rfm['Customer_Segment'] = rfm.apply(segment_customers, axis=1)

# Main content
st.header("RFM Analysis Results")

# Display RFM metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg. Recency (days)", f"{rfm['Recency'].mean():.0f}")
with col2:
    st.metric("Avg. Frequency", f"{rfm['Frequency'].mean():.1f}")
with col3:
    st.metric("Avg. Monetary Value", f"${rfm['Monetary'].mean():.2f}")

# Customer Segments Distribution
st.subheader("Customer Segments Distribution")
segment_counts = rfm['Customer_Segment'].value_counts()
fig_segments = px.pie(
    values=segment_counts.values, 
    names=segment_counts.index, 
    title="Customer Segments",
    color_discrete_sequence=[colors['primary'], colors['secondary'], colors['accent1'], colors['accent2'], colors['accent3']]
)
st.plotly_chart(fig_segments, use_container_width=True)

# RFM Score Distribution
st.subheader("RFM Score Distribution")
fig_rfm_dist = px.histogram(
    rfm, 
    x='RFM_Score', 
    title="RFM Score Distribution",
    color_discrete_sequence=[colors['primary']]
)
st.plotly_chart(fig_rfm_dist, use_container_width=True)

# Recency vs Frequency Plot
st.subheader("Recency vs Frequency")
fig_recency_frequency = px.scatter(
    rfm, 
    x='Recency', 
    y='Frequency', 
    color='Monetary', 
    size=rfm['Monetary'].abs(),
    hover_data=['CustomerID'],
    title="Recency vs Frequency (Size and Color: Monetary Value)",
    color_continuous_scale=px.colors.sequential.Viridis
)
st.plotly_chart(fig_recency_frequency, use_container_width=True)

# Top Customers Table
st.subheader("Top 10 Customers")
top_customers = rfm.sort_values('RFM_Score', ascending=False).head(10)
st.table(top_customers[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Customer_Segment']])

# Correlation Heatmap
st.subheader("RFM Correlation Heatmap")
corr_matrix = rfm[['Recency', 'Frequency', 'Monetary']].corr()
fig_heatmap = go.Figure(data=go.Heatmap(
                   z=corr_matrix.values,
                   x=corr_matrix.columns,
                   y=corr_matrix.columns,
                   colorscale='RdBu'))
fig_heatmap.update_layout(title="Correlation between RFM Metrics")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Segment Comparison
st.subheader("Segment Comparison")
segment_comparison = rfm.groupby('Customer_Segment')[['Recency', 'Frequency', 'Monetary']].mean()
fig_comparison = go.Figure()
for metric in ['Recency', 'Frequency', 'Monetary']:
    fig_comparison.add_trace(go.Bar(x=segment_comparison.index, y=segment_comparison[metric], name=metric))
fig_comparison.update_layout(barmode='group', title="Average RFM Values by Segment")
st.plotly_chart(fig_comparison, use_container_width=True)

# Conclusion
st.header("Conclusion and Recommendations")
st.write("""
Based on the RFM analysis, we can draw the following conclusions:

1. The 'Best Customers' segment represents our most valuable customers. They have high recency, frequency, and monetary values.
2. 'Loyal Customers' are frequent buyers but may not have purchased recently. They should be targeted for re-engagement.
3. 'Lost Customers' haven't purchased in a while. Consider running a win-back campaign for this group.
4. 'Lost Cheap Customers' are not only inactive but also have low monetary value. They might not be worth extensive marketing efforts.

Recommendations:
- Focus on retaining 'Best Customers' through personalized offers and exclusive benefits.
- Create targeted campaigns to re-engage 'Loyal Customers' and prevent them from becoming inactive.
- Analyze the reasons for customer churn in the 'Lost Customers' segment and develop strategies to win them back.
- Continuously monitor customer movement between segments to identify trends and adjust strategies accordingly.
""")

# Interactive Customer Lookup
st.header("Customer Lookup")
customer_id = st.number_input("Enter Customer ID", min_value=int(rfm['CustomerID'].min()), max_value=int(rfm['CustomerID'].max()))
if st.button("Look Up Customer"):
    customer_data = rfm.loc[rfm['CustomerID'] == customer_id].squeeze()
    st.write(f"Customer ID: {customer_id}")
    st.write(f"Recency: {customer_data['Recency']} days")
    st.write(f"Frequency: {customer_data['Frequency']} purchases")
    st.write(f"Monetary Value: ${customer_data['Monetary']:.2f}")
    st.write(f"RFM Score: {customer_data['RFM_Score']}")
    st.write(f"Customer Segment: {customer_data['Customer_Segment']}")

# Footer
st.markdown("---")
st.markdown("RFM Analysis Dashboard | Created with Streamlit by Dr. Erick Kiprotich Yegon")