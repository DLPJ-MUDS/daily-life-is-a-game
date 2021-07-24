from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    html = render_template('index.html')
    return html

# /graph.html
@app.route('/graph.html')
def graph():
    html = render_template('graph.html')
    return html

if __name__ == "__main__":
    app.run()