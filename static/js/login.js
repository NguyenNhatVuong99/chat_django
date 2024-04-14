$(".toggle").on("click", function () {
  $(".container").stop().addClass("active");
});

$(".close").on("click", function () {
  $(".container").stop().removeClass("active");
});

let accessToken = sessionStorage.getItem("accessToken");
let refreshToken = sessionStorage.getItem("refreshToken");
// console.log(BASE_URL_LOCAL);
if (accessToken && refreshToken) {
  window.location.href = "http://127.0.0.1:8080";
}
function readCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

var csrftoken = readCookie("csrftoken");
console.log(csrftoken);
function parseJwt(token) {
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  var jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
}

$("#btn-login").click((e) => {
  e.preventDefault();
  fetch(`${BASE_URL_API}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
    body: JSON.stringify({
      email: $("#email-login").val(),
      password: $("#password-login").val(),
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((response) => {
      // Process the newly created user data
      if (response.status === 200) {
        let data = response.data;
        currentUser = {
          id: data.user.id,
          avatar: data.user.avatar,
          full_name: data.user.full_name,
        };
        sessionStorage.setItem("accessToken", data.access);
        sessionStorage.setItem("refreshToken", data.refresh);
        sessionStorage.setItem("currentUser", JSON.stringify(currentUser));
        Swal.fire({
          text: "Login successful",
          icon: "success",
          timer: 3000,
          showConfirmButton: false,
        });
        window.location.href = "http://127.0.0.1:8080";
        // let user_id = decodedToken.user_id
        // sessionStorage.setItem("userId", user_id);
        // getUserById(userId)
      } else {
        console.log(response.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
