// ===============================
// Monaco Editor Setup
// ===============================

require.config({
    paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.0/min/vs"
    }
});


let editor;
let isRunning = false;



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


});



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