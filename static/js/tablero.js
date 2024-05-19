let table_name = document.getElementById('table').value
let owner_name = document.getElementById('table').dataset.id_user
let table_remove = document.getElementsByClassName('table_remove')
let localhost = 'http://127.0.0.1:5001/'

document.getElementById('form_table').onsubmit = function(e) {
  e.preventDefault();  
  fetch('/table/create', {
    method: 'POST',
    body: JSON.stringify({
      'name': document.getElementById('table').value,
      'owner': owner_name,
      'admin': true
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response){
    return response.json();
  })
  .then(function(jsonResponse) {
    if(jsonResponse['status']=='true'){
      window.location.reload();
    }
    else{
      UIkit.notification({
        message: "You can't create a table with the name default!",
        status: 'default',
        timeout: 3000
      });
    }
  })
  .catch(function(error){
    UIkit.notification({
			message: 'Table was not created',
			status: 'danger',
			timeout: 3000
		});
  });
}

for (let i = 0; i < table_remove.length; i++) {
  table_remove[i].addEventListener('click',  function tableRemove() {
    fetch('/' + user_name + '/' + tablero_name + '/tablero/delete/',{
      method: 'POST',
      body: JSON.stringify({
        'owner_name': owner_name,
        'table_id': table_remove[i].dataset.table_id
      }),
      headers: {
        'content-type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(res => {
      UIkit.notification({
        message: 'Table deleted!',
        status: 'success',
        timeout: 3000
      });
      window.location.assign(localhost + owner_name + "/default/" + res['table_id'] + "/todos/");
    })
  });
}