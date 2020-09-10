function edit(postid){
    document.querySelectorAll(`.btn${postid}`).forEach(button => {
        button.onclick = () => {
            document.querySelectorAll(`.form${postid}`).forEach(div => {                
                if(button.class == div.class){
                    if(div.style.display === "none"){
                        div.style.display = "block";
                    }else{
                        div.style.display = "none";
                    }                    
                }else{
                    div.style.display = "none";
                }  
            });          
        }      
    });
}
// let counter = 0;
// function like(){
//     counter++;
//     document.querySelector("#app").innerHTML = counter;
// }

function like(id) {

    fetch(`like/${id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result.result.html);
        document.getElementById(`heart-${id}`).innerHTML = result.result.html
        document.getElementById(`likes-${id}`).innerHTML = result.result.likes
    });
}


