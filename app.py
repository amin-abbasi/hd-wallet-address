import os
from dotenv import load_dotenv
from flask  import Flask, request, abort, jsonify, json
from werkzeug.exceptions import HTTPException
from py_crypto_hd_wallet import HdWalletBipFactory, HdWalletBip44Coins, HdWalletBipChanges, HdWalletBipDataTypes
availableCoins = [enum.name for enum in HdWalletBip44Coins]

load_dotenv()
WALLET_NAME = os.getenv('WALLET_NAME')
MNEMONIC    = os.getenv('MNEMONIC')
print('env MNEMONIC: ', MNEMONIC)
app = Flask(__name__)

# -------- Error Handler --------
@app.errorhandler(HTTPException)
def handle_exception(e):
  '''Return JSON instead of HTML for HTTP errors.'''
  # start with the correct headers and status code from the error
  response = e.get_response()
  # replace the body with JSON
  response.data = json.dumps({
    'code': e.code,
    'name': e.name,
    'description': e.description,
  })
  response.content_type = 'application/json'
  return response

# -------- Healthcheck Route --------
@app.route('/health')
def helloWorld():
  return '200'

# -------- Generate New Address API --------
@app.route('/address', methods=['POST'])
def createAddress():

  # -------- Validate Request Body --------
  body = request.form
  if not body:
    body = request.get_json()

  if not body:
    abort(400, 'Bad Request. No body found.')
  if not body['userId']:
    abort(400, 'Bad Request. userId is required.')
  if not body['coin']:
    abort(400, 'Bad Request. coin is required.')

  userId = int(body['userId'])
  coin = str(body['coin']).upper()

  if not (coin in availableCoins):  
    abort(400, 'Bad Request. Invalid Coin Type.')
  if not userId or userId < 0:
    abort(400, 'Bad Request. User ID must be an integer greater than 0.')

  factory = HdWalletBipFactory(HdWalletBip44Coins[coin])
  wallet = factory.CreateFromMnemonic(WALLET_NAME, MNEMONIC)
  wallet.Generate(acc_idx=userId, change_idx=HdWalletBipChanges.CHAIN_EXT, addr_num=1)
  addresses = wallet.GetData(HdWalletBipDataTypes.ADDRESS).ToDict()
  result = {
    'success' : True,
    'userId'  : userId,
    'address' : addresses['address_0']['address']
  }
  return jsonify(result)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
