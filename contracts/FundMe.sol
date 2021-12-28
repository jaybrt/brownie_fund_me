// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function getEnteranceFee() public view returns (uint256) {
        uint256 minUSD = 50 * 10**18;
        uint256 price = getPrice();
        return (minUSD * 10**18) / price;
    }

    function fund() public payable {
        //$50 threshold
        require(
            msg.value >= getEnteranceFee(),
            "ETH threshold for funding not met"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        //what eth to usd conversion rate is
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    function getConversion(uint256 ethAmt) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 usdAmt = (ethPrice * ethAmt) / 10**18;
        return usdAmt;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            addressToAmountFunded[funders[funderIndex]] = 0;
        }
        funders = new address[](0);
    }
}
