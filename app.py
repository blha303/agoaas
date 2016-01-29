from flask import Flask, request, jsonify
from ago import human
from datetime import datetime, timedelta
app = Flask(__name__)

@app.route("/")
def agolookup():
    if request.args.get('ts') and request.args.get('strf'):
        try:
            if request.args.get('strf') == "%epoch":
                dt = datetime.fromtimestamp(float(request.args.get('ts')))
            else:
                dt = datetime.strptime(request.args.get('ts'), request.args.get('strf'))
            dt = dt - timedelta(hours=4) # gotta get get UTC
            resp = {'ago': human(dt), '_agoreq': request.args.get('ts'), '_agostrf': request.args.get('strf')}
            if request.args.get('strf_to'):
                resp['strf_to'] = dt.strftime(request.args.get('strf_to'))
            return jsonify(resp)
        except Exception as e:
            return jsonify({'error': "{}: {}".format(type(e).__name__, e.message)})
    return jsonify({'error': 'Needs ts and strf as get variables'})

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get( 
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

if __name__ == "__main__":
    app.run(port=7070)
