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

buildings={'farm':20,'cave':10,'house':5}

@app.route('/process_money', methods=['POST'])
def process_money():
    now = datetime.datetime.now().strftime("%m/%d/%Y, at %H:%M %p")
    if request.form['building'] == 'casino':
        earned=randint(-50,min(int(session['gold']),50))
        if earned > 0:
            session['events'].insert(0,f"<li class='text-success'>{now}: Earned {earned} gold From the Casino! Lucky!!!</li>")
            session['gold'] = str(int(session['gold'])+ earned)
        elif earned == 0:
            session['events'].insert(0,f"<li>{now}: You broke even at the Casino! Oh well.</li>")
        elif earned < 0:
            if abs(earned) >= int(session['gold']):
                session['events'].insert(0,f"<li class='text-danger'>{now}: Lost all of your gold at the Casino!!! That's why we don't gamble...</li>")
                session['gold']=0
            else:
                session['events'].insert(0,f"<li class='text-danger'>{now}: Lost {abs(earned)} gold at the Casino! Ouch...</li>")
                session['gold'] = str(int(session['gold'])+ earned)
    else:
        earned=randint(buildings[request.form['building']]//2,buildings[request.form['building']])
        session['events'].insert(0,f"<li class='text-success'>{now}: Earned {earned} gold From the {request.form['building']}!</li>")
        session['gold'] = str(int(session['gold'])+ earned)

    return redirect('/')
@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)