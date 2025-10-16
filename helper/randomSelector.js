condition_count = 11
condition_row_length = 50
select_count = 5

const XLSX = require('xlsx');
const fs = require('fs');
const Docxtemplater = require('docxtemplater');
const path = require('path');

const scriptDirectory = __dirname; // Get the directory of the current script
const sheetFile       = path.join(scriptDirectory,'stimulus_list.xlsx')
// Load the Excel file
const workbook = XLSX.readFile(sheetFile); // Replace 'cb_id_sheet.xlsx' with the path to your Excel file

// Assume the data is in the first sheet of the workbook
const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];

function randomIntFromInterval2(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
  }
  randomIntFromInterval = randomIntFromInterval2;



function selectStimuli2(condition_count, condition_row_length, select_count){
    var all_indices=[]
    for (var i=1; i <= condition_count; i++){

        var condition_indices=[]
        var lower_bound = (0+(condition_row_length*(i-1)))
        var higher_bound = (condition_row_length*i) - 1

        while(condition_indices.length < select_count){
            var element

            element = randomIntFromInterval(lower_bound, higher_bound)
            // console.log(element)
            if (condition_indices.includes(element)){
                continue
            } else {
                condition_indices.push(element)
            }      
        }
        console.log(condition_indices)
        all_indices=all_indices.concat(condition_indices)

    }
    return all_indices
}
``
selectStimuli = selectStimuli2
condition_count = 11
condition_row_length = 50
select_count = 5
selectedRows = selectStimuli(condition_count, condition_row_length, select_count)
// console.log(selectStimuli(condition_count, condition_row_length, select_count))
posVals=[]
for (let i =2; i<600;i++){
    const position     = worksheet[`C${i}`];
    if (!position || !position.v) {
        // Break when there are no more values in the first column
        continue;
      }

    posVals.push(position.v);
}



console.log('position vals', posVals)
console.log('selected rows:', selectedRows)
console.log('selected vals:', posVals[selectedRows])
