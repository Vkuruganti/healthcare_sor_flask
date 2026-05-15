const customFields = document.querySelector("#custom-fields");
const template = document.querySelector("#custom-field-template");
const addButton = document.querySelector("#add-field");

function wireRemoveButton(button) {
  button.addEventListener("click", () => {
    button.closest(".custom-row").remove();
  });
}

document.querySelectorAll(".remove-button").forEach(wireRemoveButton);

addButton?.addEventListener("click", () => {
  const fragment = template.content.cloneNode(true);
  const removeButton = fragment.querySelector(".remove-button");
  wireRemoveButton(removeButton);
  customFields.appendChild(fragment);
  customFields.lastElementChild.querySelector("input").focus();
});
