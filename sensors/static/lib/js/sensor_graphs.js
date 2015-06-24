var SensorGraphs = function(sensor_api, board, sensor_chart_options, from_time, to_time, draw_function, chart_function) {
  var obj = this; // So we can reference the SensorGraphs object from callbacks

  this.constants = {};
  _.each(board.get("sensors"), function(sensor_id) {
    var sensor = sensor_api.sensors.get(sensor_id);
    var measurement = sensor_api.measurements.get(sensor.get("measurement"));
    var sensor_name = measurement.get("name");
    sensor.name = sensor_name
    obj.constants[sensor_name] = {};
  });
  _.each(sensor_chart_options, function(chart_options, sensor_name) {
    obj.constants[sensor_name].chart_options = chart_options;
  });

  this.load_graphs = function(data_callback) {
    _.each(obj.constants, function(sensor_constants, sensor_name) {
      var data_table = new google.visualization.DataTable()
      data_table.addColumn('datetime', 'Date');
      data_table.addColumn('number', 'Value');
      sensor_constants.data = data_table;
      sensor_constants.chart = chart_function(sensor_name);
    });
    function full_callback(data) {
      // Call the user-provided callback and then call our own callback
      data_callback(data);
      obj.load_data(data);
    }
    board.get_history(full_callback, from_time, to_time);
  };

  this.load_data = function(data) {
    _.each(data, function(data_points, sensor_id) {
      var sensor = sensor_api.sensors.get(sensor_id);
      var sensor_data = obj.constants[sensor.name].data;
      _.each(data_points, function(data_point) {
        var date = new Date(data_point.date_recorded*1000);
        sensor_data.addRow([date, data_point.value]);
      });
    });
    draw_function(obj);
  };

  // Redraw graphs on window resize
  this.resizeTimer = null;
  $(window).resize(function() {
    clearTimeout(obj.resizeTimer);
    obj.resizeTimer = setTimeout(obj.draw_graphs, 100);
  });
};
