from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the HTML code from the form
        html_code = request.form.get('html_code')
        return render_template('test.html', html_code=html_code)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change the port to 5001