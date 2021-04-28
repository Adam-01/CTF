from flask import Flask, request, render_template_string, render_template 
from subprocess import getoutput as shell 

app = Flask(__name__) 
shell('echo $FLAG > flag') 
@app.route('/', methods=['GET', 'POST']) 

def hello_world(): 
    if request.method == "GET": 
        content = request.args.get('flag') 
        if content is not None and len(content) >= 1: 
            html = '''%s''' % content 
            return render_template_string(html) 
        else: 
            return render_template('index.html', html="You need pass in a parameter named flag") 
    else: 
        return "Method Not Allowed!" 

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=80,debug=True) 