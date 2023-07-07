# The Caesar Code
#### Video Demo:  https://youtu.be/4Z94krt_-eM
#### Description:
The application has collection of questions, each question is encrypted into caesar code , and the user must guess
what is the first word in the text , the system will check the user answer and calculate the readability of the
question if the answer is correct then the user will add this grade to the score.
The index.html has the form that display the questions and score and answer result , he also contain a form to get the user answer.
The app.py file has the backend code that contains 4 main parts , post function , get function , readability calculating function , and decryption function .
the get function returns the first question and store new score value and qustion id in the session , while the encryption function encrypt the text of the question to send it to the user , the decryption function do exactly the opposite , the readability function calculate how easy or hard the text was and provides a level as a grade.
if the user answer correct then the system add up the score and ask the user the next question.
when the payer user first use the application , the system triggers the get method path through the index route web api , then he use the session to init the score and set it to 0 , and questions count to 0 , then the system would query the database and retive the first question to display it to the user , after that the system will decrypt the text and send it to the user display , in the second time when the user submit the answer the system get the question counter and retrive the question based on the given id , then he compare the fisrt word and the word given by the player user answer and if it is correct he calculates the qeustion text relability to set the grade of the text and increase the score by it , then he store it in the session , then return correct answer result .
The "@app.route("/", methods=["GET", "POST"])" over the "def index():" code means that the index method accept both get and post , we do want to use the get , since it keeps history , while post is more secured.
The code "if request.method == "POST":" checks if the user is posting answer or getting the page view for the first time .
the system use "request.form.get("answer")" parse the get url forum post content , in this example this code retrive the answer forum element name value.
The code "quizPrev = db.execute("select question from questions where id = ?", quizid)[0]["question"]" will retrive the question id quizid from the table questions .
The "correctAnswer = answer == quizPrev.split()[0]" get the first word from quizPrev text and compare it with the answer word given by the player user .
The code "return render_template("index.html", question = quizEncipher, result = result, score = score)" will return the "index.html" view with the parameters quizEncipher, result , score those are provided to the web page index.html elements name question, result, score.