function loadSummary(){

fetch("/summary")

.then(res=>res.json())

.then(data=>{

document.getElementById("totalExpense").innerText = data.expense
document.getElementById("totalIncome").innerText = data.income

const ctx = document.getElementById("myChart")

new Chart(ctx,{
type:"pie",

data:{
labels:["Expense","Income"],
datasets:[{
data:[data.expense,data.income],
backgroundColor:["#ff4d4d","#4CAF50"]
}]
}
})

})

}

loadSummary()


function addExpense(){

const data = {

title:document.getElementById("title").value,
amount:document.getElementById("amount").value,
category:document.getElementById("category").value,
type:document.getElementById("type").value

}

fetch("/add",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(data)

})

.then(()=>location.reload())

}


function deleteExpense(id){

fetch("/delete/"+id)

.then(()=>location.reload())

}