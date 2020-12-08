from flask import Flask,redirect, url_for,render_template,request
import os
import index
from index import d_dtcn

secret_key = str(os.urandom(24))

app = Flask(__name__)
app.config['TESTING'] = True
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = True

# Defining the home page of our site
@app.route("/",methods=['GET', 'POST'])
def home():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Continue') == 'Continue':
           return render_template("test1.html")
    else:
        # pass # unknown
        return render_template("index.html")

@app.route("/analyze",methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        fip = request.form['service']
        sip = request.form['CF']
        tip = request.form['UMI']
        foip=request.form['ASC']
        fifip=request.form['FP']
        index.create_resource(ti1=sip,v=fip,inac1=tip,asleep1=foip,fold=fifip)
        return render_template("index.html")
    
@app.route('/test1', methods=['GET', 'POST'])
def test1():
    return render_template("test1.html")
    
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html")
    #print(request.method)
    #if request.method == 'POST':
        #if request.form.get('Start') == 'Start':
            # pass
            #d_dtcn()
     #   return render_template("test.html")
    #else:
        # pass # unknown
     #   return render_template("test.html")

@app.route('/contact', methods=['GET', 'POST'])
def cool_form():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()
    
