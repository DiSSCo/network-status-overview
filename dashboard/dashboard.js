let csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrf_token);
    }
  }
});

function drawGraph(form, method, target, type = null, return_length = null) {
  let formData = serializeFormData(form);
  let graph;

  if (formData['options'] || method == 'draw_infrastructures_total') {
    graph = {
      'method': method,
      'mode': formData['mode'],
      'request': formData['options'],
      'type': type,
      'return_length': return_length
    }

    $.ajax({
      type: "GET",
      url: "https://sandbox.dissco.tech/api/v1/network-overview/get_graph",
      data: { 'data': JSON.stringify(graph) },
      contentType: "application/json",
      success: function (result) {
        process(result);
      }
    });
  } else {
    /* Empty target */
    $('#' + target).empty();

    if (method == 'draw_issues_and_flags') {
      document.getElementById('issueFlagsCounterTable').classList.add('d-none');
    }
  }

  function process(data) {
    let graph_data = JSON.parse(data);

    if (method == 'draw_issues_and_flags') {
      /* Show HTML table */
      document.getElementById('issueFlagsCounterTable').classList.remove('d-none');

      Plotly.newPlot(target, graph_data[0], graph_data[1], {
        responsive: true,
        displayModeBar: false,
        staticPlot: true
      });

      processSubs(graph_data[2]);

      if (document.querySelector('[pageNumber="2"]').classList.contains('opacity')) {
        document.querySelector('[pageNumber="2"]').classList.add('d-none')
        document.querySelector('[pageNumber="2"]').classList.remove('opacity');
        document.querySelector('[pageNumber="3"]').classList.add('d-none')
        document.querySelector('[pageNumber="3"]').classList.remove('opacity');
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
    for (let subGraph in data) {
      let plot_data = data[subGraph]

      $('#issueFlagsCounterTable tr:last').after('<tr id="issueFlagSubGraph' + subGraph + '"> </tr>');

      target = 'issueFlagSubGraph' + subGraph;

      Plotly.newPlot(target, plot_data[0], plot_data[1], {
        responsive: true,
        displayModeBar: false
      })
    }
  }
}

/* Function for getting a list of participating countries and setting drop downs */
function getCountriesList(country_code = null) {
  /* Receive countries data */
  $.ajax({
    type: "GET",
    url: "https://sandbox.dissco.tech/api/v1/network-overview/get_countries",
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

    for (let country in data) {
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
      specimensCounterDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='speciesCounterOption'> " + data[country] + " </label>";

      appendPieToDropdownList(id);

      // Specimen Comparison
      id = 'speciesCompareOption' + country;
      specimensCompareDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='speciesCompareOption'> " + data[country] + " </label>";

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'speciesCompareOption', 4);
        drawGraph(this.form, 'draw_specimens', 'speciesCompareGraph', 'bar');
      });

      // Issues and Flags
      id = 'issueFlagsCounterOption' + country;
      issuesFlagsDropdown.innerHTML += dropDownRow + country + "' id='" + id + "' class='issueFlagsCounterOption'> " + data[country] + " </label>";

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'issueFlagsCounterOption', 1);
        drawGraph(this.form, 'draw_issues_and_flags', 'issueFlagsCounterGraph', null, 10)
      });
    }

    /* Check if data needs to be loaded for country */
    if (country_code) {
      /* Set modes to publishing counry */
      document.getElementById('datasetsSelect').value = 'publishing_country';
      document.getElementById('specimensCounterSelect').value = 'publishing_country';
      document.getElementById('specimensCompareSelect').value = 'publishing_country';
      document.getElementById('issueFlagSelect').value = 'publishing_country';

      checkVisibleDropdowns(process_further);

      function process_further() {
        /* Render graphs */
        document.getElementById('datasets' + country_code).click();
        document.getElementById('speciesCounterOption' + country_code).click();
        document.getElementById('speciesCompareOption' + country_code).click();
        document.getElementById('issueFlagsCounterOption' + country_code).click();
      }
    } else {
      /* Set page 2 and 3 on refresh invisible */
      document.querySelector('[pageNumber="2"]').classList.add('d-none')
      document.querySelector('[pageNumber="2"]').classList.remove('opacity');
      document.querySelector('[pageNumber="3"]').classList.add('d-none')
      document.querySelector('[pageNumber="3"]').classList.remove('opacity');
    }
  }
}

/* Function for getting a list of participating organisations and setting drop downs */
function getOrganisationsList() {
  $.ajax({
    type: "GET",
    url: "https://sandbox.dissco.tech/api/v1/network-overview/get_organisations",
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

    for (let o in data) {
      let organisation = data[o];
      organisation['ror'] = organisation['ror'].replace('https://ror.org/', '');

      let link = "<a href='' class='rorLink'> " + organisation['ror'] + ' </a>'

      /* Set drop downs */
      let dropDownRow = "<label class='dropdown-item'> <input type='checkbox' name='options[]' value='";

      // Datasets
      id = 'datasets' + organisation['ror'];
      datasetsDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='datasetsOption'> " + organisation['name'] + " </label>" + link;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'datasetsOption', 4);
        drawGraph(this.form, 'draw_datasets', 'datasetsGraph');
      });

      // Specimens Count / Progress
      id = 'speciesCounterOption' + organisation['ror'];
      specimensCounterDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='speciesCounterOption'> " + organisation['name'] + " </label>" + link;

      appendPieToDropdownList(id);

      // Specimen Comparison
      id = 'speciesCompareOption' + organisation['ror'];
      specimensCompareDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='speciesCompareOption'> " + organisation['name'] + " </label>" + link;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'speciesCompareOption', 4);
        drawGraph(this.form, 'draw_specimens', 'speciesCompareGraph', 'bar');
      });

      // Issues and Flags
      id = 'issueFlagsCounterOption' + organisation['ror'];
      issuesFlagsDropdown.innerHTML += dropDownRow + organisation['ror'] + "' id='" + id + "' class='issueFlagsCounterOption'> " + organisation['name'] + " </label>" + link;

      $('.dropdownList').on('click', '#' + id, function () {
        checkOptions(this.id, 'issueFlagsCounterOption', 1);
        drawGraph(this.form, 'draw_issues_and_flags', 'issueFlagsCounterGraph', null, 10)
      });
    }
  }
}

function checkVisibleDropdowns(callback = null) {
  let datasetsSelect = document.getElementById('datasetsSelect');
  let specimensCounterSelect = document.getElementById('specimensCounterSelect');
  let specimensCompareSelect = document.getElementById('specimensCompareSelect');
  let issueFlagSelect = document.getElementById('issueFlagSelect');

  if (datasetsSelect.value == 'publishing_country') {
    document.getElementById('publishing_country_datasets').classList.remove('d-none');
    document.getElementById('publisher_datasets').classList.add('d-none');
  } else {
    document.getElementById('publisher_datasets').classList.remove('d-none');
    document.getElementById('publishing_country_datasets').classList.add('d-none');
  }

  if (specimensCounterSelect.value == 'publishing_country') {
    document.getElementById('publishing_country_speciesCounter').classList.remove('d-none');
    document.getElementById('publisher_speciesCounter').classList.add('d-none');
  } else {
    document.getElementById('publisher_speciesCounter').classList.remove('d-none');
    document.getElementById('publishing_country_speciesCounter').classList.add('d-none');
  }

  if (specimensCompareSelect.value == 'publishing_country') {
    document.getElementById('publishing_country_speciesCompare').classList.remove('d-none');
    document.getElementById('publisher_speciesCompare').classList.add('d-none');
  } else {
    document.getElementById('publisher_speciesCompare').classList.remove('d-none');
    document.getElementById('publishing_country_speciesCompare').classList.add('d-none');
  }

  if (issueFlagSelect.value == 'publishing_country') {
    document.getElementById('publishing_country_issueFlagsCounter').classList.remove('d-none');
    document.getElementById('publisher_issueFlagsCounter').classList.add('d-none');
  } else {
    document.getElementById('publisher_issueFlagsCounter').classList.remove('d-none');
    document.getElementById('publishing_country_issueFlagsCounter').classList.add('d-none');
  }

  if (callback) {
    callback();
  }
}

function appendPieToDropdownList(id) {
  $('.dropdownList').on('click', '#' + id, function () {
    checkOptions(this.id, 'speciesCounterOption', 1);
    drawGraph(this.form, 'draw_specimens', 'speciesCounterGraph', 'pie');
    drawGraph(this.form, 'draw_specimens_progress', 'speciesProgressGraph');
  });
}

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
    $(Object.keys(data)).each(function (_i, key) {
      if (key.includes('[]')) {
        let oldKey = key;
        let newKey = key.replace('[]', '');

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
  $('.' + className).each(function (_i, element) {
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
  let nextPage;

  if (method == 'up') {
    // Check if there is an up page
    nextPage = document.querySelector('[pageNumber="' + (parseInt(currentPage.getAttribute('pageNumber')) + 1) + '"]')

    if (!nextPage) {
      nextPage = document.getElementsByClassName('dashboardPage')[0];
    }
  } else if (method == 'down') {
    // Check if there is an down page
    nextPage = document.querySelector('[pageNumber="' + (parseInt(currentPage.getAttribute('pageNumber')) - 1) + '"]')

    if (!nextPage) {
      nextPage = Array.from(document.getElementsByClassName('dashboardPage')).at(-1);
    }
  }

  nextPage.classList.remove('d-none');

  // Set page number indication
  document.getElementById('pageSwitcherField').innerText = nextPage.getAttribute('pageNumber');
}

$(document).ready(function () {
  getCountriesList();

  getOrganisationsList();

  checkVisibleDropdowns();

  drawGraph(null, 'draw_infrastructures_total', 'infrastructureDatasetsTableGraph');
});