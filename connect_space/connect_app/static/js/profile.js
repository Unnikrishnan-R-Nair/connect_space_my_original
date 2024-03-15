

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

document.querySelector('.fa-pen').addEventListener('click', function(e){
    // console.log('clicked')
    //this.style.display = 'none'
    document.querySelector('input[type="file"]').click();
    //document.querySelector('.profile-img div span').style.display='inline';

})




// change event on file select
document.querySelector('input[type="file"]').addEventListener('change', function(e){
    
    document.querySelector('button[type="submit"]').click();
})

