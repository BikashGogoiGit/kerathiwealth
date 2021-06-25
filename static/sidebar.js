var li_items = document.querySelectorAll(".sidebar ul li");
var hamburger = document.querySelector(".hamburger");
var sidebar = document.querySelector(".sidebar");







hamburger.addEventListener("click", () => {
	hamburger.closest(".sidebar").classList.toggle("click_collapse");
	hamburger.closest(".sidebar").classList.toggle("hover_collapse");
})
