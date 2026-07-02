// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attendance {
    struct Record {
        string name;
        string time;
    }

    Record[] public attendanceRecords;

    // Define the AttendanceMarked event
    event AttendanceMarked(string name, string time);

    function markAttendance(string memory _name, string memory _time) public {
        attendanceRecords.push(Record(_name, _time));
        // Emit the AttendanceMarked event
        emit AttendanceMarked(_name, _time);
    }

    function getAttendanceCount() public view returns (uint256) {
        return attendanceRecords.length;
    }

    function getAttendanceRecord(uint256 index) public view returns (string memory, string memory) {
        require(index < attendanceRecords.length, "Index out of bounds");
        Record memory record = attendanceRecords[index];
        return (record.name, record.time);
    }
}
