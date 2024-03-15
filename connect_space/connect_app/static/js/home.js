
// post link click

document.querySelector('.post-link').addEventListener('click', function(e){
    this.querySelector('a').click();
})


// people section height 

document.querySelector('.people-section .view-more-btn').addEventListener('click', function(e){
    e.preventDefault();
    e.stopPropagation();
    console.log('clicked');
    
    document.querySelector('#all-people').classList.toggle('view-more');
    this.innerText = 'View less'
    if ( document.querySelector('#all-people').classList.contains('view-more')) {
        this.innerText = 'View less'
    } else {
        this.innerText = 'View more'
    }

});





// following button

document.querySelectorAll('.follow-btn').forEach((eachBtn)=>{
    eachBtn.addEventListener('click', function(e){
        console.log('clicked')
    })
})


// story section
if (document.querySelector('.card.user-story-card')){
    document.querySelector('.card.user-story-card').addEventListener('click', function(e){
        e.stopPropagation();
        document.querySelector('.user-story-active-div').classList.add('active')
        document.querySelector('.user-story-active-div').classList.remove('hidden')
        
    })
}
if(document.querySelector('.user-story-active-div .story-div i.fa-solid.fa-circle-xmark')) {
    document.querySelector('.user-story-active-div .story-div i.fa-solid.fa-circle-xmark').addEventListener('click', function(e){
        e.stopPropagation();
        document.querySelector('.user-story-active-div').classList.replace('active', 'hidden');
        
})
}

if(document.querySelector('.story-active-div .story-div i.fa-solid.fa-circle-xmark')) {
    document.querySelectorAll('.story-active-div .story-div i.fa-solid.fa-circle-xmark').forEach(function(btn){
        btn.addEventListener('click', function(e){
            e.stopPropagation();
            elemId=document.querySelector('.story-active-div.active').getAttribute('id')
            //console.log(elemId)
            document.querySelector(`#${elemId}`).classList.replace('active', 'hidden')
 
        })
    })
}


// document.querySelector('.user-story-active-div .story-div i.fa-solid.fa-chevron-left').addEventListener('click', function(e){
//     e.stopPropagation();
//     //document.querySelector('.user-story-active-div .story-div .story-detail-outter').scrollBy({top:0, left:-300, behavior:"smooth"})
    
//     //console.log(window.getComputedStyle(document.querySelector('.user-story-active-div .story-div .story-detail-outter .story-details')).width)
    
//     scrollWidth = (window.getComputedStyle(document.querySelector('.user-story-active-div .story-div .story-detail-outter .story-details')).width)
    
//     parsedWidth = parseInt(scrollWidth.replace('px', ''))
//     //console.log(typeof scrollWidth)
//     //console.log(parseInt(scrollWidth.replace('px', '')))
//     document.querySelector('.user-story-active-div .story-div .story-detail-outter').scrollBy({top:0, left:-`${parsedWidth}`, behavior:"smooth"})
// })

// document.querySelector('.user-story-active-div .story-div i.fa-solid.fa-chevron-right').addEventListener('click', function(e){
//     e.stopPropagation();
//     scrollWidth = (window.getComputedStyle(document.querySelector('.user-story-active-div .story-div .story-detail-outter .story-details')).width)
//     parsedWidth = parseInt(scrollWidth.replace('px', ''))
//     document.querySelector('.user-story-active-div .story-div .story-detail-outter').scrollBy({top:0, left:`${parsedWidth}`, behavior:"smooth"})
// })

if(document.querySelector('.post-story-btn')) {
    document.querySelector('.post-story-btn').addEventListener('click', function(e){
        e.stopPropagation()
    })
}

if(document.querySelector('.card.story-card')) {
    document.querySelectorAll('.card.story-card').forEach(function(item){
        item.addEventListener('click', function(e){
            e.stopPropagation();

            console.log(item.dataset.userId)

            document.querySelector(`#user${item.dataset.userId}`).classList.add('active')
            document.querySelector(`#user${item.dataset.userId}`).classList.remove('hidden')
            
        })
    })
    
}