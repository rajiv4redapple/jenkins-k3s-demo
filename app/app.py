from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🚀 Hello from k3s!</h1>
    <p>Deployed via Jenkins + ArgoCD GitOps Pipeline</p>
    <p>Version: 1.0</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
