from flask import Flask,render_template,request,redirect,session
from web3 import Web3,HTTPProvider
import json

depts=['finance','expenditure','revenue','education','health','power','investment','publicenterprise','technology','transportation']
depts1=['Finance','Expenditure','Revenue','Education','Health','Power','Investment','Public Enterprise','Technology','Transportation']

def connect_blockchain_register(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/register.json'
    with open(artifact_path) as F:
        contract_json=json.load(F)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

def connect_blockchain_fund(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/funds.json'
    with open(artifact_path) as F:
        contract_json=json.load(F)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

app=Flask(__name__)
app.secret_key='Sandhya'

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
def publictrackingpage():
    contract,web3=connect_blockchain_register(0)
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_fund(0)
    _senders,_receivers,_amounts=contract.functions.viewfunds().call()
    print(_usernames,_emails,_names,_mobiles,_depts,_roles,_passwords)
    print(_senders,_receivers,_amounts)
    data=[]
    for i in range(len(_senders)):
            dummy=[]
            #sno,sender,sender dept, receiver,amount
            sindex=_usernames.index(_senders[i])
            dummy.append(_senders[i])
            dummy.append(_names[sindex])
            dummy.append(_depts[sindex])
            dummy.append(_receivers[i])
            dummy.append(_amounts[i])
            data.append(dummy)
    return render_template('publictracking.html',res=data,l=len(data))

@app.route('/newhead')
def newheadpage():
    return render_template('newhead.html')

@app.route('/newhome')
def newhomepage():
    return render_template('newhome.html')

@app.route('/newdesc')
def newdescpage():
    return render_template('newdesc.html')

@app.route('/allocatefund')
def allocatefundpage():
    return render_template('allocatefund.html')

@app.route('/logout')
def logoutpage():
    session.pop('username',None)
    return redirect('/')

@app.route('/tracking')
def trackingpage():
    contract,web3=connect_blockchain_register(0)
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_fund(0)
    _senders,_receivers,_amounts=contract.functions.viewfunds().call()
    print(_usernames,_emails,_names,_mobiles,_depts,_roles,_passwords)
    print(_senders,_receivers,_amounts)
    print(session['username'])
    data=[]
    for i in range(len(_senders)):
        if _senders[i]==session['username']:
            dummy=[]
            #sno,sender,sender dept, receiver,amount
            sindex=_usernames.index(_senders[i])
            dummy.append(_senders[i])
            dummy.append(_names[sindex])
            dummy.append(_depts[sindex])
            dummy.append(_receivers[i])
            dummy.append(_amounts[i])
            data.append(dummy)
    return render_template('tracking.html',res=data,l=len(data))

@app.route('/funddetails')
def funddetails():
    contract,web3=connect_blockchain_fund(0)
    _depts=contract.functions.viewAllocatedFunds().call()
    data=[]
    for i in range(len(_depts)):
        dummy=[]
        dummy.append(depts1[i])
        dummy.append(1000000)
        dummy.append(_depts[i])
        data.append(dummy)
    return render_template('funddetails.html',res=data,l=len(data))

@app.route('/funddetails1')
def funddetails1():
    contract,web3=connect_blockchain_fund(0)
    _depts=contract.functions.viewAllocatedFunds().call()
    data=[]
    for i in range(len(_depts)):
        dummy=[]
        dummy.append(depts1[i])
        dummy.append(1000000)
        dummy.append(_depts[i])
        data.append(dummy)
    return render_template('funddetails1.html',res=data,l=len(data))

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
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()
    userindex=_usernames.index(username)
    role=_roles[userindex]
    if state==True and role==0:
        session['username']=username
        return redirect('/newdesc')
    elif role==1:
        return(render_template('login.html',err='You are not authorized'))
    else:
        return(render_template('login.html',err='login failed'))

@app.route('/allocatefundform',methods=['post'])
def allocatefundform():
    contract,web3=connect_blockchain_register(0)
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()

    walletaddr=session['username']
    walletindex=_usernames.index(walletaddr)
    department=_depts[walletindex]

    deptindex=depts1.index(department)
    sender=walletaddr
    receiver=request.form['receiver']
    amount=request.form['amount']
    print(department,sender,receiver,amount)
    contract,web3=connect_blockchain_fund(0)
    tx_hash=contract.functions.createfund(deptindex,sender,receiver,int(amount)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(render_template('allocatefund.html',res='Fund Allocated'))

@app.route('/question/<id>')
def askQuestion(id):
    session['id']=id
    return render_template('publicquestion.html')

@app.route('/questionform',methods=['post'])
def questionform():
    id=session['id']
    comment=request.form['comment']
    print(id,comment)
    contract,web3=connect_blockchain_fund(0)
    tx_hash=contract.functions.addQuestion(int(id),comment).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('publicquestion.html',res='Question Asked')

@app.route('/questiondetails')
def questiondetails():
    contract,web3=connect_blockchain_fund(0)
    _snos,_ids,_questions,_answers=contract.functions.viewQuestions().call()
    data=[]
    for i in range(len(_snos)):
        dummy=[]
        dummy.append(_ids[i])
        dummy.append(_questions[i])
        if(len(_answers[i])):
            dummy.append(_answers[i])
        else:
            dummy.append('Not Yet Answered')
        data.append(dummy)
    return render_template('questiondetails.html',res=data,l=len(data))

@app.route('/questiondetails1')
def questiondetails1():
    contract,web3=connect_blockchain_fund(0)
    _snos,_ids,_questions,_answers=contract.functions.viewQuestions().call()

    contract,web3=connect_blockchain_register(0)
    _usernames,_emails,_names,_mobiles,_depts,_roles,_passwords=contract.functions.viewusers().call()

    contract,web3=connect_blockchain_fund(0)
    _senders,_receivers,_amounts=contract.functions.viewfunds().call()
    data=[]
    for i in range(len(_snos)):
        sender=_senders[_ids[i]-1]
        if sender==session['username'] and len(_answers[i])==0:
            dummy=[]
            dummy.append(_snos[i])
            dummy.append(_questions[i])
            data.append(dummy)
    return render_template('questiondetails1.html',res=data,l=len(data))

@app.route('/answer/<id1>')
def answerQuestion(id1):
    session['id1']=id1
    return render_template('answer.html')

@app.route('/answerform',methods=['post'])
def answerform():
    id1=session['id1']
    answer=request.form['answer']
    print(id1,answer)
    contract,web3=connect_blockchain_fund(0)
    tx_hash=contract.functions.addAnswer(int(id1),answer).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('answer.html',res='answered the question')

if __name__=="__main__":
    app.run(debug=True)
