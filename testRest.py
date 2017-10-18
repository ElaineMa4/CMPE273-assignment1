import sys
from io import StringIO
import contextlib
import rocksdb
import uuid
from flask import Flask, request, redirect, url_for, jsonify
app = Flask(__name__)

db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing=True))

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.route('/api/v1/scripts', methods=['POST'])
def uploadFile():			
	fileStorage = request.files['data']
	result = fileStorage.filename
	blob = fileStorage.read()
	length = len(blob)
	key = uuid.uuid4().hex
	tmp = key.encode()
	db.put(tmp, blob)
	return jsonify( { 'script-id': key} )


@app.route('/api/v1/scripts/<id>')
def execFile(id=None):
	tmp = id + ""
	tmp = tmp.encode()
	value = db.get(tmp)
	with stdoutIO() as s:
		exec(value)
	result = s.getvalue()
	return result

if __name__ == '__main__':
	app.run()

