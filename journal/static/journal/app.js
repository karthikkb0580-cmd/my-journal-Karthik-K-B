document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("[data-demo-button]");
    const message = document.querySelector("[data-demo-message]");
    if (button && message) {
        button.addEventListener("click", () => {
            message.textContent = "Great! Your JavaScript file is connected and responding.";
        });
    }
});
