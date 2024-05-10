// linkify link
const options = { defaultProtocol: "https" };
document.querySelectorAll(".post-content").forEach((post)=>{
    text = post.innerHTML
    // console.log(text)
    newText = linkifyHtml(
        text,
        options
      );
    post.innerHTML = newText
    post.querySelector("a").style.color="darkblue"
    linkText = post.querySelector("a").innerHTML
    
    linkText.length>20 ? linkText=linkText.slice(0, 30) + "...": ""

    post.querySelector("a").innerHTML = linkText
    post.querySelector('a').setAttribute("target", "_blank");
})