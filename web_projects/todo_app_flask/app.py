from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

todos = []

INDEX_HTML = """
<!doctype html>
<title>Todo App</title>
<h1>Todo List</h1>
<form method=post action="/add">
  <input name=item placeholder="New item">
  <input type=submit value=Add>
</form>
<ul>
{% for t in todos %}<li>{{t}}</li>{% endfor %}
</ul>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    item = request.form.get('item')
    if item:
        todos.append(item)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
