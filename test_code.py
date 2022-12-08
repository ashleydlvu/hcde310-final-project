from flask import Flask, render_template, request
import logging

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main_handler():
    app.logger.info("In MainHandler")
    if request.method == 'POST':
        app.logger.info(request.form.get('username'))
        name = request.form.get('username')
        # app.logger.info(request)
        app.logger.info("In POST")
        if name:
        # if form filled in, greet them using this data
            app.logger.info("In NAME")
            greet_types = request.form.getlist('greet_type')
            app.logger.info(greet_types)
            return render_template('test_response.html',
            name=name,
            page_title="Greeting Page Response for %s"%name,
            greetings=[greet_person(name, t) for t in greet_types]
            )
        else:
        #if not, then show the form again with a correction to the user
            return render_template('test_form.html',
            page_title="Greeting Form - Error",
            prompt="How can I greet you if you don't enter a name?")
    else:
        return render_template('test_form.html',page_title="Greeting Form")

def greet_person(name, t):
    """A helper function that makes greetings"""
    if t == "birthday":
        return "Happy Birthday this month, %s!" % (name)
    else:
        return "Hello %s" % (name)

if __name__ == "__main__":
# Used when running locally only. 
# When deploying to Google AppEngine, a webserver process will
# serve your app. 
    app.run(host="localhost", port=8080, debug=True)