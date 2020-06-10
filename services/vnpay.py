import hashlib
from urllib.parse import quote


VNPAY_RETURN_URL = 'http://localhost:5000/payment_return'
VNPAY_PAYMENT_URL = 'http://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNPAY_API_URL = 'http://sandbox.vnpayment.vn/merchant_webapi/merchant.html'
VNPAY_TMN_CODE = '1SNJ89L8'
VNPAY_HASH_SECRET_KEY = 'ODJLXOCEWMFIEJXHJNMZUVFFVRDDXLOT'


class VNPay:
    requestData = {
        'vnp_Version': '2.0.0',
        'vnp_TmnCode': VNPAY_TMN_CODE,
        'vnp_ReturnUrl': VNPAY_RETURN_URL
    }
    responseData = dict()

    def __init__(self, host=None):
        if host and not host.startswith('localhost'):
            self.requestData['vnp_ReturnUrl'] = f'{host}/payment_return'


    def get_payment_url(self):
        vnpay_payment_url = VNPAY_PAYMENT_URL
        secret_key = VNPAY_HASH_SECRET_KEY
        inputData = sorted(self.requestData.items())
        queryString = '&'.join([f'{key}={quote(str(val))}' for key, val in inputData])
        hashData = '&'.join([f'{key}={val}' for key, val in inputData])
        hashValue = self._hash(secret_key + hashData)
        return f'{vnpay_payment_url}?{queryString}&vnp_SecureHashType=MD5&vnp_SecureHash={hashValue}'

    def validate_response(self):
        secret_key = VNPAY_HASH_SECRET_KEY
        vnp_SecureHash = self.responseData['vnp_SecureHash']

        # Remove hash params
        if 'vnp_SecureHash' in self.responseData:
            del self.responseData['vnp_SecureHash']

        if 'vnp_SecureHashType' in self.responseData:
            del self.responseData['vnp_SecureHashType']

        inputData = sorted(self.responseData.items())
        hashData = '&'.join([f'{key}={val}' for key, val in inputData])
        hashValue = self._hash(secret_key + hashData)

        # Debug
        print(secret_key + hashData)
        print(hashValue)
        print(vnp_SecureHash)
        return vnp_SecureHash == hashValue

    @staticmethod
    def _hash(input):
        byteInput = input.encode('utf-8')
        return hashlib.sha256(byteInput).hexdigest()
