{
    let tracks = [];

    Array.prototype.forEach.call(document.getElementsByClassName("track-selector"), trackSelector => {
        const updateCourses = () => {
            Array.prototype.forEach.call(document.getElementsByClassName("course-selector"), courseSelector => {
                if (tracks.length === 0) {
                    courseSelector.style.display = "block";
                } else if (courseSelector.getAttribute("tracks").split(",").some(track => tracks.includes(track))) {
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

            console.log(tracks)
            updateCourses();
        });
    });
}


