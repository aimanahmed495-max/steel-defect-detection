const button = document.getElementById("ping-button");
const statusMessage = document.getElementById("status-message");

if (button && statusMessage) {
  button.addEventListener("click", () => {
    statusMessage.textContent = "Frontend scaffold is wired and ready for API integration.";
  });
}
