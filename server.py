import random
import time

from flask import Flask
app = Flask(__name__)
app.debug = True


@app.route('/positive')
def postive_test_endpoint():
    return {
        "msg": "Call to this endpoint /positive has succeeded"
    }, 200


@app.route('/negative')
def negative_test_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        time.sleep(2)

    return {
        "msg": "call to the endpoint /negative has not succeeded"
    }, 500


@app.route('/arbitrary')
def fail_randomly_endpoint():
    r = random.randint(0, 1)
    if r == 0:
        return {
            "msg": "call to API endpopint arbitray method has succeeded"
        }, 200

    return {
        "msg": "this endpoint  will fail (sometimes)."
    }, 500

if __name__ == "__main__":
    app.run()
