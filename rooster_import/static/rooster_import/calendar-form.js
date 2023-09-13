{
    let tracks = [];
    let courses = [];
    let groups = [];

    Array.prototype.forEach.call(document.getElementsByClassName("track-selector"), trackSelector => {
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

        trackSelector.addEventListener("change", (event) => {
            if (event.target.checked) {
                tracks.push(event.target.name.split("-")[1]);
            } else {
                tracks = tracks.filter(track => track !== event.target.name.split("-")[1]);
            }

            updateCourses();
        });
    });

    Array.prototype.forEach.call(document.getElementsByClassName("course-checkbox"), courseCheckbox => {
        courseCheckbox.addEventListener("change", event => {
            const courseId = event.target.id.split("-")[1];
            const groupSelect = document.getElementById(`group-course-${courseId}`);

            if (event.target.checked) {
                courses.push(courseId);

                if (groupSelect) {
                    groupSelect.style.display = "inline";
                }
            } else {
                courses = courses.filter(course => course !== courseId);

                if (groupSelect) {
                    groupSelect.style.display = "none";
                }
            }
        });
    });

    Array.prototype.forEach.call(document.getElementsByClassName("group-select"), groupSelect => {
        if (!courses.includes(groupSelect.id.split("-")[2])) {
            groupSelect.style.display = "none";
        }

        groupSelect.addEventListener("change", event => {
            const prevValue = event.target.getAttribute("prevValue");
            if (prevValue) {
                groups = groups.filter(group => group !== prevValue);
            }

            groups.push(event.target.value);
            event.target.setAttribute("prevValue", event.target.value);

            console.log(groups);
        });
    });
}


