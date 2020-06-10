from datetime import datetime
from flask import Flask, render_template, request, redirect
from services.vnpay import VNPay

HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data={"title": "Danh sách demo"})


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        form = request.form.copy()
        order_type = form['order_type']
        order_id = form['order_id']
        amount = form['amount']
        order_desc = form['order_desc']
        bank_code = form['bank_code']
        language = form['language']
        ipaddr = request.remote_addr
        vnp = VNPay()
        vnp.requestData['vnp_Command'] = 'pay'
        vnp.requestData['vnp_Amount'] = int(amount) * 100
        vnp.requestData['vnp_CurrCode'] = 'VND'
        vnp.requestData['vnp_TxnRef'] = order_id
        vnp.requestData['vnp_OrderInfo'] = order_desc
        vnp.requestData['vnp_OrderType'] = order_type
        vnp.requestData['vnp_Locale'] = language if language else 'vn'
        if bank_code:
            vnp.requestData['vnp_BankCode'] = bank_code
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.requestData['vnp_IpAddr'] = ipaddr
        vnpay_payment_url = vnp.get_payment_url()
        print(vnpay_payment_url)
        return redirect(vnpay_payment_url)
    else:
        return render_template("payment.html", data={"title": "Thanh toán"})


@app.route('/payment_return')
def payment_return():
    vnp = VNPay()
    inputData = request.args.copy()
    if inputData:
        vnp.responseData = inputData
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        data = {
            "title": "Kết quả thanh toán",
            "order_id": order_id,
            "amount": amount,
            "order_desc": order_desc,
            "vnp_TransactionNo": vnp_TransactionNo,
            "vnp_ResponseCode": vnp_ResponseCode
        }
        if vnp.validate_response():
            if vnp_ResponseCode == "00":
                data['result'] = "Thành công"
                return render_template("payment_return.html", data=data)
            else:
                data['result'] = "Lỗi"
                return render_template("payment_return.html", data=data)
        else:
            data['result'] = "Lỗi"
            return render_template("payment_return.html", data=data)
    else:
        return render_template("payment_return.html", data={"title": "Kết quả thanh toán", "result": ""})

# @app.route('/query')
# def query():
#     return render_template('index.html')
#
#
# @app.route('/refund')
# def payment_return():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(HOST, PORT)
