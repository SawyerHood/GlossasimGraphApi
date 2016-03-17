from flask import Flask, request, send_file
import pygal
import operator
import base64
from hashlib import md5

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

def create_graph(data, graph_type='hbar', title=''):
    import pdb; pdb.set_trace()
    graph = None
    if graph_type == 'hbar':
        graph = pygal.HorizontalBar()
    graph.title = title
    sorted_value_tuples = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    data_hash = base64.urlsafe_b64encode(md5(str(sorted_value_tuples)).digest())
    for key, num in sorted_value_tuples:
        graph.add(key, num)
    filename = data_hash + '.png'
    graph.render_to_png(filename)
    return send_file(filename, mimetype='image/png')


@app.route('/trigger', methods=['POST'])
def trigger():
    return create_graph(request.json, 'hbar', 'Occurrences of Trigger Words')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
