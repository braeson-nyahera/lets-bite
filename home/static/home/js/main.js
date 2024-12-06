// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function () {
const alertBox = document.getElementById("alertBox");
if (alertBox) {
    // Set a timeout to hide the alert after 10 seconds
    setTimeout(() => {
    alertBox.classList.add("hidden");
    }, 10000); // 10000 milliseconds = 10 seconds
}
});