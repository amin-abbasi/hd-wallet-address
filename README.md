# HD-Wallet-Address
This is a mini service to generate addresses in the master HD-Wallet. It will use `py_crypto_hd_wallet` package as a base.

## Prerequisites
You need to have [Python3](https://www.python.org/downloads) installed in your system.

## Run Application
First, create your virtual environment:
```
python3 -m venv venv
```
and then activate it by:
```
. venv/bin/activate
```

Then install dependencies using `requirements.txt`:
```
pip3 install -r requirements.txt
```

After that you can run:
```
flask run
```
or simply:
```
python app.py
```

This will run the app in all addresses
