/**
 * This file will define functions for making requests to the backend api.
 */


base_url = 'http://127.0.0.1:5000'


function getHeader() {
    var req_head = new Headers();
    req_head.append('Accept', 'application/json');
    req_head.append('Content-Type', 'application/json');
    return req_head
}

 /**
  * Sends a post request to the api.
  * 
  * @param {String} route The route to send the post request to.
  * @param {Object} params A javascript object that contains the arguments to send in the post request.
  * @param {Function} handleRes A function that determines what to do with the response when the request is completed.
  * 
  * NOTE: this function may not be fully functional yet.
  */
function postRequest(route, params, handleRes) {
    req_head = getHeader()
    
    const req = new Request(base_url+route, {
        method: 'POST',
        headers: req_head,
        body: JSON.stringify(params),
        mode: 'cors'
    });
    fetch(req)
        .then(response => response.json())
        .then(responseJSON => handleRes(responseJSON));
}


/**
 * Sends a get request to the api.
 * 
 * @param {String} route The route to send the post request to.
 * @param {Object} params A javascript object that contains the arguments to send in the get request.
 * @param {*} handleRes A function that determines what to do with the response when the request is completed.
 * 
 * NOTE: this function may not be fully functional yet.
 */
function getRequest(route, handleRes) {
    const req = new Request(base_url+route, {
        method: 'GET',
        mode: 'cors'
    });

    fetch(req)
        .then(response => response.json())
        .then(responseJSON => handleRes(responseJSON))
}

function parse_cookies(str) {
    str = str.split('; ');
    var result = {};
    for (var i = 0; i < str.length; i++) {
        var cur = str[i].split('=');
        if (cur[0] == 'id' || cur[0] == 'token') {
            result[cur[0]] = cur[1];
        }
    }
    return result;
}