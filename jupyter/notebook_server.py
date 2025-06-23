from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/run-notebook', methods=['POST'])
def run():
    result = subprocess.run(
        ["papermill", "work/batch.ipynb", "work/output_batch.ipynb"],
        capture_output=True
    )
    return result.stdout.decode() + "\n\n" + result.stderr.decode(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
