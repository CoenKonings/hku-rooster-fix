{
    let tracks = [];
    let courses = [];

    Array.prototype.forEach.call(document.getElementsByClassName("track-checkbox"), trackCheckbox => {
        trackCheckbox.checked = false;

        const updateCourses = () => {
            Array.prototype.forEach.call(document.getElementsByClassName("course-selector"), courseSelector => {
                courseTracks = courseSelector.getAttribute("tracks")

                if (tracks.length === 0) {
                    courseSelector.style.display = "block";
                } else if (courseTracks.split(",").some(track => tracks.includes(track)) || courseTracks === "") {
                    courseSelector.style.display = "block";
                } else {
                    courseSelector.style.display = "none";
                }
            });
        }

        trackCheckbox.addEventListener("change", (event) => {
            if (event.target.checked) {
                tracks.push(event.target.name.split("-")[1]);
            } else {
                tracks = tracks.filter(track => track !== event.target.name.split("-")[1]);
            }

            updateCourses();
        });
    });

    Array.prototype.forEach.call(document.getElementsByClassName("course-checkbox"), courseCheckbox => {
        courseCheckbox.checked = false;

        courseCheckbox.addEventListener("change", event => {
            const courseId = event.target.id.split("-")[1];

            if (event.target.checked) {
                courses.push(courseId);
            } else {
                courses = courses.filter(course => course !== courseId);
            }
        });
    });

    const getIcalLink = async requestBody => {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        fetch("/", {
            method: "POST",
            body: JSON.stringify(requestBody),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": csrftoken
            }
        })
            .then(response => response.json())
            .then(json => {
                document.getElementById("calendar-link").innerHTML = json.icalUrl;
                document.getElementById("calendar-form").style.display = "none";
                document.getElementById("calendar-link-display").style.display = "block";
            });
    };

    document.getElementById("submit-button").addEventListener("click", event => {
        if (courses.length === 0) {
            alert("Selecteer minstens 1 vak");
            return;
        }

        const requestBody = []

        courses.forEach(course => {
            const courseObj = {id: course, group: ""};
            const groupSelect = document.getElementById(`group-course-${course}`);

            if (groupSelect) {
                courseObj.group = groupSelect.value;
            }

            requestBody.push(courseObj);
        });

        getIcalLink(requestBody);
    });
}


