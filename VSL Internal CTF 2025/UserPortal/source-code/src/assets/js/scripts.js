// assets/js/scripts.js

document.addEventListener("DOMContentLoaded", function () {
  const loginLink = document.getElementById("login-link");
  const loginButton = document.getElementById("login-button");
  const loginModal = document.getElementById("login-modal");
  const closeButton = document.querySelector(".close-button");
  const loginForm = document.getElementById("login-form");
  const loginError = document.getElementById("login-error");
  const logoutLink = document.getElementById("logout-link");

  function openModal() {
    if (loginModal) {
      loginModal.style.display = "block";
    }
  }

  if (loginButton) {
    loginButton.addEventListener("click", function (e) {
      e.preventDefault();
      openModal();
    });
  }

  function closeModal() {
    if (loginModal) {
      loginModal.style.display = "none";
      loginError.textContent = "";
      if (loginForm) {
        loginForm.reset();
      }
    }
  }

  if (loginLink) {
    loginLink.addEventListener("click", function (e) {
      e.preventDefault();
      openModal();
    });
  }

  if (closeButton) {
    closeButton.addEventListener("click", function () {
      closeModal();
    });
  }

  window.addEventListener("click", function (event) {
    if (event.target === loginModal) {
      closeModal();
    }
  });

  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      e.preventDefault();
      loginError.textContent = "";

      const formData = new FormData(loginForm);
      formData.append("action", "login");

      fetch("index.php", {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.reload();
          } else {
            loginError.textContent = data.message;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          loginError.textContent = "An unexpected error occurred.";
        });
    });
  }

  if (logoutLink) {
    logoutLink.addEventListener("click", function (e) {
      e.preventDefault();
      if (!confirm("Are you sure you want to logout?")) {
        return;
      }
      const formData = new FormData();
      formData.append("action", "logout");

      fetch("index.php", {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.reload();
          } else {
            alert(data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An unexpected error occurred.");
        });
    });
  }
});
