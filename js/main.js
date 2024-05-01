$(function(){
if (window.location.pathname === "/addvideo" && myuserid.innerHTML === "") {
alert("pas connecté-e vous allez être redirigé(e)")
window.location="/sign_in";

}
if (document.getElementById("editmypost")){

document.getElementById("members").onchange = function() {

        
        if(editmypost.value !== ""){

            

            editmypost.onfocus = function () {
                var myvalue = (document.getElementById("members").value).toLowerCase();
                var hi = editmypost.value.toLowerCase().indexOf(myvalue);

                if (hi !== -1){
                    console.log(hi,myvalue.length);

                editmypost.setSelectionRange(hi, (hi+myvalue.length));
                editmypost.onfocus = undefined;
document.getElementById("message").innerHTML="";
                }else{
document.getElementById("message").innerHTML="le membre n'a pas été trouvé";

                }
            } 
            editmypost.focus();        
            
        }   

    }
    }
if (document.getElementById("link")){
link.onchange = () => {
if (link.value !== ""){
  var textarea=document.getElementById("editmypost");
  if (textarea.selectionStart !== textarea.selectionEnd){
  let first = textarea.value.slice(0, textarea.selectionStart);
  let rest = textarea.value.slice(textarea.selectionEnd, textarea.value.length);

  textarea.value = first + link.value + rest;

  // Bonus: place cursor behind replacement
  textarea.selectionEnd = (first + link.innerText).length;
};
link.value="";
members.value="";
};
};
};

});
$(document).ready(function () {
      $('.someselect').selectize({
          sortField: 'text'
      });
  });

