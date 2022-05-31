// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract sendData {

    bool public state;
    uint public limit;
    address public getReward;
    address public sender;

    constructor(uint _limit, address _getReward) {
        limit = _limit;
        getReward = _getReward;
        sender = msg.sender;
    }


    function getHumidity(uint value) public returns (bool){
        if (value > limit) {
            state = true;
        } else {
            state = false;
        }
        return state;
    }

}