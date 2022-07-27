window.addEventListener('load', (event) => {
    console.log('page is fully loaded');
    function getProjects(){
        fetch('http://localhost:5000/projects')
        .then(response => response.json()) 
        .then(data=>{
            console.log(data)
            var projectsTable = document.getElementById("projects"); 
            for(let i=0; i<data.length; i++){
                let row = document.createElement("tr"); 

                let projectName = document.createElement('td'); 
                projectName.innerHTML = data[i].name;
                row.appendChild(projectName); 

                let projectDesc = document.createElement('td'); 
                projectDesc.innerHTML = data[i].description; 
                row.appendChild(projectDesc);

                let projectActions = document.createElement('td')
                projectActions.innerHTML = '<a href="/show/project/{{project_id}}">Details</a>'
                row.appendChild(projectActions);

                projectsTable.appendChild(row);
            }
        })
    }
    getProjects();


// submit form, update table with last recipe, clear form without redirecting!
var myForm = document.getElementById('myForm'); 
    myForm.onsubmit = function(e){ 
        e.preventDefault(); 
        var form = new FormData(myForm); 
        fetch("http://localhost:5000/addProject", { method :'POST', body : form})
                .then( response => response.json() )
                .then( data =>{
                    console.log(data)
                    updateTable(data); 
                    myForm.reset(); 
                })
    }
    function updateTable(data){
        var projectsTable = document.getElementById("projects"); 
        let row = document.createElement("tr"); 

        let projectName = document.createElement('td'); 
        projectName.innerHTML = data.name;
        row.appendChild(projectName); 

        let projectDesc = document.createElement('td'); 
        projectDesc.innerHTML = data.description; 
        row.appendChild(projectDesc);

        let projectActions = document.createElement('td')
        projectActions.innerHTML = '<a href="/show/project/">Details</a>'
        row.appendChild(projectActions);

        projectsTable.appendChild(row);
    }
    updateTable();
    });


    const myModal = document.getElementById('myModal')
    const myInput = document.getElementById('myInput')
    
    myModal.addEventListener('shown.bs.modal', () => {
      myInput.focus()
    })


