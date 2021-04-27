from flask import Flask, render_template, request, redirect, session, url_for, g 
import speech_recognition as sr 


app = Flask(__name__)
app.secret_key = 'hafizsecretkey5544'


class User: 
	def __init__(self, id, username, password): 
		self.id = id 
		self.username = username
		self.password = password

	def __repr__(self): 
		return "<User: {0}>".format(self.username)


users = []
users.append((User(id=1, username = "Muhammad Ahmad", password = "hafiz2020ahmad")))
users.append((User(id=2, username = "Fatih", password = "appFatih34")))

print(users)

@app.before_request
def before_request(): 
	g.user = None 
	if 'user_id' in session:
		user =  [x for x in users if x.id == session['user_id']][0]
		g.user = user 


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST': 
		session.pop('user_id', None)
		username = request.form['username']
		password = request.form['password']

		user = [x for x in users if x.username == username][0]
		if user and user.password == password: 
			session['user_id'] = user.id
			return redirect(url_for('index'))

		else:
			return redirect(url_for('login'))




	return render_template('login.html')


@app.route("/", methods = ["GET", "POST"])
def index():
	if not g.user: 
		return redirect(url_for('login'))
	text = "sample"
	if request.method == "POST": 
		with sr.Microphone() as source: 
			r = sr.Recognizer()
			audio = r.listen(source)
			try: 
				text = r.recognize_google(audio)
				print(text)
			except: 
				text = "Error in transcribing"



	return render_template('test-model.html', data = text)




@app.route('/audio_to_text/')
def audio_to_text():
    return render_template('test-model.html')

@app.route('/audio', methods=['POST'])
def audio():
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)
  
    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
		select = request.form.get('audio-models')
    	print(str(select)) # just to see what select is
        text = r.recognize_google(audio_data, language = "ar-SA")
        print(text)
        return_text = " Predicted Verse: <br> " 
        return text

        '''
        try:
            for num, texts in enumerate(text['alternative']):
                return_text += str(num+1) +") " + texts['transcript']  + " <br> "
        except:
            return_text = " Sorry!!!! Voice not Detected "
        '''

        '''
        + Arabic (Egypt) ar-EG
+? Arabic (Jordan) ar-JO
+ Arabic (Kuwait) ar-KW
+? Arabic (Lebanon) ar-LB
+ Arabic (Qatar) ar-QA
+ Arabic (UAE) ar-AE
.+ Arabic (Morocco) ar-MA
.+ Arabic (Iraq) ar-IQ
.+ Arabic (Algeria) ar-DZ
.+ Arabic (Bahrain) ar-BH
.+ Arabic (Lybia) ar-LY
.+ Arabic (Oman) ar-OM
.+ Arabic (Saudi Arabia) ar-SA
.+ Arabic (Tunisia) ar-TN
.+ Arabic (Yemen) ar-YE
'''
        
    return str(return_text)



@app.route("/", methods = ["GET", "POST"])
def test_by_upload():
	if not g.user: 
		return redirect(url_for('login'))
	if request.method == "POST": 
		print("Form Data Recieved")

		if "file" not in request.files: 
			return redirect(request.url)

		file =  request.files["file"]
		if file.filename == "": 
			return redirect(request.url)

		if file: 
			recognizer = sr.Recognizer()
			audioFile = sr.AudioFile(file)
			with audioFile as source:
				data = recognizer.record(source)

			text = recognizer.recognize_google(data,key=None)
			print(text)


	return render_template('test-model.html')


@app.route('/home', methods = ['GET', 'POST'])
def home(): 
	return render_template('home.html')





if __name__ == "__main__": 
	app.run(debug=True, threaded=True)