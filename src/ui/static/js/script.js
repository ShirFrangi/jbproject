document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("popup");
    const dropdownText = document.getElementById("dropdown-text");
    const destIdInput = document.getElementById("destinationIdInput");
    const destNameInput = document.getElementById("destinationNameInput");
    const passwordInput = document.getElementById("password");
    const toggleBtn = document.getElementById("togglePassword");
    const fileInput = document.getElementById("image");
    const fileNameSpan = document.querySelector(".file-name");
    const previewImage = document.getElementById("preview-image");
    const uploadLabel = document.querySelector(".custom-file-upload");
    const form = document.getElementById("addVacationForm");
    const priceInput = document.getElementById("price");
    const deletePopup = document.getElementById("delete-confirmation");
    const confirmBtn = document.getElementById("confirm-delete-btn");
    const cancelBtn = document.getElementById("cancel-delete-btn");
    const closeBtn = document.getElementById("delete-close-btn");
    let timeoutId;

    // open vacation popup and fill in details
    function openPopup(title, description, imageUrl = "", dates = "", price = "") {
        if (!popup) return;

        popup.querySelector("#popup-title").innerText = title;
        popup.querySelector("#popup-description").innerText = description;
        popup.querySelector("#popup-image").src = imageUrl;
        popup.querySelector("#popup-dates").innerText = `תאריכים: ${dates}`;
        popup.querySelector("#popup-price").innerText = `מחיר: ${price}`;

        popup.classList.remove("hidden");
        popup.style.display = "flex";
        document.body.style.overflow = "hidden";
    }

    // close vacation popup
    function closePopup() {
        if (!popup) return;
        popup.classList.add("hidden");
        document.body.style.overflow = "";
    }
    window.closePopup = closePopup;

    // close delete confirmation popup
    function closeDeletePopup() {
        const deletePopup = document.getElementById("delete-confirmation");
        if (!deletePopup) return;
        deletePopup.classList.add("hidden");
        deletePopup.style.display = "none";
        document.body.style.overflow = "";
        pendingDeleteId = null;
    }

    // initialize dropdown if values exist
    if (dropdownText && destNameInput?.value && destIdInput?.value) {
        dropdownText.innerText = destNameInput.value;
    }

    // initialize date picker with flatpickr
    flatpickr.localize({ rangeSeparator: " - " });
    flatpickr("#dateRangeInput", {
        mode: "range",
        altInput: true,
        allowInput: true,
        dateFormat: "Y/m/d",
        altFormat: "d/m/Y",
        parseDate: (datestr) => moment(datestr, "DD/MM/YYYY", true).toDate(),
        formatDate: (date) => moment(date).format("DD/MM/YYYY")
    });

    // handle destination dropdown item click
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function () {
            const selectedId = this.getAttribute('data-id');
            const selectedName = this.getAttribute('data-name');

            if (dropdownText) dropdownText.innerText = selectedName;
            if (destIdInput) destIdInput.value = selectedId;
            if (destNameInput) destNameInput.value = selectedName;
        });
    });

    // toggle password visibility with timeout
    if (passwordInput && toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            if (passwordInput.type === "text") {
                passwordInput.type = "password";
                clearTimeout(timeoutId);
            } else {
                passwordInput.type = "text";
                timeoutId = setTimeout(() => {
                    passwordInput.type = "password";
                }, 2000);
            }
        });
    }

    // handle vacation card click — open popup with details
    document.querySelectorAll(".vacation-card").forEach(card => {
        card.addEventListener("click", function () {
            if (this.classList.contains("add-new-card")) return;

            const title = this.querySelector("h3")?.innerText || "חופשה";
            const description = this.querySelector(".description")?.innerText || "";
            const imageUrl = this.querySelector("img")?.src || "";
            const dates = this.querySelector(".dates")?.innerText || "";
            const price = this.querySelector(".price")?.innerText || "";

            openPopup(title, description, imageUrl, dates, price);
        });
    });

    // close popup when clicking outside content
    if (popup) {
        popup.addEventListener("click", function (e) {
            if (e.target === popup) closePopup();
        });
    }

    // close button inside popup
    const popupCloseBtn = document.querySelector("#popup .close");
    popupCloseBtn?.addEventListener("click", closePopup);

    // automatically remove flash messages after 3 seconds
    document.querySelectorAll(".flash-message").forEach(msg => {
        setTimeout(() => msg.remove(), 3000);
    });

    // file input change — preview and show file name
    if (fileInput && fileNameSpan && previewImage && uploadLabel) {
        fileInput.addEventListener("change", function () {
            if (this.files?.length) {
                fileNameSpan.textContent = this.files[0].name;

                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImage.src = e.target.result;
                    previewImage.classList.remove("hidden");
                    uploadLabel.classList.add("preview-visible");
                };
                reader.readAsDataURL(this.files[0]);
            } else if (previewImage.dataset.existing) {
                previewImage.src = previewImage.dataset.existing;
                previewImage.classList.remove("hidden");
                uploadLabel.classList.add("preview-visible");
                fileNameSpan.textContent = "";
            } else {
                fileNameSpan.textContent = "לא נבחר קובץ";
                previewImage.src = "";
                previewImage.classList.add("hidden");
                uploadLabel.classList.remove("preview-visible");
            }
        });
    }

    // if page has existing image — show it
    const existingImagePath = document.querySelector("#preview-image[data-existing]");
    if (existingImagePath) {
        previewImage.src = existingImagePath.dataset.existing;
        previewImage.classList.remove("hidden");
        uploadLabel.classList.add("preview-visible");
    }

    // form validation — prevent submit if required fields are missing
    if (form) {
        form.addEventListener("submit", function (event) {
            const destinationText = dropdownText?.innerText.trim() || "";
            const dateRange = document.getElementById("dateRangeInput")?.value.trim() || "";
            const price = priceInput?.value.trim() || "";
            const description = document.getElementById("vacation_info")?.value.trim() || "";
            const isEditPage = document.getElementById("editVacationForm") !== null;

            document.querySelectorAll(".flash-message").forEach(msg => msg.remove());

            if (!destinationText || destinationText === "&nbsp;" || !dateRange || !price || !description || (!isEditPage && (!fileInput?.files || fileInput.files.length === 0))) {
                event.preventDefault();

                const flash = document.createElement("div");
                flash.className = "flash-message error";
                flash.innerText = "יש למלא את כל השדות";
                form.appendChild(flash);

                setTimeout(() => flash.remove(), 4000);
            }
        });
    }

    // price input formatting (add/remove ₪ and allow only numbers and one dot)
    if (priceInput) {
        if (priceInput.value.trim() && !priceInput.value.includes("₪")) {
            priceInput.value = priceInput.value.trim() + " ₪";
        }

        priceInput.addEventListener("focus", function () {
            this.value = this.value.replace(/[₪\s]/g, "");
        });

        priceInput.addEventListener("input", function () {
            this.value = this.value.replace(/[^\d.]/g, "");
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
        });

        priceInput.addEventListener("blur", function () {
            if (this.value.trim()) {
                this.value = this.value.trim() + " ₪";
            }
        });
    }

    // delete popup confirm / cancel buttons
    confirmBtn?.addEventListener("click", () => {
        if (pendingDeleteId !== null) {
            handleDelete(pendingDeleteId);
            closeDeletePopup();
        }
    });
    cancelBtn?.addEventListener("click", closeDeletePopup);
    closeBtn?.addEventListener("click", closeDeletePopup);

    // close delete popup when clicking outside content
    deletePopup?.addEventListener("click", (e) => {
        if (e.target === deletePopup) closeDeletePopup();
    });

    window.openPopup = openPopup;
    
});

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const envPrefix = document.querySelector('meta[name="env-prefix"]').getAttribute('content');

// send delete request to the server
function handleDelete(vacationId) {
    fetch(`/${envPrefix}/delete-vacation/${vacationId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken}
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert("An error occurred while deleting");
            }
        })
        .catch(err => {
            console.error(err);
            alert("An error occurred while deleting");
        });
}

// delete confirmation popup
let pendingDeleteId = null;
function showDeleteConfirmation(vacationId, event) {
    event.stopPropagation();
    pendingDeleteId = vacationId;

    const deletePopup = document.getElementById("delete-confirmation");
    if (!deletePopup) return;
    deletePopup.classList.remove("hidden");
    deletePopup.style.display = "flex";
    document.body.style.overflow = "hidden";
}

window.showDeleteConfirmation = showDeleteConfirmation;

// send like request to the server
function handleLikeClick(event) {
    event.stopPropagation();

    const icon = event.currentTarget;
    const vacationId = icon.getAttribute("data-vacation-id");

    fetch(`/${envPrefix}/like`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
        credentials: "include",
        body: JSON.stringify({ vacation_id: vacationId })
    })
        .then(res => res.json())
        .then(data => {
            if (data.likes_count !== undefined) {
                const likeCountSpan = document.getElementById("like-count-" + vacationId);
                likeCountSpan.textContent = `${data.likes_count} סימנו בלייק`;

                const heartIcon = icon.querySelector("i");
                heartIcon.style.color = data.message.includes("added") ? "red" : "white";
            } else {
                alert(data.error || "Unexpected error");
            }
        })
        .catch(err => {
            console.error("Error sending like:", err);
            alert("Error sending like");
        });
}
