const foldButtons = document.querySelectorAll(".fold-button");

foldButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const post = button.closest(".one-post");
        const isFolded = post.classList.toggle("folded");

        button.textContent = isFolded ? "Развернуть" : "Свернуть";
        button.setAttribute("aria-expanded", String(!isFolded));
    });
});