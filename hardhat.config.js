require("@nomiclabs/hardhat-ethers");
require("dotenv").config();

module.exports = {
    solidity: {
      version: "0.8.24", // Specify your desired Solidity version here
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        }
      }
    },
    // Other configurations...
  };
 

