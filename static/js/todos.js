const form = document.getElementById('ftodo');
const errormsg = document.getElementById('error');
const todosElement = document.getElementById('todosli');
const user_name = document.getElementById('description').dataset.id_user;
let href = window.location.href
let arr = href.split('/')
let tablero_name = arr[4]

listAllTable();



document.getElementById('ftodo').onsubmit = function(e){
  e.preventDefault();

  // Check deadline
  let valDeadline = document.getElementById('deadline').value;
  if(valDeadline == ""){
    valDeadline = new Date(0,0,0);
  }

  fetch('/' + user_name + '/' + tablero_name + '/todos/add/', {
    method: 'POST',
    body: JSON.stringify({
      'description': document.getElementById('description').value,
      'deadline': valDeadline,
      'table_id': document.getElementById('table_id').dataset.curr_table_id
    }),
    headers: {
      'content-type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(res => {
    console.log(res)
		if(res['status'] == 'true') {
      listAllTable();
			document.getElementById("description").value = ""
			UIkit.notification({
				message: 'Todo created!',
				status: 'success',
				timeout: 3000
			});
		}
  })
  .catch(function(error) {
		UIkit.notification({
			message: 'Todo could not be created!',
			status: 'danger',
			timeout: 3000
		});
  });
}

function listAllTable() {
  fetch('/' + user_name + '/' + tablero_name + '/todos/displayall/',{
    method: 'POST',
    body: JSON.stringify({
      'table_id': document.getElementById('table_id').dataset.curr_table_id
    }),
    headers: {
      'content-type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(todos => {
      let tbodyAll = document.getElementById("tasks");
      tbodyAll.innerHTML = "";
      todos.forEach(todo => {
          fillRowTable(tbodyAll,todo);
      })
  })
}

function fillRowTable(tbodyAll,todo){
    let tdCheckbox = document.createElement('td');
    let checkbox = document.createElement('input');
    checkbox.type = "checkbox";
    checkbox.classList.add("uk-checkbox");
    tdCheckbox.appendChild(checkbox);

    let tdTodo = document.createElement('td');
    let inputTodo = document.createElement('input');
    inputTodo.value = todo['description'];
    inputTodo.disabled = true;
    inputTodo.type = "text"; 
    inputTodo.classList.add("uk-form-blank"); 
    tdTodo.appendChild(inputTodo);

    let tdDeadline = document.createElement('td');
    let inputDeadline = document.createElement('input');
    inputDeadline.classList.add("uk-form-blank");
    inputDeadline.type = "date";
    let valDeadline = todo['deadline'];
    var dead = new Date(valDeadline);
    if(dead.getDay() == 0){
      inputDeadline.disabled = true;
    }
    else{
      inputDeadline.disabled = true;
      dead.setDate(dead.getDate()+1);
      var dd = dead.getDate();
      var mm = dead.getMonth()+1; 
      var yyyy = dead.getFullYear();
      let date = yyyy + "-" + mm + "-" + dd;
      inputDeadline.value = date;    
    }
    let divAnimation = document.createElement("div");
    let spanDeadline = document.createElement("span");
    spanDeadline.classList.add("uk-label");
    spanDeadline.innerHTML = "Presione ENTER para guardar cambios";
    divAnimation.classList.add("uk-animation-slide-top");
    divAnimation.classList.add("hidden");
    divAnimation.appendChild(spanDeadline);
    tdDeadline.appendChild(inputDeadline);
    tdDeadline.appendChild(divAnimation); 


    let tdStatus = document.createElement('td');
    let pStatus = document.createElement('span');    
    if(todo.is_done == false){
      pStatus.classList.add("uk-label");
      pStatus.classList.add("uk-label-danger");
      pStatus.innerHTML = "Incompleted";
      checkbox.checked = false;
    }
    else{
      pStatus.classList.add("uk-label");
      pStatus.classList.add("uk-label-success");
      pStatus.innerHTML  = "Success";
      checkbox.checked = true;
    }
    tdStatus.appendChild(pStatus);

    let tdCreatedDate = document.createElement('td');
    let pCreatedDate = document.createElement('input');
    pCreatedDate.classList.add("uk-form-blank")
    pCreatedDate.type = "date";
    var d = new Date(todo['created_date']);
    var dd_ = d.getDate();
    var mm_ = d.getMonth()+1; 
    var yyyy_ = d.getFullYear();
    let date_ = yyyy_ + "-" + mm_ + "-" + dd_;
    pCreatedDate.value = date_;
    pCreatedDate.disabled = true;
    tdCreatedDate.appendChild(pCreatedDate);
    
    

    let tdOptions = document.createElement('td');
    let editButton = document.createElement('i');
    editButton.setAttribute("class", "far fa-edit");
    editButton.style.margin = '0 5px 0 2px';
    let removeButton = document.createElement('i');
    removeButton.setAttribute("class", "far fa-trash-alt");
    removeButton.style.margin = '0 5px 0 2px';
    let calendarButton = document.createElement('i');
    calendarButton.setAttribute("uk-icon", "icon: calendar");
    calendarButton.style.margin = '0 5px 0 2px';
    tdOptions.appendChild(editButton);
    tdOptions.appendChild(removeButton);
    tdOptions.appendChild(calendarButton);

    let trTodo = document.createElement('tr');
    trTodo.dataset.todoid = todo['id'];
    trTodo.classList.add("row_table");
    
    tbodyAll.appendChild(trTodo);
    trTodo.appendChild(tdCheckbox)
    trTodo.appendChild(tdTodo);
    trTodo.appendChild(tdDeadline);
    trTodo.appendChild(tdStatus);
    trTodo.appendChild(tdCreatedDate);
    trTodo.appendChild(tdOptions);

    checkbox.onclick =function() {updateTodo(todo,trTodo,checkbox,pStatus,todo.is_done,inputDeadline)};    
    editButton.addEventListener('click', () => this.editTodo(inputTodo,trTodo,todo.is_done));
    removeButton.addEventListener('click', () => this.removeTodo(tbodyAll,trTodo));
    calendarButton.addEventListener('click', () => this.editDeadline(inputDeadline, trTodo,divAnimation));  
}

function removeTodo(tbody,trTodo){
  fetch('/' + user_name + '/' + tablero_name + '/todos/delete/',{
    method: 'POST',
    body: JSON.stringify({
      'todo_id': trTodo.dataset.todoid
    }),
    headers: {
      'content-type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(res => {
    tbody.removeChild(trTodo);
  })
}


function editDeadline(inputDeadline, trTodo,divAnimation){
  inputDeadline.disabled = !inputDeadline.disabled; 
  divAnimation.classList.remove("hidden");
  inputDeadline.addEventListener('keydown', function(event){
    if(event.which == 13){
      divAnimation.classList.add("hidden");
      inputDeadline.disabled = !inputDeadline.disabled;
      let deadline_val = inputDeadline.value;
      console.log("edit todo")
      fetch('/' + user_name + '/' + tablero_name + '/todos/editdeadline/' ,{
        method: 'POST',
        body: JSON.stringify({
          'todo_id': trTodo.dataset.todoid,
          'deadline': deadline_val
        }),
        headers: {
          'content-type': 'application/json'
        }
      })
      .then(response => response.json())
    }

  })

}

function editTodo(inputTodo, trTodo){
  inputTodo.disabled = !inputTodo.disabled; 
  inputTodo.addEventListener('keydown', function(event){
    
    if(event.which == 13){

      inputTodo.disabled = !inputTodo.disabled;
      let todo_val = inputTodo.value;
      console.log("edit todo")
      fetch('/' + user_name + '/' + tablero_name + '/todos/update/' ,{
        method: 'POST',
        body: JSON.stringify({
          'todo_id': trTodo.dataset.todoid,
          'description': todo_val
        }),
        headers: {
          'content-type': 'application/json'
        }
      })
      .then(response => response.json())
    }

  })

}


function updateTodo(todo,trTodo,checkbox,pStatus,is_done,inputDeadline){
  if(is_done){
    todo.is_done = false;
    checkbox.checked = false;
    pStatus.innerHTML = "Incompleted";
    pStatus.classList.remove("uk-label-success");
    pStatus.classList.add("uk-label-danger");
  }
  else{
    todo.is_done = true;
    checkbox.checked = true;
    pStatus.innerHTML = "Success";
    pStatus.classList.remove("uk-label-danger");
    pStatus.classList.add("uk-label-success");
  }
  fetch('/' + user_name + '/' + tablero_name + '/todos/update_is_done/',{
    method: 'POST',
    body: JSON.stringify({
      'todo_id': trTodo.dataset.todoid
    }),
    headers: {
      'content-type': 'application/json'
    }
  })
  .then(response => response.json())
}


var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; 
var yyyy = today.getFullYear();
if(dd<10){
  dd='0'+dd
} 
if(mm<10){
  mm='0'+mm
}
today = yyyy+'-'+mm+'-'+dd;
document.getElementById("deadline").setAttribute("min", today);