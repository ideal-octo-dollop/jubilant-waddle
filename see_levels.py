import sqlite3
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def display_levels():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Level")
    levels = cursor.fetchall()
    conn.close()

    html_template = '''
    <html>
    <head><title>Levels</title></head>
    <body>
        <h2>Level Table Contents</h2>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>Category</th>
                <th>Level ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Difficulty</th>
                <th>XP</th>
            </tr>
            {% for level in levels %}
            <tr>
                {% for field in level %}
                <td>{{ field }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, levels=levels)

if __name__ == '__main__':
    app.run(debug=True)
