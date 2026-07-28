const students = [

{
roll:"101",
name:"Rahul Sharma",
branch:"Computer Science",
year:"2nd Year",
cgpa:"8.9",
image:"Student-Images/images/Flower.jpg",
email:"rahul@college.edu",

maths:95,
physics:88,
chemistry:91,
english:84,
computer:98
},

{
roll:"102",
name:"Priya Verma",
branch:"Information Technology",
year:"3rd Year",
cgpa:"9.2"
},

{
roll:"103",
name:"Aman Gupta",
branch:"Mechanical",
year:"1st Year",
cgpa:"8.1"
},

{
roll:"104",
name:"Sneha Singh",
branch:"Civil",
year:"4th Year",
cgpa:"8.8"
},

{
roll:"105",
name:"Rohit Kumar",
branch:"Electronics",
year:"2nd Year",
cgpa:"9.0"
}

];

const rollInput=document.getElementById("rollNumber");

const searchBtn=document.getElementById("searchBtn");

const result=document.getElementById("result");

searchBtn.addEventListener("click",function(){

const roll=rollInput.value.trim();

const student = students.find(function(item){

    return item.roll===roll;

});

const totalMarks =
student.maths +
student.physics +
student.chemistry +
student.english +
student.computer;

if(student){

result.innerHTML = `

<div class="card">

<img src="${student.image}" class="student-photo">

<h2>${student.name}</h2>

<hr><br>

<p><strong>Roll Number :</strong> ${student.roll}</p>

<p><strong>Branch :</strong> ${student.branch}</p>

<p><strong>Year :</strong> ${student.year}</p>

<p><strong>CGPA :</strong> ${student.cgpa}</p>

<p><strong>Email :</strong> ${student.email}</p>

<p><strong>Mathematics :</strong> ${student.maths}</p>

<p><strong>Total Marks :</strong> ${totalMarks} / 500</p>

</div>

`;

}
else{

result.innerHTML=`

<p class="error">

❌ Roll Number Not Found

</p>

`;

}

});

rollInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        searchBtn.click();

    }

});