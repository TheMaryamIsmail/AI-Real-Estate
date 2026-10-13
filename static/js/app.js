document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        OverallQual: parseInt(document.getElementById('OverallQual').value),
        GrLivArea: parseInt(document.getElementById('GrLivArea').value),
        GarageCars: parseInt(document.getElementById('GarageCars').value),
        TotalBsmtSF: parseInt(document.getElementById('TotalBsmtSF').value),
        FullBath: parseInt(document.getElementById('FullBath').value),
        YearBuilt: parseInt(document.getElementById('YearBuilt').value),
        Neighborhood: document.getElementById('Neighborhood').value
    };
    const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await res.json();
    document.getElementById('prediction-result').innerText = `Estimated Price: $${result.estimated_price.toLocaleString()}`;
});

document.getElementById('chat-btn').addEventListener('click', async () => {
    const prompt = document.getElementById('chat-input').value;
    const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });
    const result = await res.json();
    document.getElementById('chat-response').innerText = result.response;
});