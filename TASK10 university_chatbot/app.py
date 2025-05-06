from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Basic rule-based chatbot logic
def chatbot_response(user_input):
    user_input = user_input.lower()
    if "admission" in user_input:
        return "Our admissions are open from June to August. You can apply online via the portal."
    elif "fee" in user_input:
        return "The tuition fee varies by program. For BS programs, it's around Rs. 80,000 per semester."
    elif "scholarship" in user_input:
        return "Yes, we offer merit-based and need-based scholarships."
    elif "campus" in user_input:
        return "We have campuses in Lahore, Karachi, and Islamabad."
    else:
        return "Sorry, I didn't understand that. Please ask about admission, fees, or scholarships."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    user_msg = request.args.get("msg")
    response = chatbot_response(user_msg)
    return jsonify(response=response)

if __name__ == "__main__":
    app.run(debug=True)
