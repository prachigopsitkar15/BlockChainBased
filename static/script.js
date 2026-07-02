const video = document.getElementById('video');
const saveButton = document.getElementById('saveButton');
const displayButton = document.getElementById('displayButton');
const attendanceList = document.getElementById('attendanceList');

// Function to start attendance marking
async function saveAttendance() {
    // Capture image from video
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');

    // Convert Data URL to Blob
    const blob = await fetch(imageData).then(res => res.blob());

    // Create form data
    const formData = new FormData();
    formData.append('image', blob, 'image.jpg'); // Ensure 'image' is the field name

    // Send image data to server
    const response = await fetch('/save_attendance', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    console.log(data);
}

async function displayAttendance() {
    try {
        // Make API call to fetch attendance data
        const response = await fetch('/display_attendance');
        const data = await response.json();

        // Clear previous data
        attendanceList.innerHTML = '';

        // Populate attendance list
        if (Array.isArray(data)) {
            data.forEach(entry => {
                const listItem = document.createElement('li');
                listItem.textContent = `${entry.name} - ${entry.time}`;
                attendanceList.appendChild(listItem);
            });
        } else {
            console.error("Invalid data format:", data);
        }
    } catch (error) {
        console.error("Error fetching/displaying attendance:", error);
    }
}



// Access webcam
async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
    video.srcObject = stream;
}

saveButton.addEventListener('click', saveAttendance);
displayButton.addEventListener('click', displayAttendance);

setupCamera();
