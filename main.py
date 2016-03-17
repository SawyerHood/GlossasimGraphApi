from flask import Flask, request, send_file
import pygal
import operator

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/trigger', methods=['POST'])
def trigger():
    bar_graph = pygal.HorizontalBar()
    bar_graph.title = 'Occurance of trigger words'
    sorted_word_tuples = sorted(request.json.items(), key=operator.itemgetter(1), reverse=True)
    for word, num in sorted_word_tuples:
        bar_graph.add(word, num)
    bar_graph.render_to_png('test.png')
    return send_file('test.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
