function ajaxGetRequest(path, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
  	  if (this.readyState===4 && this.status ===200) {
	      callback(this.response);
	    }
    }
    request.open("GET", path);
    request.send();
}


function showGraph(response) {
    let d = JSON.parse(response);
    Plotly.newPlot(d.div,d.data,d.layout);
}

function getData() {
    ajaxGetRequest("/pieChart", showGraph);
    ajaxGetRequest("/bubbleChart", showGraph);
}

function ajaxPostRequest(path, data, callback){
    let request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState === 4 && this.status === 200){
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(data);
}

function sendPiePost(){
  toSend = document.getElementById("input1").value;
  if(parseInt(toSend) >= 1998 && parseInt(toSend) <= 2020){
    ajaxPostRequest("/sendPie", toSend, showGraph);
  } else{
    alert();
  }
}

function chart(){
  ajaxGetRequest("/bubbleMonth", showGraph);
}

function chart(){
  ajaxGetRequest("/bubbleChart", showGraph);
}

function chart(){
  ajaxGetRequest("/bubbleChange", showGraph);
}