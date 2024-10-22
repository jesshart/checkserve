$(document).ready(function () {
    function adjustDropdownWidth() {
        var inputWidth = $('#userInput').outerWidth();
        $('#results').css('width', inputWidth + 'px');
    }

    adjustDropdownWidth();

    $(window).resize(function () {
        adjustDropdownWidth();
    });

    $("#userInput").on("input", function () {
        var query = $(this).val();

        if (query.length > 0) {
            $.ajax({
                url: "/search",
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
                        $("#results").show();
                    } else {
                        $("#results").hide();
                    }
                }
            });
        } else {
            $("#results").hide();
        }
    });
});