from flask import Flask
from flask import request
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
    sorted_word_tuples = sorted(request.json.items(), key=operator.itemgetter(1))
    for word, num in sorted_word_tuples:
        bar_graph.add(word, num)
    try:
        bar_graph.render_to_png('test.png')
    except Exception as e:
        print e
    return 200


if __name__ == '__main__':
    app.run()
