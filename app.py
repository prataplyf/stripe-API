# I'm an INDIAN and proud to be on it.
from flask import Flask, request, render_templetes, url_for, jsonify
import stripe   # pip install stripe
from flask_cors import CORS, cross_origin   # to provide cross_origin that access by third party
# pip install flask_cors

app = Flask(__name__)

pub_key = 'pk_test_jhgdjhfvjhvjhvjhcsjhcbsdjcv'
secret_key = 'sk_test_cbsjhcvcjs875sd7cg8ctscsgcg'
stripe.api_key = secret_key

@app.route('/stripePayment')
@cross_origin()
def stripePayment():
    img = "https://www.python.org/static/img/python-logo@2x.png"
    return render_template('stripePayment.html', pub_key=pub_key, image = img)

# checkout
@app.route('/pay', methods=['POST','GET'])
@cross_origin()
def pay():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            # Data from stripe api form
            mail = data['userEmail']
            tkid = data['token']
            # Data at course Purchase time
            name = data['userName']
            amount = data['amount']
            description = data['description']
            courseid = data['courseID']
            userid = data['userID']
            # address
            line1 = data['line1']
            p_code = data['postal_code']
            city = data['city']
            state = data['state']
            country = data['country']  # consider country code must be its IDENTITY NAME INDIA->IND, United State of America->USA
        else:
            mail = request.form['stripeEmail']
            tkid = request.form['stripeToken']
            name = 'xyz'
            amount = 100
            description = 'Test'
            courseid = 'course001'
            userid = 'user001'
            line1 = 'xyz Company'
            p_code = '123'
            city = 'ABC City'
            state = 'MNO State'
            country = 'IND'  # consider country code must be its IDENTITY NAME INDIA->IND, United State of America->USA
        customer = stripe.Customer.create(email=mail, source=tkid)
        # print(customer)
        uniqueCustomerId = customer.sources['data'][0]['fingerprint']
        print(customer.id)
        # print(customer.source)
        Charge = stripe.Charge.create(
                customer = customer.id,
                    amount=amount,
                    currency='usd',
                    description=description,
                    shipping={
                        'name': name,
                        'address': {
                        'line1': line1,
                    'postal_code': p_code,
                    'city': city,
                    'state': state,
                    'country': country,
                        }
                    },
                    )
       
        payment.insert_one({"ChargeID": Charge.id, "customerEmail":customer.email, "customerID":customer.id, "timestamp":Charge.created, "courseID":courseid, "userID":userid})
        return jsonify({"Success Message":Charge.outcome.seller_message, "Charge":Charge.id, "Email":Charge.receipt_url, "status":True})

if __name__ == "__main__":
    # app.run(use_reloader= True, debug=True)
    run_simple('localhost', 5000, app, use_reloader= True, use_debugger = True, use_evalex=True)
