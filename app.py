from flask import Flask, render_template, redirect, request, session
from random import randint
import datetime
app = Flask(__name__)
app.secret_key="notmygoldennuggetsssssssssssss"
@app.route('/')
def index():
    if not 'gold' in session:
        session['gold'] = '0'
        session['events']=[]
    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process_money():
    now = datetime.datetime.now().strftime("%m/%d/%Y, at %H:%M %p")
    if request.form['building'] == 'farm':
        earned=randint(10,20)
        session['gold'] = str(int(session['gold'])+ earned)
        session['events'].append(f"<li class='text-success'>{now}: Earned {earned} gold From the Farm!</li>")
    elif request.form['building'] == 'cave':
        earned=randint(5,10)
        session['gold'] = str(int(session['gold'])+ earned)
        session['events'].append(f"<li class='text-success'>{now}: Earned {earned} gold From the Cave!</li>")
    elif request.form['building'] == 'house':
        earned=randint(2,5)
        session['gold'] = str(int(session['gold'])+ earned)
        session['events'].append(f"<li class='text-success'>{now}: Earned {earned} gold From the House!</li>")
    elif request.form['building'] == 'casino':
        earned=randint(-50,min(int(session['gold']),50))
        if earned > 0:
            session['events'].append(f"<li class='text-success'>{now}: Earned {earned} gold From the Casino! Lucky!!!</li>")
            session['gold'] = str(int(session['gold'])+ earned)
        elif earned == 0:
            session['events'].append(f"<li>{now}: You broke even at the Casino! Oh well.</li>")
        elif earned < 0:
            if abs(earned) >= int(session['gold']):
                session['events'].append(f"<li class='text-danger'>{now}: Lost all of your gold at the Casino!!! That's why we don't gamble...</li>")
                session['gold']=0
            else:
                session['events'].append(f"<li class='text-danger'>{now}: Lost {abs(earned)} gold at the Casino! Ouch...</li>")
                session['gold'] = str(int(session['gold'])+ earned)
    print(session['events'])
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)