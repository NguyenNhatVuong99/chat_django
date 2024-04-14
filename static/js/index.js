$(document).ready(function () {
  let accessToken = sessionStorage.getItem("accessToken");
  let refreshToken = sessionStorage.getItem("refreshToken");
  let currentUser = JSON.parse(sessionStorage.getItem("currentUser"));
  console.log(currentUser);
  if (!accessToken || !refreshToken) {
    window.location.href = `http://127.0.0.1:8080/login`;
  }
  $("#user-avatar").attr(
    "src",
    "https://firebasestorage.googleapis.com/v0/b/spotify-83a8a.appspot.com/o/images%2Flogo.jpg?alt=media&token=05e4b1a7-790f-4dbd-ac2e-f99fcbd2239f"
  );
  $("#full_name").html(currentUser.full_name);
  const toggleButton = document.querySelector(".dark-light");
  const colors = document.querySelectorAll(".color");

  $("#btnLogout").click(() => {
    sessionStorage.removeItem("accessToken");
    sessionStorage.removeItem("refreshToken");
    sessionStorage.removeItem("currentUser");
    window.location.href = `http://127.0.0.1:8080/login`;
  });
});
