

document.querySelectorAll('.close-btn').forEach((button)=>{

    button.addEventListener('click', function(e){
        console.log('clicked')
        
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
    console.log('clicked')
    //this.style.display = 'none'
    document.querySelector('input[type="file"]').click();
    //document.querySelector('.profile-img div span').style.display='inline';

})


// document.querySelector('.fa-solid.fa-xmark').addEventListener('click', function(e){
//     document.querySelector('.fa-pen').style.display = 'inline';
//     document.querySelector('.profile-img div span').style.display='none';
// })


// document.querySelector('.fa-solid.fa-check').addEventListener('click', function(e){
//     console.log('clicked')
//     document.querySelector('button[type="submit"]').click();
// })



document.querySelector('input[type="file"]').addEventListener('change', function(e){
    console.log(e.target)
    console.log(e.target.files[0])
    document.querySelector('button[type="submit"]').click();
})