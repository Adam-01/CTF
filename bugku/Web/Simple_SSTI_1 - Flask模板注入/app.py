from flask import Flask, request, render_template_string, render_template 
from subprocess import getoutput as shell 

app = Flask(__name__) 
flag = shell('echo $FLAG') 
app.config['SECRET_KEY'] = flag 
@app.route('/', methods=['GET', "POST"]) 
def index(): 
    if request.method == "GET": 
        content = request.args.get('flag') 
        if content is not None and len(content) >= 1: 
            html = '''%s''' % content 
            return render_template_string(html) 
        else: 
            html = """You need pass in a parameter named flag。""" 
        return render_template('index.html', html=html) 

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=80, debug=True) 