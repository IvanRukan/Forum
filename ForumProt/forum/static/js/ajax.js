function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function edit_publication() {
    $.ajax({
        headers: {"X-CSRFToken": csrftoken},
        type: 'POST',
        url: '/edit_publication',
//        dataType: 'json',
//        contentType: 'application/json',
        data: {
            'id': document.getElementById('hidden_publication_id').value,
        },
        success: function (response) {
            console.log(response['id'])
           // window.location.href = '/edit_chosen_cat/' + response['ID']
        }
    });
}


function upvote_publication() {
    $.ajax({
        headers: {"X-CSRFToken": csrftoken},
        type: 'POST',
        url: '/publ_upvote',
//        dataType: 'json',
//        contentType: 'application/json',
        data: {
            'id': document.getElementById('hidden_publication_id').value,
            'user_id': document.getElementById('hidden_user_id').value,
        },
        success: function (response) {
            console.log(response['id'])
            window.location.href = '/publication?id=' + response['id']
        }
    });
}

