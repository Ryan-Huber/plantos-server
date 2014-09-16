function render_plants(container, options) {
    if (typeof options === "undefined") {
        options = {};
    }
    $.get("/plants/plants.json", options.data, function(res) {
        var row = $("<div>").addClass("row");
        container.append(row);
        for (var i = 0; i < res.length; i++) {
            var plant = res[i];
            var link = "/plants/by-id/"+plant.id;
            row.append(_info_cell(link, [
                $("<h3>").html(plant.id).css("color","black")
                         .css("background-color",plant.id_color),
                $("<p>").html(plant.type.common_name)
            ]));
        }
        if (options.hide_create_button != true) {
            var link = "/plants/by-id/new.html";
            row.append(_info_cell(link, [
                $("<span>").addClass("glyphicon")
                           .addClass("glyphicon-plus-sign"),
                $("<span>").text(" New Plant")
            ]));
        }
    },"json");
}
function render_plant_types(container, options) {
    if (typeof options === "undefinded") {
        options = {};
    }
    $.get("/plants/plant_types.json", function(res) {
        var row = $("<div>").addClass("row");
        container.append(row);
        for (var i = 0; i < res.length; i++) {
            var type = res[i];
            var link = "/plants/types/"+type.common_name;
            row.append(_info_cell(link, [
                $("<h3>").html(type.common_name).css("color","black"),
                $("<p>").html(type.latin_name),
                $("<p>").html(type.cultivar)
            ]));
        }
        var link = "/plants/types/new.html";
        row.append(_info_cell(link, [
            $("<span>").addClass("glyphicon")
                       .addClass("glyphicon-plus-sign"),
            $("<span>").text(" New Plant Type")
        ]));
    }, "json");
}

// Creates an info_cell DOM element with the given link and content
function _info_cell(link, content) {
    var cell = $("<div>").addClass("info_cell");
    for (var i = 0; i < content.length; i++) {
        cell.append(content[i]);
    }
    return $("<a>").addClass("col-lg-3").addClass("col-md-4")
                   .addClass("col-sm-6").attr("href",link).append(cell);
}

// Function to pass to the jsongotm displayErrors option to render errors better
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

// Function to fix the array navigation buttons. (They are designed for use with
// Bootstrap 2, and we are using Bootstrap 3).
function _jsonform_fix_array_buttons() {
    $('._jsonform-array-addmore').addClass('btn-default');
    $('.icon-plus-sign').addClass('glyphicon')
                        .addClass('glyphicon-plus-sign');
    $('._jsonform-array-deletelast').addClass('btn-default');
    $('.icon-minus-sign').addClass('glyphicon')
                         .addClass('glyphicon-minus-sign');
}
