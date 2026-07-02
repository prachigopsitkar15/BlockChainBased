
# Blockchain-Based Facial Recognition Attendance System

A web application that marks attendance using facial recognition and records each attendance entry immutably on an Ethereum blockchain via a Solidity smart contract.

## Overview

This project combines computer vision, a Flask backend, and a Hardhat/Solidity smart contract to build a tamper-proof attendance system:

1. A known set of face images is encoded on startup.
2. A webcam captures a face via the browser (or a local OpenCV window, in the script version).
3. The Flask backend matches the captured face against known encodings using `face_recognition`.
4. On a match, the backend calls the `markAttendance` function on an `Attendance` smart contract deployed to a local Ethereum node, storing the name and timestamp on-chain.
5. Attendance records can be fetched back from the contract and displayed in the browser.

## Tech Stack

**Smart contract / blockchain**
- Solidity `^0.8.24`
- Hardhat (compilation, local node, deployment)
- Hardhat Ignition (deployment modules)
- ethers.js v5 / `@nomiclabs/hardhat-ethers`

**Backend**
- Python, Flask
- `web3.py` (contract interaction)
- OpenCV (`opencv-python`)
- `face_recognition` (face detection/encoding)
- NumPy

**Frontend**
- HTML/CSS/JavaScript (vanilla)
- Browser `getUserMedia` API for webcam capture

## Project Structure

```
proj/
├── contracts/
│   ├── Attendance.sol        # Core smart contract: stores/retrieves attendance records
│   └── Lock.sol               # Sample Hardhat starter contract (not used by the app)
├── scripts/
│   └── deploy.js               # Deploys the Attendance contract
├── ignition/modules/
│   └── Lock.js                 # Hardhat Ignition sample deployment module
├── test/
│   └── Lock.js                 # Sample test for Lock.sol
├── templates/
│   └── index.html              # Web UI (webcam capture + attendance list)
├── static/
│   └── script.js               # Frontend logic: capture image, call API, render results
├── AP.py                       # Flask app: web-based attendance API (main entry point)
├── AttendanceProject.py        # Standalone OpenCV script version (local webcam window, no Flask)
├── contract_details.json       # Deployed contract address + ABI (generated after deployment)
├── hardhat.config.js           # Hardhat/Solidity compiler configuration
├── package.json                # Node.js dependencies
└── .gitignore
```

## Smart Contract: `Attendance.sol`

```solidity
function markAttendance(string memory _name, string memory _time) public
function getAttendanceCount() public view returns (uint256)
function getAttendanceRecord(uint256 index) public view returns (string memory, string memory)
```

Each call to `markAttendance` appends a `Record { name, time }` to on-chain storage and emits an `AttendanceMarked` event.

## Prerequisites

- Node.js and npm
- Python 3.x
- `cmake` and a C++ build toolchain (required to build `dlib`, a dependency of `face_recognition`)
- A working webcam

## Setup

### 1. Install Node dependencies and start a local blockchain

```bash
npm install
npx hardhat node
```

Keep this terminal running — it hosts your local Ethereum network on `http://localhost:8545`.

### 2. Compile and deploy the contract

In a new terminal:

```bash
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

Copy the deployed contract address printed to the console, and update `contract_details.json` with the deployed `address` and the ABI from `artifacts/contracts/Attendance.sol/Attendance.json`.

### 3. Install Python dependencies

```bash
pip install flask opencv-python numpy face_recognition web3
```

> `face_recognition` depends on `dlib`, which compiles from source — installation can take several minutes.

### 4. Add reference face images

Create an `ImagesAttendance/` folder in the project root and add one clear photo per person, named after that person (e.g., `ImagesAttendance/John.jpg`). This folder is not included in the repo and must be created locally.

### 5. Run the app

**Web version (recommended):**
```bash
python AP.py
```
Then open `http://localhost:5000` in a browser, allow camera access, and use the on-page buttons to capture and view attendance.

**Standalone script version:**
```bash
python AttendanceProject.py
```
This opens a native OpenCV window using your default webcam, marks attendance automatically on face match, and press `q` to quit.

## API Endpoints (`AP.py`)

| Method | Endpoint              | Description                                      |
|--------|------------------------|---------------------------------------------------|
| GET    | `/`                    | Serves the web UI                                  |
| POST   | `/save_attendance`     | Accepts an image, matches face, marks attendance on-chain |
| GET    | `/display_attendance`  | Returns all attendance records from the contract   |

## Notes

- `artifacts/` and `cache/` are Hardhat build outputs — normally excluded from version control via `.gitignore`, but currently present in this bundle.
- `contract_details.json` must be regenerated (or manually updated) every time the contract is redeployed, since local Hardhat node addresses reset between sessions.
- This is a local-development setup (`localhost:8545`); deploying to a public testnet or mainnet would require additional configuration (RPC provider, private keys, gas handling) not present here.


