import hashlib
from urllib.parse import quote


class VNPay:
    requestData = dict()
    responseData = dict()

    def get_payment_url(self, vnpay_payment_url, secret_key):
        inputData = sorted(self.requestData.items())
        queryString = '&'.join([f'{key}={quote(val)}' for key, val in inputData])
        hasData = '&'.join([f'{key}={val}' for key, val in inputData])
        hashValue = self.md5_hash(secret_key + hashData)
        return f'{vnpay_payment_url}?{queryString}&vnp_SecureHashType=MD5&vnp_SecureHash={hashValue}'

    def validate_response(self, secret_key):
        vnp_SecureHash = self.responseData['vnp_SecureHash']
        
        # Remove hash params
        if 'vnp_SecureHash' in self.responseData:
            del self.responseData['vnp_SecureHash']

        if 'vnp_SecureHashType' in self.responseData:
            del self.responseData['vnp_SecureHashType']

        inputData = sorted(self.responseData.items())
        hashData = '&'.join([f'{key}={val}' for key, val in inputData])
        hashValue = self.md5_hash(secret_key + hasData)

        # Debug
        print(secret_key + hashData)
        print(hashValue)
        print(vnp_SecureHash)
        return vnp_SecureHash == hashValue

    @staticmethod
    def md5_hash(self, input):
        byteInput = input.encode('utf-8')
        return hashlib.md5(byteInput).hexdigest()
