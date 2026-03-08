document.addEventListener('DOMContentLoaded', () => {
    const generateForm = document.getElementById('generate-form');
    const categorySelect = document.getElementById('category-select');
    const spinner = document.getElementById('spinner');
    const namesContainer = document.getElementById('names-container');
    const raceFilter = document.getElementById('race-filter');
    const recentContainer = document.getElementById('recent-names-container');

    function rateName(name) {
        if (!name || typeof name !== 'string') return 0;

        const clean = name.toLowerCase().replace(/[^a-zа-яё]/gi, '');
        const uniqueLetters = new Set(clean);
        const vowels = clean.match(/[aeiouаеёиоуыэюя]/gi) || [];
        const consonants = clean.length - vowels.length;

        let score = clean.length * 2 + uniqueLetters.size * 3;

        const balance = Math.abs(vowels.length - consonants);
        if (balance <= 2) score += 10;

        const rareLetters = [...clean].filter(ch => 'xzjqwфщц'.includes(ch));
        score += rareLetters.length * 5;

        if (clean.length > 8) score += 10;

        const luck = Math.random();
        if (luck > 0.97) score = 100;

        return Math.min(100, score);
    }

    function getCSRFToken() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    generateForm.addEventListener('submit', (e) => {
        e.preventDefault();
        spinner.style.display = 'block';
        namesContainer.innerHTML = '';

        const formData = new FormData(generateForm);
        fetch('/ajax/generate-name/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            console.log('Ответ от сервера:', data);
            spinner.style.display = 'none';

            if (data.error) {
                alert(data.error);
                return;
            }

            const div = document.createElement('div');
            div.className = 'name-box fade-in';
            div.innerHTML = `
                <div class="name-entry">
                    <span class="name-text">${data.name}</span>
                    <span class="race-tag">(${data.category})</span>
                    <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
                <form method="post" action="/add-favorite/" class="favorite-form">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${data.csrf_token}">
                    <input type="hidden" name="name" value="${data.name}">
                    <input type="hidden" name="race" value="${data.category}">
                    <button type="submit">⭐ Add to favorites</button>
                </form>
            `;

            if (data.is_legendary) {
                console.log('🌌 Легендарное имя выпало!');
                div.classList.add('legendary-glow');
            }

            namesContainer.appendChild(div);

            let score = rateName(data.name);
            if (data.is_legendary) score = 100;

            document.getElementById('power-score').textContent = `${score} / 100`;

            const statusEl = document.getElementById('power-status');
            statusEl.className = 'power-status';

            if (data.is_legendary || score >= 90) {
                statusEl.textContent = '🌌 Legendary';
                statusEl.classList.add('status-legendary');
            } else if (score < 40) {
                statusEl.textContent = '💀 Common';
                statusEl.classList.add('status-weak');
            } else if (score < 70) {
                statusEl.textContent = '🧝 Rare';
                statusEl.classList.add('status-rare');
            } else {
                statusEl.textContent = '🐉 Epic';
                statusEl.classList.add('status-epic');
            }

            loadRecentNames(raceFilter.value);
        })
        .catch(err => {
            spinner.style.display = 'none';
            console.error('🔥 JS ошибка при обработке имени:', err);
            alert('Ошибка генерации имени: ' + err.message);
        });
    });

    function loadRecentNames(race) {
        fetch(`/ajax/recent-names/?race=${encodeURIComponent(race)}`)
            .then(res => res.json())
            .then(data => {
                recentContainer.innerHTML = '';

                if (data.names.length === 0) {
                    recentContainer.innerHTML = '<p>Ничего не найдено.</p>';
                    return;
                }

                data.names.forEach(n => {
                    const div = document.createElement('div');
                    div.className = 'name-box fade-in';
                    div.innerHTML = `
                        <div class="name-entry">
                            <span class="name-text">${n.name}</span>
                            <span class="race-tag">(${n.race})</span>
                            <span class="timestamp">${n.created}</span>
                        </div>
                    `;
                    recentContainer.appendChild(div);
                });
            })
            .catch(err => {
                console.error('Ошибка загрузки истории:', err);
                recentContainer.innerHTML = '<p>Ошибка загрузки истории.</p>';
            });
    }

    raceFilter.addEventListener('change', () => {
        loadRecentNames(raceFilter.value);
    });

    loadRecentNames(raceFilter.value);
});
