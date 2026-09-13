// ===============================
// Sidebar Navigation (Dashboard / Projects / etc.)
// ===============================

const sidebarItems = document.querySelectorAll(".sidebar li[data-page]");
const pages = document.querySelectorAll(".page");

sidebarItems.forEach((item) => {

    item.addEventListener("click", () => {

        const targetPage = item.getAttribute("data-page");

        // Sidebar active state update
        sidebarItems.forEach((li) => li.classList.remove("active"));
        item.classList.add("active");

        // Page switch
        pages.forEach((page) => {
            page.style.display = (page.id === `page-${targetPage}`) ? "flex" : "none";
        });

        // Jab "Projects" page khule, list render kar do
        if (targetPage === "projects" && typeof renderProjects === "function") {
            renderProjects();
        }

    });

});


// ===============================
// Monaco Editor Setup
// ===============================
// NOTE: Monaco loads from a CDN (loader.min.js). If that CDN is slow,
// blocked, or down, `require` won't exist and calling it directly would
// throw and stop the REST of this file from running (including the
// Projects page search/filter code below). Wrapping this in a
// try/catch keeps everything else on the page working even if the
// editor itself can't load.

let editor;
let isRunning = false;

try {

    if (typeof require === "undefined") {
        throw new Error("Monaco loader script did not load (CDN unreachable).");
    }

    require.config({
        paths: {
            vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs"
        }
    });

    require(["vs/editor/editor.main"], function () {

        editor = monaco.editor.create(
            document.getElementById("editor"),
            {

                value: `# Write your Python code here...

print("Hello World")
`,

                language: "python",

                theme: "vs-dark",

                automaticLayout: true,

                fontSize: 16,

                minimap: {
                    enabled: false
                }

            }
        );

    }, function (err) {

        console.error("Monaco module failed to load:", err);

        const editorEl = document.getElementById("editor");
        if (editorEl) {
            editorEl.innerHTML = `<p style="color:#f87171;padding:15px;">⚠ Code editor failed to load. Check your internet connection and refresh.</p>`;
        }

    });

} catch (err) {

    console.error("Monaco setup failed, editor will be unavailable:", err);

    const editorEl = document.getElementById("editor");
    if (editorEl) {
        editorEl.innerHTML = `<p style="color:#f87171;padding:15px;">⚠ Code editor failed to load. Check your internet connection and refresh.</p>`;
    }

}



// ===============================
// HTML Elements
// ===============================


const runBtn = document.getElementById("runBtn");

const language = document.getElementById("language");

const output = document.getElementById("output");

const explanation = document.getElementById("explanation");

const suggestions = document.getElementById("aiSuggestions");

const errorFix = document.getElementById("errorFix");




// ===============================
// Language Change
// ===============================


language.addEventListener("change", () => {


    if(editor){


        monaco.editor.setModelLanguage(
            editor.getModel(),
            language.value
        );


    }


});




// ===============================
// Run Button
// ===============================


runBtn.addEventListener("click", async () => {



    if(isRunning){

        return;

    }



    if(!editor){

        output.textContent = "Editor loading...";

        return;

    }



    isRunning = true;


    output.textContent = "Running...";

    explanation.textContent = "";

    suggestions.textContent = "";

    errorFix.textContent = "";




    try{


        const controller = new AbortController();


        const timeout = setTimeout(() => {

            controller.abort();

        },10000);




        const response = await fetch(
            "https://ai-smart-compiler-3.onrender.com/compile",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    code: editor.getValue(),
                    language: language.value
                }),

                signal: controller.signal
            }
        );


        clearTimeout(timeout);



        const result = await response.json();



        console.log(result);



        const data = result.result;



        // ===============================
        // Output
        // ===============================


        if(typeof data.output === "string"){


            output.textContent = data.output;


        }


        else if(
            typeof data.output === "object" &&
            data.output !== null
        ){


            output.textContent =
                data.output.output ||
                JSON.stringify(
                    data.output,
                    null,
                    2
                );


        }


        else{


            output.textContent = "No Output";


        }




        // ===============================
        // AI Explanation
        // ===============================


        if(Array.isArray(data.ai_explanation)){


            explanation.textContent =
                data.ai_explanation.join("\n");


        }

        else{


            explanation.textContent =
                "No AI explanation available";


        }






        // ===============================
        // AI Suggestions
        // ===============================


        if(Array.isArray(data.ai_suggestions)){


            suggestions.textContent =
                data.ai_suggestions.join("\n");


        }

        else{


            suggestions.textContent =
                "No AI suggestions available";


        }






        // ===============================
        // AI Error Fix
        // ===============================


        if(data.ai_error_fix){


            errorFix.textContent =
                JSON.stringify(
                    data.ai_error_fix,
                    null,
                    2
                );


        }

        else{


            errorFix.textContent =
                "No AI error fix available";


        }



    }


    catch(error){


        console.error(error);



        if(error.name === "AbortError"){


            output.textContent =
                "Execution timeout";


        }

        else{


            output.textContent =
                "Backend connection error: " + error.message;


        }


    }


    finally{


        isRunning = false;


    }



});



// ===============================
// Projects Page — Search + Filter
// ===============================

const projectSearch = document.getElementById("projectSearch");
const languageFilter = document.getElementById("languageFilter");
const levelFilter = document.getElementById("levelFilter");
const surpriseBtn = document.getElementById("surpriseBtn");
const projectsGrid = document.getElementById("projectsGrid");
const projectCount = document.getElementById("projectCount");


function getLevelTagClass(level) {

    if (level === "Basic") return "tag-basic";
    if (level === "Medium") return "tag-medium";
    if (level === "Advanced") return "tag-advanced";

    return "tag-basic";

}


function renderProjectCards(list) {

    if (!projectsGrid) return;

    if (list.length === 0) {

        projectsGrid.innerHTML = `<p style="color:#94a3b8;">No projects match your filters. Try changing the search or filters.</p>`;
        projectCount.textContent = "";
        return;

    }

    projectCount.textContent = `${list.length} project idea${list.length !== 1 ? "s" : ""} found`;

    projectsGrid.innerHTML = list.map((project) => `
        <div class="project-card">
            <h4>${project.title}</h4>
            <p>${project.description}</p>
            <div class="project-card-tags">
                <span class="tag tag-language">${project.language}</span>
                <span class="tag ${getLevelTagClass(project.level)}">${project.level}</span>
            </div>
        </div>
    `).join("");

}


function renderProjects() {

    if (typeof projects === "undefined") {

        if (projectsGrid) {
            projectsGrid.innerHTML = `<p style="color:#f87171;">Could not load project ideas (projects.js missing).</p>`;
        }

        return;

    }

    const searchTerm = (projectSearch?.value || "").toLowerCase().trim();
    const selectedLanguage = languageFilter?.value || "all";
    const selectedLevel = levelFilter?.value || "all";

    const filtered = projects.filter((project) => {

        const matchesSearch =
            searchTerm === "" ||
            project.title.toLowerCase().includes(searchTerm) ||
            project.description.toLowerCase().includes(searchTerm);

        const matchesLanguage =
            selectedLanguage === "all" || project.language === selectedLanguage;

        const matchesLevel =
            selectedLevel === "all" || project.level === selectedLevel;

        return matchesSearch && matchesLanguage && matchesLevel;

    });

    renderProjectCards(filtered);

}


if (projectSearch) {
    projectSearch.addEventListener("input", renderProjects);
}

if (languageFilter) {
    languageFilter.addEventListener("change", renderProjects);
}

if (levelFilter) {
    levelFilter.addEventListener("change", renderProjects);
}

if (surpriseBtn) {

    surpriseBtn.addEventListener("click", () => {

        if (typeof projects === "undefined" || projects.length === 0) return;

        const randomProject = projects[Math.floor(Math.random() * projects.length)];

        renderProjectCards([randomProject]);

        if (projectSearch) projectSearch.value = "";
        if (languageFilter) languageFilter.value = "all";
        if (levelFilter) levelFilter.value = "all";

    });

}