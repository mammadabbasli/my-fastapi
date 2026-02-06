document.getElementById('predictBtn').addEventListener('click', async function () {
    const exp = document.getElementById('experience').value;

    if (!exp) {
        alert('Please enter years of experience');
        return;
    }

    const response = await fetch('http://16.170.204.193:8000/predict?experience=' + exp);
    const data = await response.json();

    const result = document.getElementById('result');
    result.style.display = 'block';
    result.textContent = 'Predicted Salary: $' + data.predicted_salary.toLocaleString();

    loadHistory();
});

async function loadHistory() {
    const response = await fetch('http://16.170.204.193:8000/history');
    const data = await response.json();

    document.getElementById('historyTitle').style.display = 'block';
    document.getElementById('historyTable').style.display = 'table';

    const tbody = document.getElementById('historyBody');
    tbody.innerHTML = '';

    data.forEach(function (item) {
        const row = document.createElement('tr');
        row.innerHTML =
            '<td>' + item.experience + ' years</td>' +
            '<td>$' + item.salary.toLocaleString() + '</td>' +
            '<td>' + item.date.slice(0, 16) + '</td>';
        tbody.appendChild(row);
    });
}
