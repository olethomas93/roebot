from flask import Flask, render_template, Response
from ImageProcessing import camera2
import pdb
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera2):
    while True:
        frame = camera2.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='10.0.0.36', debug=True)