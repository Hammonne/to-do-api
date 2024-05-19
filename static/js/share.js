document.getElementById('form_share').onsubmit = function(e){
  e.preventDefault();
  fetch('/' + user_name + '/' + tablero_name + '/tablero/share/',{
    method: 'POST',
    body: JSON.stringify({
      shared_user: document.getElementById('shared_username').value,
      owner_user: owner_name
    }),
    headers: {
      'content-type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(res =>{
    if(res['status'] == 'true') {
      listAllTable();
      document.getElementById("description").value = ""
			UIkit.notification({
				message: 'Table shared whit ' +  document.getElementById('shared_username').value,
				status: 'success',
				timeout: 3000
			});
    }
    else{
      UIkit.notification({
        message: "You can't share this table!",
        status: 'default',
        timeout: 3000
      });
    } 
  })
  .catch(function(error) {
		UIkit.notification({
			message: 'Table not shared',
			status: 'danger',
			timeout: 3000
		});
  });
}