$(document).ready(function () {
    // Adjust dropdown width
    function adjustDropdownWidth() {
        var inputWidth = $('#userInput').outerWidth();
        $('#results').css('width', inputWidth + 'px');
    }

    adjustDropdownWidth();

    $(window).resize(function () {
        adjustDropdownWidth();
    });

    // Trigger the search
    $("#userInput").on("input", function () {
        var query = $(this).val();

        if (query.length > 0) {
            $.ajax({
                url: "/search",  // Assuming you have a /search route
                method: "GET",
                data: { query: query },
                success: function (response) {
                    $("#results").empty();

                    if (response.results.length > 0) {
                        response.results.forEach(function (result) {
                            $("#results").append(
                                '<li>' +
                                '<span class="client-name">' + result.name + '</span>' +
                                '<button class="check-in-button">Check In</button>' +
                                '</li>'
                            );
                        });
                    }

                    // Always append "Add New Client"
                    $("#results").append(
                        '<li class="add-client-link">' +
                        '<span class="add-client-text">+ Add New Client</span>' +
                        '</li>'
                    );
                    $("#results").show();
                }
            });
        } else {
            $("#results").hide();
        }
    });

    // Show modal when "Add New Client" is clicked
    $(document).on('click', '.add-client-link', function () {
        $('#addClientModal').show();  // Show the modal
    });

    // Close the modal
    $('#closeModal').click(function () {
        $('#addClientModal').hide();
    });

    // Handle form submission via AJAX
    $('#submitClientForm').click(function () {
        let countAdults = $('#count_adults').val();
        let countChildren = $('#count_children').val();
        let countSeniors = $('#count_seniors').val();
        let firstName = $('#first_name').val();
        let lastName = $('#last_name').val();
        let internalNote = $('#internal_note').val();
        let needsFoodCat = $('#needs_food_cat').is(':checked');
        let needsFoodDog = $('#needs_food_dog').is(':checked');

        // Validate non-negative numbers
        if (countAdults < 0 || countChildren < 0 || countSeniors < 0) {
            alert('Please enter non-negative numbers.');
            return;
        }

        if (firstName === '' || lastName === '') {
            alert('Please fill out the client\'s first and last name.');
        } else if (countAdults === '' || countChildren === '' || countSeniors === '') {
            alert('Please fill out all required fields.');
        } else {
            // Send form data via AJAX
            $.ajax({
                url: "/add-client",
                method: "POST",
                data: {
                    first_name: firstName,
                    last_name: lastName,
                    count_adults: countAdults,
                    count_children: countChildren,
                    count_seniors: countSeniors,
                    internal_note: internalNote,
                    needs_food_cat: needsFoodCat,
                    needs_food_dog: needsFoodDog
                },
                success: function (response) {
                    alert(response.message);
                    $('#addClientModal').hide();
                },
                error: function (error) {
                    alert("An error occurred while adding the client.");
                    console.log(error);
                }
            });
        }
    });
});