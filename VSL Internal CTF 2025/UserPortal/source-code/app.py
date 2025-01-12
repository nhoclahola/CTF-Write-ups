from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
from jinja2.sandbox import SandboxedEnvironment
import functools
from urllib import parse as urls
import datetime
from dateutil import relativedelta
from jinja2 import Undefined

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'users.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


def initialize_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()


initialize_db()


class NoSelfUndefined(Undefined):
    def __getattr__(self, name):
        if name == 'self':
            raise AttributeError("Access to 'self' is not allowed.")
        return super()._getattr(name)

    def __getitem__(self, key):
        if key == 'self':
            raise AttributeError("Access to 'self' is not allowed.")
        return super()._getitem__(key)


SAFE_GLOBALS = {
    'str': str,
    'quote': urls.quote,
    'urlencode': urls.urlencode,
    'datetime': datetime,
    'len': len,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'filter': filter,
    'reduce': functools.reduce,
    'map': map,
    'round': round,
    'relativedelta': lambda *a, **kw: relativedelta.relativedelta(*a, **kw),
}
SAFE_FILTERS = {
    'lower': str.lower,
    'upper': str.upper,
    'capitalize': str.capitalize,
    'title': str.title,
    'safe': lambda x: x,
}

jinja_env = SandboxedEnvironment(
    block_start_string="<%",
    block_end_string="%>",
    variable_start_string="{{",
    variable_end_string="}}",
    comment_start_string="<%doc>",
    comment_end_string="</%doc>",
    line_statement_prefix="%",
    line_comment_prefix="##",
    trim_blocks=True,
    autoescape=True,
    undefined=NoSelfUndefined,
)
jinja_env.globals.clear()
jinja_env.globals.update(SAFE_GLOBALS)
jinja_env.filters.clear()
jinja_env.filters.update(SAFE_FILTERS)
jinja_env.enable_async = False


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        cursor = conn.cursor()
        query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT username, email FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', username=user[0] if user else 'Unknown', email=user[1] if user else 'Unknown')


@app.route('/send_email', methods=['GET', 'POST'])
def send_email_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    preview = None
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        body = request.form.get('body')
        action = request.form.get('action')
        if action == 'preview':
            try:
                context = {
                    'user': 'admin',
                    'object': {'id': 1, 'name': 'Test Object'},
                    'ctx': session,
                    'datetime': datetime
                }
                template = jinja_env.from_string(body)
                preview = template.render(**context)
                flash('Email preview generated.', 'info')
            except Exception as e:
                flash(f'Failed to render preview: {e}', 'danger')
        elif action == 'send':
            try:
                context = {
                    'user': 'admin',
                    'object': {'id': 1, 'name': 'Test Object'},
                    'ctx': session,
                    'datetime': datetime
                }
                template = jinja_env.from_string(body)
                email_body = template.render(**context)
                flash(
                    f'Email Sent:<br><strong>Subject:</strong> {subject}<br><strong>To:</strong> {recipient}<br><strong>Body:</strong><br>{email_body}', 'success')
            except Exception as e:
                flash(f'Failed to send email: {e}', 'danger')

        return render_template('send_email.html', preview=preview, recipient=recipient, subject=subject, body=body)
    return render_template('send_email.html', preview=preview)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1005)
