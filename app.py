from flask import Flask, render_template, url_for, Response
from flask import request
import speedtest
import json

app = Flask(__name__)

def speed_test():
    servers = [3212, 6699]
    threads = None
    s = speedtest.Speedtest()

    try:
        s.get_servers(servers)
        
    except Exception as e:
        return json.dumps({'status': 'error', 'message': 'An error occured. Please, try later'}, separators=(',', ':'))
    
    s.get_best_server()
    s.download(threads = threads)
    s.upload(threads = threads)
    s.results.share()

    results_dict = s.results.dict()

    result = json.dumps({
            'status': 'success',
            'download': f"{results_dict['download'] / 1024 / 1024:.2f}", 
            'upload': f"{results_dict['upload'] / 1024 / 1024:.2f}", 
            'ping': f"{results_dict['ping']:.2f}"
        }, separators=(',', ':'))
    
    return result

@app.route("/")
def test_page():
    return render_template('test_page.html', site_title='Спит Тест')

@app.route("/api")
def api():
    return speed_test()

app.run(debug=True)