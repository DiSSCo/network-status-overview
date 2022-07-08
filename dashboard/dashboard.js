function drawGraph(form, method, target, type = null, return_length = null) {
  if (target) {
    let formData = serializeFormData(form);
    let graph;

    if (formData['options']) {
      graph = {
        'method': method,
        'mode': formData['mode'],
        'request': formData['options'],
        'type': type,
        'return_length': return_length
      }

      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/get_graph",
        data: JSON.stringify(graph),
        contentType: "application/json",
        success: function (result) {
          process(result, method);
        }
      });
    } else if (method == 'draw_infrastructures_total') {
      graph = {
        'method': method
      }

      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/get_graph",
        data: JSON.stringify(graph),
        contentType: "application/json",
        success: function (result) {
          process(result, method)
        }
      });
    } else {
      /* Empty target */
      $('#' + target).empty();

      if (method == 'draw_issues_and_flags') {
        document.getElementById('issueFlagsCounterTable').classList.add('d-none');
      }
    }
  }

  function process(data, method) {
    graph_data = JSON.parse(data);

    if (method == 'draw_issues_and_flags') {
      /* Show HTML table */
      document.getElementById('issueFlagsCounterTable').classList.remove('d-none');

      Plotly.newPlot(target, graph_data[0], graph_data[1], {
        responsive: true,
        displayModeBar: false,
        staticPlot: true
      });

      if (graph_data[2]) {
        processSubs(graph_data[2])
      }
    } else {
      Plotly.newPlot(target, graph_data[0], graph_data[1], {
        responsive: true,
        displayModeBar: false
      });
    }
  }

  function processSubs(data) {
    /* Check if method is issues and flags, if so draw sub graphs */
    for (subGraph in data) {
      let plot_data = data[subGraph]

      $('#issueFlagsCounterTable tr:last').after('<tr id="issueFlagSubGraph' + subGraph + '"> </tr>');

      let target = 'issueFlagSubGraph' + subGraph;

      Plotly.newPlot(target, plot_data[0], plot_data[1], {
        responsive: true,
        displayModeBar: false
      })
    }
  }
}

/* Function for getting a list of participating countries and setting drop downs */
function getCountriesList() {
  /* Receive countries data */
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/get_countries",
    contentType: "application/json",
    success: function (result) {
      process(result);
    }
  });

  function process(data) {
    let datasetsDropdown = document.getElementById('datasets_country_dropdown');
    let specimensCounterDropdown = document.getElementById('specimens_counter_country_dropdown');
    let specimensCompareDropdown = document.getElementById('specimens_compare_country_dropdown');
    let issuesFlagsDropdown = document.getElementById('issues_flags_country_dropdown');

    let id;

    for (country in data) {
      /* Set drop downs */
      let dropDownRow = "<label class='dropdown-item'> <input type='checkbox' name='options[]' value='";

      // Datasets
      id = 'datasets' + country;
      datasetsDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='datasetsOption'> " + data[country] + " </label>";

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'datasetsOption', 4);
        drawGraph(this.form, 'draw_datasets', 'datasetsGraph');
      });

      // Specimens Count / Progress
      id = 'speciesCounterOption' + country;
      specimensCounterDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='speciesCounterOption'> " + data[country] + " </label>";;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'speciesCounterOption', 1);
        drawGraph(this.form, 'draw_specimens', 'speciesCounterGraph', 'pie');
        drawGraph(this.form, 'draw_specimens_progress', 'speciesProgressGraph');
      });

      // Specimen Comparison
      id = 'speciesCompareOption' + country;
      specimensCompareDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='speciesCompareOption'> " + data[country] + " </label>";;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'speciesCompareOption', 4);
        drawGraph(this.form, 'draw_specimens', 'speciesCompareGraph', 'bar');
      });

      // Issues and Flags
      id = 'issueFlagsCounterOption' + country;
      issuesFlagsDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='issueFlagsCounterOption'> " + data[country] + " </label>";;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'issueFlagsCounterOption', 1);
        drawGraph(this.form, 'draw_issues_and_flags', 'issueFlagsCounterGraph', null, 10)
      });
    }
  }
}
window.onload = getCountriesList();

/* Function for getting a list of participating organisations and setting drop downs */
function getOrganisationsList() {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/get_organisations",
    contentType: "application/json",
    success: function (result) {
      process(result);
    }
  });

  function process(data) {
    let datasetsDropdown = document.getElementById('datasets_organisation_dropdown');
    let specimensCounterDropdown = document.getElementById('specimens_counter_organisation_dropdown');
    let specimensCompareDropdown = document.getElementById('specimens_compare_organisation_dropdown');
    let issuesFlagsDropdown = document.getElementById('issues_flags_organisation_dropdown');

    let id;

    for (organisation in data) {
      organisation = data[organisation];
      organisation['ror'] = organisation['ror'].replace('https://ror.org/', '');

      /* Set drop downs */
      let dropDownRow = "<label class='dropdown-item'> <input type='checkbox' name='options[]' value='";

      // Datasets
      id = 'datasets' + organisation['ror'];
      datasetsDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='datasetsOption'> " + organisation['name'] + " </label>";

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'datasetsOption', 4);
        drawGraph(this.form, 'draw_datasets', 'datasetsGraph');
      });

      // Specimens Count / Progress
      id = 'speciesCounterOption' + organisation['ror'];
      specimensCounterDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='speciesCounterOption'> " + organisation['name'] + " </label>";;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'speciesCounterOption', 1);
        drawGraph(this.form, 'draw_specimens', 'speciesCounterGraph', 'pie');
        drawGraph(this.form, 'draw_specimens_progress', 'speciesProgressGraph');
      });

      // Specimen Comparison
      id = 'speciesCompareOption' + organisation['ror'];
      specimensCompareDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='speciesCompareOption'> " + organisation['name'] + " </label>";;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'speciesCompareOption', 4);
        drawGraph(this.form, 'draw_specimens', 'speciesCompareGraph', 'bar');
      });

      // Issues and Flags
      id = 'issueFlagsCounterOption' + organisation['ror'];
      issuesFlagsDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='issueFlagsCounterOption'> " + organisation['name'] + " </label>";;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'issueFlagsCounterOption', 1);
        drawGraph(this.form, 'draw_issues_and_flags', 'issueFlagsCounterGraph', null, 10)
      });
    }
  }

}
window.onload = getOrganisationsList();

/* Function for serizaling form data to an object */
function serializeFormData(form) {
  if (form != null) {
    let data = {};

    /* Setting the form data to the new data object */
    $.each($(form).serializeArray(), function () {
      if (this.name.includes('[]')) {
        if (typeof data[this.name] === 'undefined') {
          data[this.name] = [];

          data[this.name].push(this.value);
        } else {
          data[this.name].push(this.value);
        }
      } else {
        data[this.name] = this.value;
      }
    });

    /* Removing block brackets */
    $(Object.keys(data)).each(function (i, key) {
      if (key.includes('[]')) {
        oldKey = key;
        newKey = key.replace('[]', '');

        data[newKey] = data[oldKey];
        delete data[oldKey];
      }
    });

    return data;
  } else {
    return false;
  }
}

/* Function for checking how many options are checked */
function checkOptions(id, className, length) {
  let currentLength = $('.' + className + ':checked:not(:disabled)').length;

  if (currentLength > length) {
    document.getElementById(id).checked = false;
  }
}

/* Function for switching actives */
function switchMode(id, className) {
  $('.' + className).each(function (i, element) {
    element.classList.add('d-none');

    $('#' + element.id + ' input').prop('disabled', true);
  });

  document.getElementById(id).classList.remove('d-none');
  $('#' + id + ' input').prop('disabled', false);
}

/* Function for swithing the dashboard page */
function switchDashboardPage(method) {
  let currentPage = $('.dashboardPage:not(".d-none")')[0];

  currentPage.classList.add('d-none');
  nextPage = '';

  if (method == 'up') {
    // Check if there is an up page
    if (nextPage = document.querySelector('[pageNumber="' + (parseInt(currentPage.getAttribute('pageNumber')) + 1) + '"]')) {

    } else {
      nextPage = document.getElementsByClassName('dashboardPage')[0];
    }
  } else if (method == 'down') {
    // Check if there is an down page
    if (nextPage = document.querySelector('[pageNumber="' + (parseInt(currentPage.getAttribute('pageNumber')) - 1) + '"]')) {

    } else {
      nextPage = Array.from(document.getElementsByClassName('dashboardPage')).at(-1);
    }
  }

  nextPage.classList.remove('d-none');

  // Set page number indication
  document.getElementById('pageSwitcherField').innerText = nextPage.getAttribute('pageNumber');
}

window.onload = drawGraph(null, 'draw_infrastructures_total', 'infrastructureDatasetsTableGraph');