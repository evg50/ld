const TOTAL_INDEXES = 8;


// Генерация таблицы один раз
async function buildTable() {
    const body = document.getElementById("devices-body");

    for (let index = 0; index < TOTAL_INDEXES; index++) {
        const device = "emulator-" + (5554 + index * 2);

        body.innerHTML += `
            <tr data-device="${device}">
                <td class="index">${index}</td>
                <td class="device-id">${device}</td>

                <td>
                    <select class="action-select">
                        <option value="hunt">Охота</option>
                        <option value="vip">VIP</option>
                        <option value="fury">Fury Lord</option>
                        <option value="train">Train Troops</option>
                    </select>
                </td>

                <td>
                    <button class="action-start-btn">Старт</button>
                </td>

                <td>
                    <button class="start-btn">Запустить LD</button>
                    <button class="stop-btn">Стоп LD</button>
                    <button class="shot-btn">Скрин</button>
                </td>

                <td id="status-${device}" class="status">Неизвестно</td>

                <td>
                    <img id="img-${device}" class="screenshot" src="">
                </td>
            </tr>
        `;
    }

    bindButtons();
    updateStatuses();
}


// ws.onmessage = (event) => {
//   const cp = JSON.parse(event.data);

//   addCheckpointToUI(cp);
// };
// Привязка кнопок
function bindButtons() {
    const rows = document.querySelectorAll("table.devices-table tbody tr");

    rows.forEach(row => {
        const device = row.dataset.device;
        const index = row.querySelector(".index").innerText.trim();

        const select = row.querySelector(".action-select");
        const startBtn = row.querySelector(".action-start-btn");

        startBtn.onclick = () => {
            const action = select.value;

            if (action === "hunt") runHunt(device, index);
            if (action === "vip") runVIP(device);
            if (action === "fury") runFuryLord(device);
            if (action === "train") runTrainTroops(device);
        };

        row.querySelector(".start-btn").onclick = () => startLD(index);
        row.querySelector(".stop-btn").onclick = () => stopLD(index, device);
        row.querySelector(".shot-btn").onclick = () => loadScreenshot(device);
    });
}

// LD
function startLD(index) {
    fetch("/start-ld?index=" + index);
}

function stopLD(index, device) {
    fetch("/stop-ld?index=" + index);
}

// Скрин
function loadScreenshot(device) {
    const img = document.getElementById("img-" + device);
    img.src = "/screenshot?device=" + device + "&ts=" + Date.now();
}

// Охота
function runHunt(device, index) {
    fetch(`/run-hunt?device=${device}&index=${index}`);
}

function runVIP(device) {
    fetch(`/run-vip?device=${device}`);
}

function runFuryLord(device) {
    fetch(`/run-fury-lord?device=${device}`);
}

// NEW: Train Troops
function runTrainTroops(device) {
    fetch(`/train-troops?device=${device}`);
}

function addCheckpointToUI(cp) {
  const box = document.getElementById('checkpoints');

  const div = document.createElement('div');
  div.className = 'checkpoint';
  div.innerHTML = `
        <b>${cp.time}</b> — ${cp.label}
        ${cp.data ? `<pre>${cp.data}</pre>` : ''}
    `;

  box.appendChild(div);
}

// Обновление статусов
async function updateStatuses() {
    const devices = await fetch("/devices").then(r => r.json());

    document.querySelectorAll("tr[data-device]").forEach(row => {
        const device = row.dataset.device;
        const isRunning = devices.includes(device);

        const statusCell = document.getElementById("status-" + device);
        const stopBtn = row.querySelector(".stop-btn");
        const shotBtn = row.querySelector(".shot-btn");
        const select = row.querySelector(".action-select");
        const actionStart = row.querySelector(".action-start-btn");

        if (isRunning) {
            row.classList.add("running");
            row.classList.remove("offline");

            statusCell.innerText = "Запущен";

            stopBtn.disabled = false;
            shotBtn.disabled = false;
            select.disabled = false;
            actionStart.disabled = false;

        } else {
            row.classList.add("offline");
            row.classList.remove("running");

            statusCell.innerText = "Оффлайн";

            stopBtn.disabled = true;
            shotBtn.disabled = true;
            select.disabled = true;
            actionStart.disabled = true;
        }
    });
}

buildTable();
setInterval(updateStatuses, 3000);
