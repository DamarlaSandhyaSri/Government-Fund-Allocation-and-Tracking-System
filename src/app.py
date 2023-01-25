from flask import Flask,render_template,request,redirect
from web3 import Web3,HTTPProvider
import json

def connect_blockchain_register(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/register.json'
    contract_address='0x361ef311Fb9bD723aE7424Af6B4e86Eb2a451625'
    with open(artifact_path) as F:
        contract_json=json.load(F)
        contract_abi=contract_json['abi']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('Home.html')

@app.route('/registration')
def registerpage():
    return render_template('Registration.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/head')
def headpage():
    return render_template('Head.html')

@app.route('/desc')
def descpage():
    return render_template('desc.html')

@app.route('/publictracking')
def trackingpage():
    return render_template('publictracking.html')

@app.route('/newhead')
def newheadpage():
    return render_template('newhead.html')

@app.route('/newhome')
def newhomepage():
    return render_template('newhome.html')

@app.route('/registeruser',methods=['post'])
def registeruser():
    username=request.form['username']
    email=request.form['email']
    name=request.form['name']
    mobile=request.form['mobile']
    dept=request.form['dept']
    role=request.form['role']
    password=request.form['password']
    print(username,email,name,mobile,dept,role,password)
    contract,web3=connect_blockchain_register(0)
    tx_hash=contract.functions.registeruser(username,email,name,mobile,dept,int(role),int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/login')

@app.route('/loginuser',methods=['post'])
def loginuser():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    state=contract.functions.loginuser(username,int(password)).call()
    if state==True:
        return redirect('/newhome')
    else:
        return('login failed')

if __name__=="__main__":
    app.run(debug=True)
