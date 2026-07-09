const aadhaarInput = document.getElementById("aadhaar");
const selfieInput = document.getElementById("selfie");

const aadhaarPreview = document.getElementById("aadhaarPreview");
const selfiePreview = document.getElementById("selfiePreview");

const verifyBtn = document.getElementById("verifyBtn");

const loading = document.getElementById("loading");
const result = document.getElementById("result");


// -------------------------------
// Image Preview
// -------------------------------

aadhaarInput.onchange = function () {

    if (this.files.length === 0) return;

    aadhaarPreview.src = URL.createObjectURL(this.files[0]);

    aadhaarPreview.style.display = "block";

};

selfieInput.onchange = function () {

    if (this.files.length === 0) return;

    selfiePreview.src = URL.createObjectURL(this.files[0]);

    selfiePreview.style.display = "block";

};


// -------------------------------
// Verify Button
// -------------------------------

verifyBtn.onclick = async function () {

    if (aadhaarInput.files.length === 0) {

        alert("Select Aadhaar Image");

        return;

    }

    if (selfieInput.files.length === 0) {

        alert("Select Selfie");

        return;

    }

    loading.style.display = "block";

    result.style.display = "none";

    verifyBtn.disabled = true;

    verifyBtn.innerHTML = "Verifying...";

    const form = new FormData();

    form.append("aadhaar", aadhaarInput.files[0]);

    form.append("selfie", selfieInput.files[0]);

    try {

        const response = await fetch(

            "http://127.0.0.1:8000/verify",

            {

                method: "POST",

                body: form

            }

        );

        if (!response.ok) {

            throw new Error("Server Error");

        }

        const data = await response.json();

        showResult(data);

    }

    catch (error) {

        console.error(error);

        alert("Cannot connect to FastAPI Backend");

    }

    finally {

        loading.style.display = "none";

        verifyBtn.disabled = false;

        verifyBtn.innerHTML = "Verify Aadhaar";

    }

};


// -------------------------------
// Show Result
// -------------------------------

function showResult(data){

    result.style.display="block";

    document.getElementById("status").innerHTML =
        data.status=="PASS"
        ? "<span class='success'>✔ VERIFIED</span>"
        : "<span class='fail'>✖ FAILED</span>";

    document.getElementById("confidence").innerHTML =
        data.confidence+"%";

    document.getElementById("name").innerHTML =
        data.aadhaar.name ?? "-";

    document.getElementById("dob").innerHTML =
        data.aadhaar.dob ?? "-";

    document.getElementById("gender").innerHTML =
        data.aadhaar.gender ?? "-";

    document.getElementById("aadhaarNumber").innerHTML =
        data.aadhaar.aadhaar_number ?? "-";

    document.getElementById("quality").innerHTML =
        data.image_quality.status;

    document.getElementById("similarity").innerHTML =
        data.face.similarity+"%";

    document.getElementById("tampering").innerHTML =
        data.tampering.tampered
        ? "<span class='fail'>Detected</span>"
        : "<span class='success'>Not Detected</span>";

}


// -------------------------------
// Download Report
// -------------------------------

document.getElementById("downloadBtn").onclick = function () {

    const report = {

        status:
            document.getElementById("status").innerText,

        confidence:
            document.getElementById("confidence").innerText,

        name:
            document.getElementById("name").innerText,

        dob:
            document.getElementById("dob").innerText,

        gender:
            document.getElementById("gender").innerText,

        aadhaar:
            document.getElementById("aadhaarNumber").innerText,

        similarity:
            document.getElementById("similarity").innerText,

        tampering:
            document.getElementById("tampering").innerText

    };

    const blob = new Blob(

        [

            JSON.stringify(

                report,

                null,

                4

            )

        ],

        {

            type: "application/json"

        }

    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "verification_report.json";

    a.click();

    URL.revokeObjectURL(url);

};