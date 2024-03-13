/**
Responsive HTML Table With Pure CSS - Web Design/UI Design

Code written by:
👨🏻‍⚕️ @Coding Design (Jeet Saru)

> You can do whatever you want with the code. However if you love my content, you can **SUBSCRIBED** my YouTube Channel.

🌎link: www.youtube.com/codingdesign 
*/

const search = document.querySelector('.input-group input'),
    table_rows = document.querySelectorAll('tbody tr'),
    table_headings = document.querySelectorAll('thead th');

// 1. Searching for specific data of HTML table
search.addEventListener('input', searchTable);

function searchTable() {
    console.log("search table active");
    table_rows.forEach((row, i) => {
        let table_data = row.textContent.toLowerCase(),
            search_data = search.value.toLowerCase();
            console.log("searching for...", search_data)

        row.classList.toggle('d-none', table_data.indexOf(search_data) < 0);
        row.style.setProperty('--delay', i / 25 + 's');
    })

    document.querySelectorAll('tbody tr:not(.hide)').forEach((visible_row, i) => {
        visible_row.style.backgroundColor = (i % 2 == 0) ? 'transparent' : '#0000000b';
    });
}


// 2. Sorting | Ordering data of HTML table

table_headings.forEach((head, i) => {
    let sort_asc = true;
    head.onclick = () => {
        console.log("clucked", head)
        

        if (head.getElementsByTagName('i')[0].classList.contains("bi-caret-down")) {
            console.log("sort");
            table_headings.forEach(head => head.classList.remove('active'));
            head.classList.add('active');

            head.classList.toggle('asc', sort_asc);
            sort_asc = head.classList.contains('asc') ? false : true;
    
            head.getElementsByTagName('i')[0].classList.toggle("bi-caret-up");
    
            sortTable(i, sort_asc, head);

        } else {
            console.log("do not sort")
        }


    }
})


function sortTable(column, sort_asc, head) {
    [...table_rows].sort((a, b) => {
        // let first_row = a.querySelectorAll('td')[column].textContent.toLowerCase(),
        //     second_row = b.querySelectorAll('td')[column].textContent.toLowerCase();

        if (head.textContent.includes("Date")) {
                var xxx = convertDate(a.querySelectorAll('td')[column].textContent),
                    yyy = convertDate(b.querySelectorAll('td')[column].textContent);
            } else {
                var xxx = a.querySelectorAll('td')[column].textContent,
                    yyy = b.querySelectorAll('td')[column].textContent;
            }
    

        let first_row = (isNaN(xxx)) ? (xxx.toLowerCase() === '-')? 0 : xxx.toLowerCase(): parseFloat(xxx);
        let second_row = (isNaN(yyy)) ? (yyy.toLowerCase() === '-')? 0 : yyy.toLowerCase(): parseFloat(yyy);

        return sort_asc ? (first_row < second_row ? 1 : -1) : (first_row < second_row ? -1 : 1);
    })
        .map(sorted_row => document.querySelector('tbody').appendChild(sorted_row));
}

function convertDate(d) {
    var p = d.split("/");
    return +(p[2]+p[0]+p[1]);
  }
