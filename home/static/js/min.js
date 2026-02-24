// login
const loginBtn = document.getElementById("loginBtn");
const loginModal = document.getElementById("loginModal");

loginBtn.addEventListener("click", () => {
  loginModal.classList.remove("hidden");
});

function closeModal() {
  loginModal.classList.add("hidden");
}

// signup
const signupBtn = document.getElementById("signupBtn");
const signupModal = document.getElementById("signupModal");

signupBtn.addEventListener("click", () => {
  signupModal.classList.remove("hidden");
});

function closeSignup() {
  signupModal.classList.add("hidden");
}

// dashboard
// function goDashboard(){
//     window.location.href = "dashboard.html";
// }

