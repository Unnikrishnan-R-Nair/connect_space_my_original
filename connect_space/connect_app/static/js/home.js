
// post link click

document.querySelector('.post-link').addEventListener('click', function(e){
    this.querySelector('a').click();
})


// people section height 

document.querySelector('.people-section .view-more-btn').addEventListener('click', function(e){
    console.log('clicked')
})

// story section scroll

document.querySelector('.left-slide-btn').addEventListener('click', function(e){
    console.log('clicked')

    document.querySelector('.story-div').scrollBy({top:0, left:-100, behavior:"smooth"})
})

document.querySelector('.right-slide-btn').addEventListener('click', function(e){
    console.log('clicked')
    document.querySelector('.story-div').scrollBy({top:0, left:100, behavior:"smooth"})
})

// following button

document.querySelectorAll('.follow-btn').forEach((eachBtn)=>{
    eachBtn.addEventListener('click', function(e){
        console.log('clicked')
    })
})


// search





// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');



// Json Response

// document.querySelector('.like-btn').forEach((eachBtn)=>{
//     eachBtn.addEventListener('click', function(e){
//         location.reload();

//         $.ajax({
//             type:'POST',
//             url: '{% url "like-dislike-post" %}',
//             data: {
//                 post_id: data['index'].text,
//             }
//         })
//     })
// })