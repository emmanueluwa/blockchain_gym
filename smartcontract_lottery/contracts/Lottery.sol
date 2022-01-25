// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    //functions needed for lottery project

    //address array storing players
    address payable[] public players;
    uint256 public usdEntryFee;

    //pulling from pricefeed to convert 50$ to its value in eth
    AggregatorV3Interface internal ethUsdPriceFeed;

    //type w 3 positions
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    } //0, 1, 2
    LOTTERY_STATE public lottery_state;

    //storing things we need for when contract deployed
    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18); //having units of measure in wei
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable {
        //can only enter when lottery started
        require(lottery_state == LOTTERY_STATE.OPEN);
        //50$ minimum
        require(msg.value >= getEntranceFee(), "Not enough ETH to enter");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        //getting entrance fee depending on latest price feed
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18decimals, eth/usd feed is 8 .dp
        //50$ -> 2,000 eth. Solidity does not work w decimals
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice; //decimals need to be understood cancelling out is needed
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Current lottery is still running"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public {}
}
