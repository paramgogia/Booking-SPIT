document.addEventListener("DOMContentLoaded", function() {
  var dateDisplay = document.querySelector("#a");
  var prevBtn = document.querySelector("#prevBtn");
  var nextBtn = document.querySelector("#nextBtn");
  var cDate = document.getElementById("a").innerHTML.trim();
  var dateParts = cDate.split("-");
  var year = parseInt(dateParts[0]);
  var month = parseInt(dateParts[1]) - 1; // Months are zero-based (0-11)
  var day = parseInt(dateParts[2]);
  var currentDate = new Date(year, month, day);
  var options = {
    timeZone: "Asia/Kolkata",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  };
  var istDate = currentDate.toLocaleString("en-IN", options).substring(0,10);
  var listDate=istDate.split("/");
  document.getElementById("myDate").value = listDate[2]+"-"+listDate[1]+"-"+listDate[0];
  var status = document.getElementById("status").value;
  console.log(status);
  console.log(typeof status);
  // var prebooked = [
  //   {r: 1, c: 0},
  //   {r: 1, c: 1},
  //   {r: 1, c: 2},
  //   {r: 2, c: 0},
  //   {r: 2, c: 1},
  //   {r: 2, c: 2},
  //   {r: 3, c: 0},
  // ]
  // var timeslots = JSON.parse('{{ timeslots|json_script:"timeslots-data" }}');
  // // Accessing timeslots in JavaScript
  // for (var i = 0; i < timeslots.length; i++) {
  //   var timeslot = timeslots[i];
  //   console.log(timeslot.slot, timeslot.room, timeslot.date);
  //   // Perform any desired operations with the timeslot attributes
  // }
  // Update the table with the current date
  updateTable(currentDate);

  // Add click event listeners to the buttons
  prevBtn.addEventListener("click", function () {
    currentDate.setDate(currentDate.getDate() - 1);
    var dateinput = document.createElement("input");
    dateinput.type = "hidden";
    dateinput.name = "dateinput";
    dateinput.id = "dateinput";
    var day = String(currentDate.getDate()).padStart(2, "0");
    var month = String(currentDate.getMonth() + 1).padStart(2, "0");
    var year = currentDate.getFullYear();

    var formattedDate = year + "-" + month + "-" + day;
    dateinput.value = formattedDate;

    // Append the hidden input fields
    var form = document.getElementById("form1");
    form.appendChild(dateinput);
    form.submit();
  });

  nextBtn.addEventListener("click", function () {
    currentDate.setDate(currentDate.getDate() + 1);
    var dateinput = document.createElement("input");
    dateinput.type = "hidden";
    dateinput.name = "dateinput";
    dateinput.id = "dateinput";
    var day = String(currentDate.getDate()).padStart(2, "0");
    var month = String(currentDate.getMonth() + 1).padStart(2, "0");
    var year = currentDate.getFullYear();

    var formattedDate = year + "-" + month + "-" + day;
    dateinput.value = formattedDate;

    // Append the hidden input fields
    var form = document.getElementById("form2");
    form.appendChild(dateinput);
    form.submit();
  });

  // Function to update the table with the given date
  function updateTable(date) {
    var selectedDate = new Date(cDate);
    var thisDate = new Date();
    selectedDate.setHours(0,0,0,0);
    thisDate.setHours(0,0,0,0);
    console.log(selectedDate);
    console.log(thisDate);
    var dateboolean;
    if(selectedDate < thisDate){
      dateboolean = false;
    }
    else{
      dateboolean = true;
    }
    // Clear existing rows
    // tableBody.innerHTML = "";

    // Update date display
    dateDisplay.textContent = formatDate(date);
    
    var cell = document.getElementsByClassName("table-cells");
    for (var i = 0; i < cell.length; i++) {
      if (cell[i].innerHTML.trim()==="" && dateboolean && isLessThanTwoMonthsDifference(selectedDate, thisDate)) {
        if(status === "0"){
        cell[i].addEventListener("mousedown", handleMouseDown);
        cell[i].addEventListener("mouseover", handleMouseOver);
        cell[i].addEventListener("mouseup", handleMouseUp);
        }
      }
      else if (cell[i].innerHTML.trim() === "Booked by You") {
        //add grey background color
        cell[i].style.backgroundColor = "lightgreen";
      }
      else if (cell[i].innerHTML.trim() !==""){
        //add blue background color
        cell[i].style.backgroundColor = "lightgrey";
      }
    }
    // Generate rows dynamically
    // for (var i = 0; i < 24; i++) {
    //   var timeSlot = getTimeSlot(i);
    //   var row = document.createElement("tr");

    //   var timeSlotCell = document.createElement("td");
    //   timeSlotCell.textContent = timeSlot;
    //   row.appendChild(timeSlotCell);

    //   for (var j = 0; j < 3; j++) {
    //     var roomCell = document.createElement("td");
    //     row.appendChild(roomCell);
    //     roomCell.id = "cell-" + i + "-" + j;
    //     
    //     var isPrebooked = prebooked.some(
    //       (cell) => cell.r === i && cell.c === j
    //     );

    //     if (isPrebooked) {
    //       roomCell.style.backgroundColor = "lightblue";
    //       roomCell.removeEventListener("mousedown", handleMouseDown);
    //       roomCell.removeEventListener("mouseover", handleMouseOver);
    //       roomCell.removeEventListener("mouseup", handleMouseUp);
    //     }
    //   }

  //     tableBody.appendChild(row);
  //   }
  }

  function isLessThanTwoMonthsDifference(date1, date2) {
    var twoMonthsMilliseconds = 1000 * 60 * 60 * 24 * 30 * 1; // Total milliseconds in two months
    var dateDiffMilliseconds = Math.abs(date2 - date1); // Difference in milliseconds between the two dates
    return dateDiffMilliseconds < twoMonthsMilliseconds;
  }

  // Helper function to format the date as "Day, Month Date, Year"
  function formatDate(date) {
    var options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    return date.toLocaleDateString(undefined, options);
  }
  
  function toggleBooking(cell) {
    cell.classList.toggle("selected");

  }

  // Rest of the code for handleMouseDown, handleMouseOver, handleMouseUp, toggleBooking, and getTimeSlot functions..

  // Function to handle mousedown event
  function handleMouseDown(event) {
    event.preventDefault();
    isMouseDown = true;
    startCell = event.target;
    toggleBooking(startCell);
  }

  // Function to handle mouseover event
  function handleMouseOver(event) {
    if (isMouseDown) {
      var currentCell = event.target;
      toggleBooking(currentCell);
    }
  }

  // Function to handle mouseup event
  function handleMouseUp() {
    isMouseDown = false;
    startCell = null;
  }

  // Function to save the selected slots
  function saveBooking() {
    // Get all elements with the class "selected"
    var selectedElements = document.getElementsByClassName("selected");

    // Create an array to store the IDs
    var selectedIds = [];

    // Loop through the selected elements and extract their IDs
    for (var i = 0; i < selectedElements.length; i++) {
      selectedIds.push(selectedElements[i].id);
    }

    // Create a hidden input field to store the IDs
    var hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "selected_ids";
    hiddenInput.id = "selected_ids";
    hiddenInput.value = selectedIds;
    console.log(selectedIds);
    //create another hidden input field to store the date
    var dateinput = document.createElement("input");
    dateinput.type = "hidden";
    dateinput.name = "dateinput";
    dateinput.id = "dateinput";
    var day = String(currentDate.getDate()).padStart(2, "0");
    var month = String(currentDate.getMonth() + 1).padStart(2, "0");
    var year = String(currentDate.getFullYear());

    var mon = document.createElement("input");
    mon.type="hidden";
    mon.name="month";
    mon.id="month";
    mon.value = month;
    console.log(month);
    var formattedDate = year + "-" + month + "-" + day;
    dateinput.value = formattedDate;

    var y = document.createElement("input");
    y.type = "hidden";
    y.name = "year";
    y.id = "year";
    y.value = year;
    console.log(y);

    // Append the hidden input fields
    var form = document.getElementById("bookingForm");
    form.appendChild(hiddenInput);
    form.appendChild(dateinput);
    form.appendChild(mon);
    form.appendChild(y);
    form.validateForm();
    form.submit()
    // var reason = prompt("Please enter a reason for booking the slots:");
    // if (reason.trim() !== null) {
    //   var confirmed = confirm(
    //     "Are you sure you want to book these slots?\nReason: " + reason
    //   );
    //   if (confirmed) {
    //     // form.submit();
    //   }
    // }
  }

  // Add click event listener to the "Book" button
  bookBtn.addEventListener("click", function () {
    saveBooking();
  });
  
  var curr = document.getElementById("myDate");
  curr.addEventListener("input", function () {
    // Submit the form when a date is selected
    var dateinput = document.createElement("input");
    dateinput.type = "hidden";
    dateinput.name = "dateinput";
    dateinput.id = "dateinput";
    dateinput.value = curr.value;
    console.log(curr.value)
    console.log(dateinput.value);
    // Append the hidden input fields
    var form1 = document.getElementById("form4");
    form1.appendChild(dateinput);
    form1.submit();
  });
});
