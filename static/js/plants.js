function render_plants(container, options) {
    if (typeof options === "undefined") {
        options = {};
    }
    $.get("/plants.json", options.data, function(res) {
        for (var i = 0; i < res.length; i++) {
            var plant = res[i];
            var link = "/plants/by-id/"+plant.id;
            container.append(
                $("<a>").attr("href",link).append(
                    $("<div>").addClass("info_cell").append(
                        $("<h3>").html(plant.id).css("color","black")
                            .css("background-color",plant.id_color)
                    ).append(
                        $("<p>").html(plant.type.common_name)
                    )
                )
            );
        }
        if (!options.hide_create_button) {
            container.append(
                $("<a>").attr("href","/plants/by-id/new.html").append(
                    $("<div>").addClass("info_cell").html("(+) New Plant")
                )
            );
        }
    },"json");
}
function render_plant_types(container, options) {
    $.get("/plant_types.json", function(res) {
        for (var i = 0; i < res.length; i++) {
            var type = res[i];
            var link = "/plants/types/"+type.common_name;
            container.append(
                $("<a>").attr("href",link).append(
                    $("<div>").addClass("info_cell").append(
                        $("<h3>").html(type.common_name).css("color","black")
                    ).append(
                        $("<p>").html(type.latin_name)
                    ).append(
                        $("<p>").html(type.cultivar)
                    )
                )
            );
        }
        var new_string = "(+) New Plant Type";
        container.append(
            $("<a>").attr("href","/plants/types/new.html").append(
                $("<div>").addClass("info_cell").html(new_string)
            )
        );
    }, "json");
}

function _jsonform_display_errors(errors, formElt) {
    for (var i = 0; i < errors.length; i++) {
        if (errors[i].attribute == "type") {
            var message = "Value must be an " +
                errors[i].details[0];
            errors[i].message = message;
        }
        console.log(errors[i]);
    }
    $(formElt).jsonFormErrors(errors, this);
}
