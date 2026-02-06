document.getElementById('predictBtn').addEventListener('click', async function () {
    const exp = document.getElementById('experience').value;

    if (!exp) {
        alert('Please enter years of experience');
        return;
    }

    const response = await fetch('/predict?experience=' + exp);
    const data = await response.json();

    const result = document.getElementById('result');
    result.style.display = 'block';
    result.textContent = 'Predicted Salary: $' + data.predicted_salary.toLocaleString();
});
