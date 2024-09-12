# **Customer Segmentation Using RFM Model**

## Objective

The primary objective of this project is to build an RFM (Recency, Frequency, Monetary) model to segment customers based on their purchasing behavior. This segmentation helps identify customer groups such as high-value, loyal customers and low-engagement customers, providing valuable insights for targeted marketing and retention strategies.

## Methodology

I used the RFM model, which segments customers based on three key factors:
- **Recency (R)**: How recently a customer made a purchase.
- **Frequency (F)**: How often a customer makes purchases.
- **Monetary (M)**: How much money a customer spends.

### Data Exploration and Preprocessing
- **Dataset**: The dataset used for this project is an online retail dataset, containing transactional data of customers over a specific period.
  
- **Data Cleaning**: I removed any missing or invalid records and ensured that only complete transactions were considered. I also handled data types to make sure all the calculations were accurate.

- **Feature Engineering**: Created RFM scores for each customer by calculating:
  - **Recency**: Time difference between the most recent transaction and the reference date.
  - **Frequency**: Total number of transactions made by a customer.
  - **Monetary**: Total amount spent by a customer.

### Approach
- **RFM Scoring**: Customers were assigned RFM scores on a scale, allowing segmentation into distinct groups.
- **Visualization**: Visualized the customer segments based on the RFM scores using Plotly to better understand customer behavior.

### Tools Used
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For interactive visualizations of customer segments.
- **Excel**: For importing the dataset.

## Key Findings

The RFM analysis revealed three distinct customer segments:
1. **High-Value Customers**: These customers scored high on recency, frequency, and monetary, indicating frequent, recent, and high-spending behavior.
2. **Mid-Tier Customers**: Customers with moderate frequency and monetary value, but less recent activity.
3. **Low-Engagement Customers**: Customers with low scores across recency, frequency, and monetary value, representing those who haven’t made recent purchases and typically spend less.

These segments are crucial for crafting personalized marketing strategies. For example:
- **High-Value Customers** can be targeted with loyalty rewards and exclusive offers to maintain engagement.
- **Mid-Tier Customers** may benefit from engagement strategies like special promotions or targeted ads to increase their purchase frequency.
- **Low-Engagement Customers** require reactivation campaigns to encourage them to return and make purchases.

## Summary

In this project, I successfully applied the RFM model to segment customers based on their purchasing behavior. The analysis helped identify high-value, mid-tier, and low-engagement customer groups, offering actionable insights for marketing and retention strategies.

**Next Steps**:
1. Test the RFM model in a real-world marketing scenario.
2. Incorporate additional customer data, such as engagement with marketing channels, to refine the model.
3. Explore advanced techniques such as machine learning for automated customer segmentation.

## Links:
- [LinkedIn Profile](https://www.linkedin.com/in/erick-yegon-phd-4116961b4/)
- [Streamlit App](https://customer-segementation-rfm-model.streamlit.app/)

