function toggleDatetype(datetype) {
    document.getElementById('toggleYear').classList.add('visually-hidden')
    document.getElementById('toggleMonth').classList.add('visually-hidden')
    document.getElementById('toggleDay').classList.add('visually-hidden')
    if (datetype === 'year') {
        document.getElementById('toggleYear').classList.remove('visually-hidden')
    } else if (datetype === 'month') {
        document.getElementById('toggleMonth').classList.remove('visually-hidden')
    } else if (datetype === 'day') {
        document.getElementById('toggleDay').classList.remove('visually-hidden')
    }
}

let startDate = document.getElementById('startDate')
let endDate = document.getElementById('endDate')

startDate.addEventListener('change',(e)=>{
    document.getElementById('startDateSelected').innerText = e.target.value
})

endDate.addEventListener('change',(e)=>{
    document.getElementById('endDateSelected').innerText = e.target.value
})