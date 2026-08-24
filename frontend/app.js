// Point this to your local FastAPI server
const API_BASE_URL = "http://127.0.0.1:8000/api/v1/auth";

async function requestOTP() {
    const mobileNumber = document.getElementById("mobile").value;
    const statusText = document.getElementById("status-message");

    try {
        const response = await fetch(`${API_BASE_URL}/request-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mobile_number: mobileNumber })
        });

        const data = await response.json();

        if (response.ok) {
            // Hide phone input, show OTP input
            document.getElementById("step-1-phone").style.display = "none";
            document.getElementById("step-2-otp").style.display = "block";
            statusText.innerText = "OTP sent successfully! Check your terminal.";
            statusText.style.color = "green";
        } else {
            statusText.innerText = data.detail[0].msg || "Invalid phone number.";
            statusText.style.color = "red";
        }
    } catch (error) {
        statusText.innerText = "Server error. Is your FastAPI backend running?";
        statusText.style.color = "red";
    }
}

async function verifyOTP() {
    const mobileNumber = document.getElementById("mobile").value;
    const otpCode = document.getElementById("otp").value;
    const statusText = document.getElementById("status-message");

    try {
        const response = await fetch(`${API_BASE_URL}/verify-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mobile_number: mobileNumber, otp: otpCode })
        });

        const data = await response.json();

        if (response.ok) {
            // Securely store the JWT in the browser
            localStorage.setItem("gramin_jwt", data.access_token);
            
            document.getElementById("step-2-otp").style.display = "none";
            statusText.innerText = "Login Successful! Token saved securely.";
            statusText.style.color = "green";
            
            console.log("Your JWT:", data.access_token);
        } else {
            statusText.innerText = data.detail || "Invalid OTP.";
            statusText.style.color = "red";
        }
    } catch (error) {
        statusText.innerText = "Server error during verification.";
        statusText.style.color = "red";
    }
}
async function registerFarmer(event) {
    event.preventDefault(); // Prevents the page from reloading
    
    // Gather data from the form
    const profileData = {
        full_name: document.getElementById("reg-name").value,
        aadhaar_hash: document.getElementById("reg-aadhaar").value, // In reality, we'd hash this on the client or server
        mobile_number: document.getElementById("reg-mobile").value,
        land_holding_hectares: parseFloat(document.getElementById("reg-land").value),
        village_name: document.getElementById("reg-village").value
    };

    const statusText = document.getElementById("status-message");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/farmers/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(profileData)
        });

        const data = await response.json();

        if (response.ok) {
            statusText.innerText = "Registration Successful! You can now log in.";
            statusText.style.color = "green";
            // Optionally, switch the view back to the OTP login screen here
        } else {
            statusText.innerText = data.detail || "Registration failed.";
            statusText.style.color = "red";
        }
    } catch (error) {
        statusText.innerText = "Server error during registration.";
        statusText.style.color = "red";
    }
}