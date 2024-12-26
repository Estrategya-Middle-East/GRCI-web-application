;(function () {
    const modal = new bootstrap.Modal(document.getElementById("modal")); // Initialize the modal
  
    // Show modal when content is loaded into the dialog
    htmx.on("htmx:afterSwap", (e) => {
      if (e.detail.target.id == "dialog") {
        modal.show();
      }
    });
  
    // Hide modal if an empty response is received
    htmx.on("htmx:beforeSwap", (e) => {
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.hide();
        e.detail.shouldSwap = false;
      }
    });
  
    // Clear modal content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = "";
    });
  })();
  