function openNav() {
  document.getElementById("myNav").style.width = "90%";
}

function closeNav() {
  document.getElementById("myNav").style.width = "0%";
}

socketio = io()

socketio.on('live_data', function (data) {
    document.getElementById('live_data').innerHTML = "";
    let result = data['data']
    for (let key in result) {
      let value = result[key];
      $( 'div.live_data' ).append( '<h4 class="gradient">' + key + ': ' + value + '</h4>' )
    }
});

document.getElementById("checkBtn").addEventListener("click", getLiveData);

function getLiveData() {
    var selectedCountryIndex = document.getElementById('selectedCountry').value;
    socketio.emit('getLiveData', selectedCountryIndex)
}

socketio.on('live_c_data', function(data) {
    document.getElementById('live_country_data').innerHTML = "";
    response = data['data']
    for (let key in response) {
      let value = response[key];
      $( 'div.live_country_data' ).append( '<h4 class="gradient text-1-4">' + key + ': ' + value + '</h4>' )
    }
});
