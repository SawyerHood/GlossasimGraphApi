from flask import Flask, request, send_file
import pygal
import operator
import base64
from hashlib import md5

app = Flask(__name__)

@app.route('/')
def root():
    return 'Welcome to the GlossasimGraphApi!'

def sort_tuple_list(lst):
    return sorted(lst, key=operator.itemgetter(1), reverse=True)

def create_graph(data, graph_type='hbar', title=''):
    graph = None
    if graph_type == 'hbar':
        graph = pygal.HorizontalBar()
    elif graph_type == 'pie':
        graph = pygal.Pie()
    elif graph_type == 'gauge':
        graph = pygal.Gauge()
        graph.range = [100,200]
    elif graph_type == 'line':
        graph = pygal.Line()

    graph.title = title
    data_hash = base64.urlsafe_b64encode(md5(str(data)).digest())

    if graph_type == 'line':
        graph.add('dB over time', data)
    else:
        for key, num in data:
            graph.add(key, num)

    filename = data_hash + '.png'
    graph.render_to_png(filename)
    return send_file(filename, mimetype='image/png')

@app.route('/trigger', methods=['POST'])
def trigger():
    return create_graph(sort_tuple_list(request.json.items()), 'hbar', 'Occurrences of Trigger Words')
    
@app.route('/body_language', methods=['POST'])
def body_language():
    return create_graph(sort_tuple_list(request.json.items()), 'pie', 'Body Language Inference')

@app.route('/wpm', methods=['POST'])
def wpm():
    return create_graph(request.json.items(), 'gauge', 'WPM of you compared to famous speakers.')

@app.route('/db', methods=['POST'])
def db():
    return create_graph(request.json, 'line', 'Volume of presentation over time.')

@app.route('/eyeline', methods=['POST'])
def eyeline():
    return create_graph(sort_tuple_list(request.json.items()), 'pie', 'Time spent looking at parts of the room')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
