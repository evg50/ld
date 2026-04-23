// Запуск LDPlayer + игры
function startLD(index) {
    fetch("/start-ld?index=" + index)
        .then(r => r.text())
        .then(text => {
            console.log(text);
        })
        .catch(() => {
            console.log("Ошибка запуска LDPlayer");
        });
}

// Остановка бота (если он запущен)
function stopLD(index, device) {
    fetch("/stop-ld?index=" + index)
        .then(r => r.text())
        .then(data => {
            document.getElementById("status-" + device).innerText = "LD закрыт";
        })
        .catch(() => {
            document.getElementById("status-" + device).innerText = "Ошибка";
        });
}

// Загрузка скриншота
function loadScreenshot(device) {
    const img = document.getElementById("img-" + device);
    img.src = "/screenshot?device=" + device + "&ts=" + Date.now();
}

// Автообновление статуса всех устройств
function updateStatuses() {
    const rows = document.querySelectorAll("table.devices-table tbody tr");

    rows.forEach(row => {
        const device = row.dataset.device;

        fetch("/status?device=" + device)
            .then(r => r.json())
            .then(data => {
                document.getElementById("status-" + device).innerText = data.status;
            })
            .catch(() => {
                document.getElementById("status-" + device).innerText = "Оффлайн";
            });
    });
}

// Привязка кнопок
function bindButtons() {
    const rows = document.querySelectorAll("table.devices-table tbody tr");

    rows.forEach(row => {
        const device = row.dataset.device;
        const index = row.querySelector("td:first-child").innerText.trim();

        const select = row.querySelector("select");
        select.onchange = () => onFunctionChange(device, select.value, index);

        row.querySelector(".start-btn").onclick = () => startLD(index);
        row.querySelector(".stop-btn").onclick = () => stopLD(index, device);
        row.querySelector(".shot-btn").onclick = () => loadScreenshot(device);
    });
}
function runHunt(device, index) {
    fetch(`/run-hunt?device=${device}&index=${index}`)
        .then(r => r.text())
        .then(text => {
            console.log(text);
            document.getElementById("status-" + device).innerText = "Охота выполняется";
        })
        .catch(() => {
            document.getElementById("status-" + device).innerText = "Ошибка охоты";
        });
}



function onFunctionChange(device, value, index) {
    if (value === "VIP") {
        runVIP(device);
    }

    if (value === "Охота") {
        runHunt(device, index);
    }
}

function runVIP(device) {
    fetch("/run-vip?device=" + device)
        .then(r => r.text())
        .then(text => {
            console.log(text);
            document.getElementById("status-" + device).innerText = "VIP выполняется";
        })
        .catch(() => {
            document.getElementById("status-" + device).innerText = "Ошибка VIP";
        });
}
// Инициализация
bindButtons();
updateStatuses();
setInterval(updateStatuses, 3000);