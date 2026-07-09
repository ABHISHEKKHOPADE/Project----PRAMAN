const aadhaar = document.getElementById("aadhaar");
const selfie = document.getElementById("selfie");

const aadhaarPreview = document.getElementById("aadhaarPreview");
const selfiePreview = document.getElementById("selfiePreview");

aadhaar.onchange = function(){

    aadhaarPreview.src = URL.createObjectURL(this.files[0]);

    aadhaarPreview.style.display = "block";

}

selfie.onchange = function(){

    selfiePreview.src = URL.createObjectURL(this.files[0]);

    selfiePreview.style.display = "block";

}