// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

// CONTRACT FOR A CROWD FUNDING APP
// contract that accepts payments

contract Fundino {
    //uses safemath chainlink to stop any wrapping of int values
    using SafeMathChainlink for uint256;

    //keeping track of transactions
    mapping(address => uint256) public addressToAmountFunded;

    //creating an array for contract funders
    address[] public funders;

    //setting owner when smart contract is deployed, sender is contract deployer
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        //setting min value required, everything calculated in wei
        uint256 minimumUSD = 50 * 10**18;
        //revert error check and message
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "Please spend more ETH to continue"
        );

        //keywords used with every transaction [funding smart contract]
        addressToAmountFunded[msg.sender] += msg.value;

        //adding payer to list of funders
        funders.push(msg.sender);
    }

    //to accept money in different currencies, conversion rates needed
    function getVersion() public view returns (uint256) {
        //using eth/usd address
        return priceFeed.version();
    }

    //return price from the smart contract tuple
    function getPrice() public view returns (uint256) {
        // blanks can be used if variable is available but unused
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
        // 404577000000 = 4,045.77000000, smallest unit of measure Wei = 18d.p
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    //withdrawing money to owners account
    modifier onlyOwner() {
        //making sure only owner can withdraw(call this function)
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        //updating each funder account updated to 0 when money withdrawed
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            //put address of funder inside funder variable
            address funder = funders[funderIndex];

            //use 'funder' for key in mapping, number of funders updated to 0
            addressToAmountFunded[funder] = 0;
        }
        //resetting funders array
        funders = new address[](0);
    }
}
