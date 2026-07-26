const API_URL = "http://127.0.0.1:8000";

async function registerUser() {

    const username = document
        .getElementById("username")
        .value
        .trim();

    const email = document
        .getElementById("email")
        .value
        .trim();

    const password = document
        .getElementById("password")
        .value
        .trim();

    if (
        username === "" ||
        email === "" ||
        password === ""
    ) {

        alert("Please fill all fields.");

        return;

    }

    const data = {

        username,
        email,
        password

    };

    try {

        const response = await fetch(

            `${API_URL}/register`,

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

        alert("Registration Successful!");

        window.location.href = "login.html";

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to backend.");

    }

}