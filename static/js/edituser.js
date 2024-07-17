document.getElementById("form2").addEventListener("click", function (event) {
  var confirmDelete = confirm("Are you sure you want to delete?");
  console.log(confirmDelete);
  if (confirmDelete === true ) {
    document.getElementById("someform").submit(); // Submit the form if confirmed
  }
});