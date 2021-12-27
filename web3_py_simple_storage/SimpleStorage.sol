// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    //initialised to 0
    uint256 luckyNumber;

    struct People {
        uint256 luckyNumber;
        string name;
    }

    // People public person = People({
    //     favouriteNumber: 1,
    //     name: "wiseova"
    // });

    People[] public people;

    //use mapping to find associated paired values
    mapping(string => uint256) public nameToluckyNumber;

    //add a person to an array
    function addPersonstring(string memory _name, uint256 _luckyNumber) public {
        people.push(People({luckyNumber: _luckyNumber, name: _name}));
        // or using index order
        people.push(People(_luckyNumber, _name));

        //add mapping to function
        nameToluckyNumber[_name] = _luckyNumber;
    }

    function store(uint256 _luckyNumber) public {
        luckyNumber = _luckyNumber;
    }

    function retrieve() public view returns (uint256) {
        return luckyNumber;
    }
}
