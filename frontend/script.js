const API_URL = "https://job-application-tracker-ba5l.onrender.com";

let applications = [];
let filteredApplications = [];

// ---------------- LOAD APPLICATIONS ----------------

async function loadApplications() {

    try {

        const response = await fetch(`${API_URL}/applications`);

        if (!response.ok) {
            throw new Error("Failed to fetch applications");
        }

        applications = await response.json();

        alert(JSON.stringify(applications));

        filteredApplications = [...applications];

        updateDashboard();

        displayApplications(filteredApplications);

    }
    catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML =
            "<h3>Unable to connect to backend.</h3>";

    }

}

// ---------------- ADD APPLICATION ----------------

async function addApplication() {

    const company = document.getElementById("company").value.trim();
    const role = document.getElementById("role").value.trim();
    const location = document.getElementById("location").value.trim();
    const status = document.getElementById("status").value;

    const applied_date = document.getElementById("appliedDate").value;
    const deadline_date = document.getElementById("deadlineDate").value;
    const interview_date = document.getElementById("interviewDate").value;
    const notes = document.getElementById("notes").value.trim();

    if (
        company === "" ||
        role === "" ||
        location === "" ||
        applied_date === ""
    ) {

        alert("Please fill all required fields.");

        return;

    }

    const data = {

        company,
        role,
        location,
        status,
        applied_date,
        deadline_date: deadline_date || null,
        interview_date: interview_date || null,
        notes

    };

    try {

        const response = await fetch(`${API_URL}/applications`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        if (!response.ok) {

            const error = await response.json();

            alert(error.detail);

            return;

        }

        clearForm();

        await loadApplications();

        alert("Application Added Successfully.");

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to backend.");

    }

}
// ---------------- DASHBOARD ----------------

function updateDashboard() {

    let applied = 0;
    let interview = 0;
    let selected = 0;
    let rejected = 0;

    applications.forEach(app => {

        switch (app.status) {

            case "Applied":
                applied++;
                break;

            case "Interview":
                interview++;
                break;

            case "Selected":
                selected++;
                break;

            case "Rejected":
                rejected++;
                break;

        }

    });

    document.getElementById("dashboard").innerHTML = `

    <div class="dashboard-grid">

        <div class="card total">
            Total<br>${applications.length}
        </div>

        <div class="card applied">
            Applied<br>${applied}
        </div>

        <div class="card interview">
            Interview<br>${interview}
        </div>

        <div class="card selected">
            Selected<br>${selected}
        </div>

        <div class="card rejected">
            Rejected<br>${rejected}
        </div>

    </div>

    `;

}

// ---------------- DISPLAY TABLE ----------------

function displayApplications(data) {

    if (data.length === 0) {

        document.getElementById("result").innerHTML =
            "<h3>No Applications Found</h3>";

        return;

    }

    let output = `

    <table>

        <tr>

            <th>Company</th>
            <th>Role</th>
            <th>Location</th>
            <th>Status</th>
            <th>Applied</th>
            <th>Deadline</th>
            <th>Interview</th>
            <th>Notes</th>
            <th>Actions</th>

        </tr>

    `;

    data.forEach(app => {

        console.log(app);

        output += `

        <tr>

            <td>${app.company}</td>

            <td>${app.role}</td>

            <td>${app.location}</td>

            <td>${app.status}</td>

            <td>${app.applied_date}</td>

            <td>${app.deadline_date ?? "-"}</td>

            <td>${app.interview_date ?? "-"}</td>

            <td>${app.notes ? app.notes : "-"}</td>

            <td>

                <button
                    class="edit-btn"
                    onclick="editApplication(${app.id})">

                    Edit

                </button>

                <button
                    class="delete-btn"
                    onclick="deleteApplication(${app.id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

    output += "</table>";

    document.getElementById("result").innerHTML = output;

}
// ---------------- SEARCH ----------------

function searchApplication() {

    const search = document
        .getElementById("search")
        .value
        .toLowerCase();

    filteredApplications = applications.filter(app =>
        app.company.toLowerCase().includes(search)
    );

    displayApplications(filteredApplications);

}

// ---------------- FILTER ----------------

function filterApplications() {

    const filter = document.getElementById("filter").value;

    if (filter === "All") {

        filteredApplications = [...applications];

    }

    else {

        filteredApplications = applications.filter(app =>
            app.status === filter
        );

    }

    displayApplications(filteredApplications);

}

// ---------------- SORT ----------------

function sortApplications() {

    const sort = document.getElementById("sort").value;

    if (sort === "companyaz") {

        filteredApplications.sort((a, b) =>
            a.company.localeCompare(b.company)
        );

    }

    else if (sort === "companyza") {

        filteredApplications.sort((a, b) =>
            b.company.localeCompare(a.company)
        );

    }

    else if (sort === "status") {

        const order = {

            Applied: 1,
            Interview: 2,
            Selected: 3,
            Rejected: 4

        };

        filteredApplications.sort((a, b) =>
            order[a.status] - order[b.status]
        );

    }

    else if (sort === "applied") {

        filteredApplications.sort(
            (a, b) =>
                new Date(b.applied_date) -
                new Date(a.applied_date)
        );

    }

    displayApplications(filteredApplications);

}
// ---------------- EDIT ----------------

function editApplication(id) {

    const app = applications.find(item => item.id === id);

    if (!app) return;

    document.getElementById("applicationId").value = app.id;

    document.getElementById("company").value = app.company;

    document.getElementById("role").value = app.role;

    document.getElementById("location").value = app.location;

    document.getElementById("status").value = app.status;

    document.getElementById("appliedDate").value =
        app.applied_date || "";

    document.getElementById("deadlineDate").value =
        app.deadline_date || "";

    document.getElementById("interviewDate").value =
        app.interview_date || "";

    document.getElementById("notes").value =
        app.notes || "";

    document.getElementById("saveBtn").innerHTML =
        "Update Application";

    document.getElementById("saveBtn").onclick =
        updateApplication;

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}
// ---------------- UPDATE ----------------

async function updateApplication() {

    const id = document.getElementById("applicationId").value;

    const data = {

        company: document.getElementById("company").value.trim(),
        role: document.getElementById("role").value.trim(),
        location: document.getElementById("location").value.trim(),
        status: document.getElementById("status").value,

        applied_date: document.getElementById("appliedDate").value,
        deadline_date:
            document.getElementById("deadlineDate").value || null,

        interview_date:
            document.getElementById("interviewDate").value || null,

        notes:
            document.getElementById("notes").value.trim()

    };

    if (
        data.company === "" ||
        data.role === "" ||
        data.location === "" ||
        data.applied_date === ""
    ) {

        alert("Please fill all required fields.");

        return;

    }

    try {

        const response = await fetch(

            `${API_URL}/applications/${id}`,

            {

                method: "PUT",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(data)

            }

        );

        if (!response.ok) {

            const error = await response.json();

            alert(error.detail);

            return;

        }

        clearForm();

        document.getElementById("saveBtn").innerHTML =
            "Add Application";

        document.getElementById("saveBtn").onclick =
            addApplication;

        await loadApplications();

        alert("Application Updated Successfully.");

    }

    catch (error) {

        console.error(error);

        alert("Unable to update application.");

    }

}
// ---------------- DELETE ----------------

async function deleteApplication(id) {

    const answer = confirm(
        "Are you sure you want to delete this application?"
    );

    if (!answer) return;

    try {

        await fetch(

            `${API_URL}/applications/${id}`,

            {

                method: "DELETE"

            }

        );

        await loadApplications();

        alert("Application Deleted Successfully.");

    }

    catch (error) {

        console.error(error);

        alert("Unable to delete application.");

    }

}

// ---------------- CLEAR FORM ----------------

function clearForm() {

    document.getElementById("applicationId").value = "";

    document.getElementById("company").value = "";

    document.getElementById("role").value = "";

    document.getElementById("location").value = "";

    document.getElementById("status").value = "Applied";

    document.getElementById("appliedDate").value = "";

    document.getElementById("deadlineDate").value = "";

    document.getElementById("interviewDate").value = "";

    document.getElementById("notes").value = "";

}
// ---------------- INITIAL LOAD ----------------

loadApplications();