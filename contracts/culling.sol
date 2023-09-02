// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "tests/console.sol";

interface IERC20 {
    function transferFrom(address from, address to, uint value) external returns(bool );
    function burnFrom(address account, uint256 amount) external;
    function balanceOf(address account) external view returns (uint256 balance);
    function totalSupply() external view returns (uint256 totalSupplyAmount);
}

contract CullProtocol {
    IERC20 public token;
    uint256 public lastCullTime;
    uint256 public APR; // in percentage, e.g., 5 for 5%
    uint256 public constant YEAR_IN_SECONDS = 31536000; // 365 days

    // Mapping and array for O(1) operations
    mapping(address => uint256) public holderIndex;  // address => index+1 in holderList
    address[] public holderList;

    constructor(address _token, uint256 _APR) {
        console.log("kek");
        token = IERC20(_token);
        APR = _APR;
        console.log("block.timestamp", block.timestamp);
        lastCullTime = block.timestamp;
        console.log("lastCullTime", lastCullTime);
    }

    function addHolder(address _holder) public {
        require(holderIndex[_holder] == 0, "Holder already exists");
        holderList.push(_holder);
        holderIndex[_holder] = holderList.length;
    }

    function removeHolder(address _holder) public {
        require(holderIndex[_holder] > 0, "Holder does not exist");
        
        uint256 index = holderIndex[_holder] - 1;
        address lastHolder = holderList[holderList.length - 1];
        holderList[index] = lastHolder;
        holderIndex[lastHolder] = index + 1;
        
        holderList.pop();
        delete holderIndex[_holder];
    }

    function cullInterval() public view returns(uint256 _cullInterval) {
        uint256 totalSupply = token.totalSupply();
        uint256 cullAmount = (totalSupply * APR) / 100;
        _cullInterval = YEAR_IN_SECONDS / cullAmount;
        return _cullInterval;
    }

    function cull() public {
        uint256 timePassed = block.timestamp - lastCullTime; // Time since the last cull
        uint256 totalSupply = token.totalSupply(); // Total token supply

        // Calculate the Holding Period Return (HPR)
        uint256 hprNumerator = 1 + APR / 100;
        uint256 hprDenominator = YEAR_IN_SECONDS;
        uint256 hprExponent = timePassed / hprDenominator;
        uint256 hpr = hprNumerator ** hprExponent - 1;

        // Calculate the total tokens to cull based on total supply
        uint256 totalTokensToCull = totalSupply * hpr;

        // Initialize the random index
        uint256 randomIndex = uint256(keccak256(abi.encodePacked(block.timestamp, blockhash(block.number - 1)))) % holderList.length;

        // Loop to cull tokens from holders
        while (totalTokensToCull > 0) {
            address holderToCull = holderList[randomIndex];
            uint256 holderBalance = token.balanceOf(holderToCull);

            uint256 tokensToCullFromHolder = holderBalance < totalTokensToCull ? holderBalance : totalTokensToCull;

            // Burn tokens from this holder
            token.burnFrom(holderToCull, tokensToCullFromHolder);
            totalTokensToCull -= tokensToCullFromHolder;

            // If the holder's balance becomes zero, remove them from holderList
            if (token.balanceOf(holderToCull) == 0) {
                removeHolder(holderToCull);
            }

            // Update the random index for the next iteration
            randomIndex = (randomIndex + 1) % holderList.length;
        }

        lastCullTime = block.timestamp;
    }


    function calculateAmountToCull() internal view returns(uint256 totalTokensToCull) {
        uint256 timePassed = block.timestamp - lastCullTime; // Time since the last cull
        uint256 totalSupply = token.totalSupply(); // Total token supply

        // Calculate the Holding Period Return (HPR)
        uint256 hprNumerator = 1 + APR / 100;
        uint256 hprDenominator = YEAR_IN_SECONDS;
        uint256 hprExponent = timePassed / hprDenominator;
        uint256 hpr = hprNumerator ** hprExponent - 1;

        // Calculate the total tokens to cull based on total supply
        totalTokensToCull = totalSupply * hpr;
        
        return totalTokensToCull;
    }
}
