from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        old_html = request.form.get('old_html')
        new_html = migrate_html(old_html)  # Call the migration function
        return render_template('migrate.html', old_html=old_html, new_html=new_html)
    return render_template('index.html')

def migrate_html(old_html):
    # Here you can implement your migration logic
    # For example, replacing certain tags or attributes
    new_html = old_html.replace('<old-tag>', '<new-tag>')  # Example transformation
    # Add more transformations as needed
    return new_html

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Change the port if necessary