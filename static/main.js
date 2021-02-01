let close = document.getElementById('close');
const form = document.getElementById('form');
const success = document.getElementById('success');
const error = document.getElementById('error');
const checkbox = document.querySelectorAll('.check-boolean');
const deleteBtn = document.querySelectorAll('.delete-btn');

checkbox.forEach(e => {
    const post = e.dataset.id;
    e.onchange = click => {
        console.log('event', click, post);
        const completed = click.target.checked;
        fetch(`/update-completed/${post}`, {
            method:'POST',
            body:JSON.stringify({
                'completed': completed
            }),
            headers:{
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log(response);
        })
        .catch(errors => {
            console.log(errors);
        })
    }
});

deleteBtn.forEach(item => {
    const post = item.dataset.id;
    item.onclick = () => {
        fetch(`/delete-ajax/${post}`, {
            method:'DELETE'
        });
    }
});

if (close !== null){
    close.onclick = function(){
        if (success !== null){
            success.style.display = 'none';
        } else {
            error.style.display = 'none';
        }
    }
}

if (form !== null){
    form.onsubmit = function(e){
        e.preventDefault();  
        
        fetch('/create_js', {
            method:'POST',
            body:JSON.stringify({
                'content':document.getElementById('content').value,
                'description':document.getElementById('description').value
            }),
            headers:{
                'Content-Type':'application/json'
            }
        })
        .then(response =>{
            return response.json();
        })
        .then(json => {
            console.log(json);  
            let tags = `<tr>
                     <td><input class="check-boolean" data-id={{ ${json['id']} }} type="checkbox" {% if ${json['completed']} %} checked {% endif %}></td>
              <td>
                  <button style="color: red;" type="button" data-id="{{ ${json['id']} }}" class="close delete-btn" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
              </td>
              <td scope="row">{{ ${json['id']} }}</td>
              <td>{{ ${json['content']} }}</td>
              <td>{{ ${json['description']} }}</td>
              <td>{{ post.created_at.date() }}</td>
              <td>
                <a href="/update/{{ ${json['id']} }}" class="btn btn-primary">Update</a>
                <a type="submit" href="/delete/{{ ${json['id']} }}" onclick="event.preventDefault(); 
                                                        document.getElementById('delete-'+this.dataset.del).submit();" id="del" data-del="{{ ${json['id']} }}" class="btn btn-danger">Delete</a>
                <form  action="/delete/{{ ${json['id']} }}" method="POST" style="display: none;"  id="delete-{{ ${json['id']} }}">
                </form>
              </td></tr>
            `;
            document.getElementById('posts').appendChild(tdItem);
        })
        .catch(error => {
            console.error(error);
        });
    }
}
