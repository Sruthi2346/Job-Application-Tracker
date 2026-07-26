const API_URL = "https://job-application-tracker-ba5l.onrender.com";

async function loginUser() {

    const email = document
        .getElementById("email")
        .value
        .trim();

    const password = document
        .getElementById("password")
        .value
        .trim();

    if (email === "" || password === "") {

        alert("Please fill all fields.");

        return;

    }

    const data = {

        email,
        password

    };

    try {

        const response = await fetch(

            `${API_URL}/login`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(data)

            }

        );

        const result = await response.json();

        if (!response.ok) {

            alert(result.detail);

            return;

        }

        localStorage.setItem(
            "token",
            result.access_token
        );

        alert("Login Successful!");

        window.location.href = "index.html";

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to backend.");

    }

}