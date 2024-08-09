import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from utils.data_handler import load_user_data

def generate_pie_chart(username):
    df = load_user_data(username)
    pie_data = df.groupby('Category')['Amount'].sum()
    img = BytesIO()
    pie_data.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Spending Distribution by Category')
    plt.ylabel('')  # Remove y-label for better appearance
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def generate_trend_analysis(username):
    df = load_user_data(username)
    df['Date'] = pd.to_datetime(df['Date'])
    trend_data = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    img = BytesIO()
    trend_data.plot(kind='line')
    plt.title('Monthly Spending Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Spending')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()
