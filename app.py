from flask import Flask, render_template, redirect, url_for, request, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import users
from utils.data_handler import load_user_data, save_user_data
from utils.visualization import generate_pie_chart, generate_trend_analysis
import pandas as pd
import io
from fpdf import FPDF

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'username' not in session:
        return redirect(url_for('login'))
    date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = float(request.form['amount'])
    df = load_user_data(session['username'])
    df = df.append({'Date': date, 'Category': category, 'Description': description, 'Amount': amount}, ignore_index=True)
    save_user_data(session['username'], df)
    return redirect(url_for('index'))

@app.route('/pie_chart')
def pie_chart():
    if 'username' not in session:
        return redirect(url_for('login'))
    plot_url = generate_pie_chart(session['username'])
    return render_template('pie_chart.html', plot_url=plot_url)

@app.route('/trend_analysis')
def trend_analysis():
    if 'username' not in session:
        return redirect(url_for('login'))
    plot_url = generate_trend_analysis(session['username'])
    return render_template('trend_analysis.html', plot_url=plot_url)

@app.route('/export_report/<format>')
def export_report(format):
    if 'username' not in session:
        return redirect(url_for('login'))
    df = load_user_data(session['username'])
    if format == 'excel':
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Transactions')
        writer.save()
        output.seek(0)
        return send_file(output, attachment_filename='transactions.xlsx', as_attachment=True)

    elif format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Date']} {row['Category']} {row['Description']} ${row['Amount']}", ln=True)
        output = io.BytesIO()
        pdf.output(output)
        output.seek(0)
        return send_file(output, attachment_filename='transactions.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
