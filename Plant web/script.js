function displayFileName() {
  const fileInput = document.getElementById("file");
  const fileNameSpan = document.getElementById("file-name");

  if (fileInput.files.length > 0) {
    fileNameSpan.textContent = fileInput.files[0].name;
  } else {
    fileNameSpan.textContent = "";
  }
}

function captureImage() {
  fetch("/cam-hi.jpg")
    .then((response) => {
      if (response.status === 200) {
        alert("Image captured successfully!");
      } else {
        alert("Failed to capture image. Check ESP32-CAM connection.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
