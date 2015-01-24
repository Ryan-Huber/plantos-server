var list_plants_url;
var view_plant_url;
function render_plants(container, data) {
    $.get(list_plants_url, data, function(res) {
        var row = $("<div>").addClass("row");
        container.append(row);
        for (var i = 0; i < res.length; i++) {
            var plant = res[i];
            var link = view_plant_url + plant._id;
            row.append(_info_cell(link, [
                $("<h3>").html(plant.number).css("color","black"),
                $("<p>").html(plant.type.common_name)
            ]));
        }
    },"json");
}
var list_plant_types_url;
var view_plant_type_url;
function render_plant_types(container) {
    $.get(list_plant_types_url, function(res) {
        var row = $("<div>").addClass("row");
        container.append(row);
        res.sort(function(a, b) {
          return a.common_name.localeCompare(b.common_name);
        });
        for (var i = 0; i < res.length; i++) {
            var type = res[i];
            var link = view_plant_type_url + type._id;
            row.append(_info_cell(link, [
                $("<h3>").html(type.common_name).css("color","black"),
                $("<p>").html(type.latin_name),
                $("<p>").html(type.cultivar)
            ]));
        }
    }, "json");
}

// Creates an info_cell DOM element with the given link and content
function _info_cell(link, content, data) {
    var cell = $("<div>").addClass("info_cell");
    for (var key in data) {
        attr = "data-" + key;
        cell.attr(attr, data[key]);
    }
    for (var i = 0; i < content.length; i++) {
        cell.append(content[i]);
    }
    return $("<a>").addClass("col-lg-3").addClass("col-md-4")
                   .addClass("col-sm-6").attr("href",link).append(cell);
}
/*function clear_search() {
    $("#id_search").val("");
    plant_id_search();
    $("#location_search").val("");
    plant_location_search();
    $("#type_search").val("");
    plant_type_search();
}
function plant_id_filter() {
    $("#location_filter").hide();
    $("#type_filter").hide();
    $("#id_filter").show();
    clear_search();
}
function plant_id_search() {
    id = $("#id_search").val();
    $.each($("#plants .info_cell"), function(i, cell) {
        if (id == "" || cell.getAttribute("data-id").indexOf(id) > -1) {
            $(cell.parentNode).show();
        }
        else {
            $(cell.parentNode).hide();
        }
    });
}
function plant_location_filter() {
    $("#id_filter").hide();
    $("#type_filter").hide();
    $("#location_filter").show();
    clear_search();
}
function plant_location_search() {
    _location = $("#location_search").val();
    console.log(_location);
    $.each($("#plants .info_cell"), function(i, cell) {
        if (_location == "" || cell.getAttribute("data-location").indexOf(_location) > -1) {
            $(cell.parentNode).show();
        }
        else {
            $(cell.parentNode).hide();
        }
    });
}
function plant_type_filter() {
    $("#id_filter").hide();
    $("#location_filter").hide();
    $("#type_filter").show();
    clear_search();
}
function plant_type_search() {
    type = $("#type_search").val();
    $.each($("#plants .info_cell"), function(i, cell) {
        if (type == "" || cell.getAttribute("data-type").indexOf(type) > -1) {
            $(cell.parentNode).show();
        }
        else {
            $(cell.parentNode).hide();
        }
    });
}*/
