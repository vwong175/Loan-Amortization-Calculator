"use strict";

// Clears the text fields
function get_value_and_clear(input_obj){
  let retVal = parseFloat(input_obj.value);
  input_obj.value = "";
  return retVal;
}


//CALLBACK Function called when the server responds to client givens. 
function displayTableAndChart(response){
  let dataFromApp = JSON.parse(response);

  google.charts.load('current', {'packages':['table']});
  google.charts.setOnLoadCallback(drawTable);

  function drawTable() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Payment Amount');
    data.addColumn('number', 'Interest');
    data.addColumn('number', 'Cumulative Interest');
    data.addColumn('number', 'Principal');
    data.addColumn('number', 'Principal Paid');
    data.addColumn('number', 'Balance');
    data.addRows(dataFromApp);

    var table = new google.visualization.Table(document.getElementById('table'));

    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
  }
}

//Function called when we want to load the table and graph
function plotTableAndGraph(){
  let loanAmontElem = document.getElementById("loanAmount");
  let loanAmount = get_value_and_clear(loanAmontElem);

  let annualInterestRateElem = document.getElementById("annualInterestRate");
  let annualInterestRate = get_value_and_clear(annualInterestRateElem);

  let loanTermLengthElem = document.getElementById("termLength");
  let loanTermLength = get_value_and_clear(loanTermLengthElem);

  let clientGivens = {"loan_amount": loanAmount, "annual_interest_rate": annualInterestRate, "loan_term_length": loanTermLength};
  let clientGivensJSON = JSON.stringify(clientGivens);


  ajaxPostRequest("/table", clientGivensJSON, displayTableAndChart);
}

