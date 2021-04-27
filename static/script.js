function openForm() {
    document.getElementById("div_file_upload").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("div_file_upload").style.display = "none";
  }

  
// Input CSV File __________________________________________________________________________________________________________
const realFileBtn = document.getElementById("real-file")
const chooseFileBtn = document.getElementById("choose-file-button")
const chooseFileTxt = document.getElementById("choose-file-text")
var currFileName = "No file choosen"
chooseFileBtn.addEventListener("click", function(){
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function(){
    if (realFileBtn.value) {
        currFileName = realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    }
    chooseFileTxt.innerHTML = currFileName;
});
