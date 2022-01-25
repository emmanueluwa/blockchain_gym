// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    //functions needed for lottery project

    //address array storing players
    address payable[] public players;
    address payable public recentWinner;
    //keeping track of numbers
    uint256 public randomness;
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
    uint256 public fee;
    bytes32 public keyhash;

    //storing things we need for when contract deployed
    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18); //having units of measure in wei
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
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

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        //call...
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Too early to be claculating the winner."
        );
        require(_randomness > 0, "random number not found");
        //picking a random winnder
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        //paying winner all the p
        recentWinner.transfer(address(this).balance);
        //reset lottery
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
