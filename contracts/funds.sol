// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract funds {

  address[] _senders;
  address[] _receivers;
  uint[] _amounts;
  uint count=0;

  uint[] _snos;
  uint[] _ids;
  string[] _questions;
  string[] _answers;

  uint[10] _depts=[1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000];
  // Finance,Expenditure,Revenue,Education,Health,Power,Investment,Public Enterprise,Technology,Transportation;

  function addQuestion(uint id,string memory question) public {
    count+=1;
    _snos.push(count);
    _ids.push(id);
    _questions.push(question);
    _answers.push("");
  }

  function viewQuestions() public view returns(uint[] memory,uint[] memory,string[] memory,string[] memory) {
    return(_snos,_ids,_questions,_answers);
  }

  function addAnswer(uint qid,string memory answer) public {
    uint i;
    for(i=0;i<_snos.length;i++){
      if(qid==_snos[i]) {
        _answers[i]=answer;
      }
    }
  }

  function createfund(uint dept,address sender,address receiver,uint amount) public{

    if(_depts[dept]>=amount) {
      _senders.push(sender);
      _receivers.push(receiver);
      _depts[dept]-=amount;
      _amounts.push(amount);
    }
  }

  function viewfunds() public view returns(address[] memory,address[] memory,uint[] memory){
    return(_senders,_receivers,_amounts);
  }

  function viewAllocatedFunds() public view returns(uint[10] memory) {
    return(_depts);
  }

  function addFund(uint dept,uint newfund) public {
    _depts[dept]+=newfund;
  }

}
