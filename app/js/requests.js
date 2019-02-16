/**
 * This file will define functions for making requests to the backend api.
 */


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
function getRequest(route, params, handleRes) {
    var req_head = getHeader();

    args = Array()
    for (let [key, value] of Object.entries(params)) {
        if (value instanceof Array || value instanceof Object) {
            value = JSON.stringify(value)
        }
        args.push(key + '=' + value)
    }
    query = '?' + args.join('&')
    
    const req = new Request(base_url+route+query, {
        method: 'GET',
        mode: 'cors'
    });

    fetch(req)
        .then(response => response.json())
        .then(responseJSON => handleRes(responseJSON))
}