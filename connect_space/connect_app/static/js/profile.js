

document.querySelectorAll('.close-btn').forEach((button)=>{

    button.addEventListener('click', function(e){
        // console.log('clicked')
        
        document.querySelectorAll('.alert-message').forEach((item)=>{
            
            item.remove();
            
        })
    })
})



// setTimeout(function messageTimer(){
//     document.querySelectorAll('.close-btn').forEach((btn)=>{
//         btn.click;
//     })
// }, 2000)

document.querySelector('.fa-pen.profile-image-edit').addEventListener('click', function(e){
    // console.log('clicked')
    //this.style.display = 'none'
    document.querySelector('input[name="image"]').click();
    //document.querySelector('.profile-img div span').style.display='inline';

})


document.querySelector('.fa-pen.cover-image-edit').addEventListener('click', function(e){
    document.querySelector('input[name="cover_image"]').click();
})


// change event on file select
document.querySelector('input[name="image"]').addEventListener('change', function(e){
    
    document.querySelector('button[type="submit"]').click();
})

document.querySelector('input[name="cover_image"]').addEventListener('change', function(e){
    
    document.querySelector('button[type="submit"]').click();
})
