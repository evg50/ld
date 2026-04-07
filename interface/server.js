const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));

// Получение списка устройств
app.get("/devices", (req, res) => {
    exec("adb devices", (err, stdout) => {
        if (err) return res.json([]);

        const lines = stdout.split("\n").slice(1);
        const devices = lines
            .map(l => l.trim().split("\t"))
            .filter(parts => parts.length === 2 && parts[1] === "device")
            .map(parts => parts[0]);

        res.json(devices);
    });
});

// Запуск игры
app.get("/start-game", (req, res) => {
    const device = req.query.device;
    if (!device) return res.send("Ошибка: не указан device");

    exec(
        `python -m Ldplayer_bot.services.start_game ${device}`,
        { cwd: path.join(__dirname, "..") },
        (err, stdout) => {
            if (err) return res.send("Ошибка: " + err);
            res.send(stdout);
        }
    );
});

// Скриншот
app.get("/screenshot", (req, res) => {
    const device = req.query.device;

    exec(
        `python -m Ldplayer_bot.services.screenshot ${device}`,
        { cwd: path.join(__dirname, "..") },
        (err, stdout) => {
            if (err) return res.json({ error: err.toString() });

            const filePath = stdout.trim();
            res.sendFile(filePath);
        }
    );
});

// Охота
app.get('/hunt', (req, res) => {
    const device = req.query.device;
    const count = req.query.count || 5;
    const pausa = req.query.pausa || 120;

    if (!device) return res.send("Ошибка: не указан device");

    const cmd = `python -m Ldplayer_bot.services.hunt_smart ${device} ${count} ${pausa}`;

    exec(cmd, { cwd: path.join(__dirname, "..") }, (err, stdout) => {
        if (err) return res.send("Ошибка: " + err);
        res.send(stdout);
    });
});

app.listen(PORT, () => {
  console.log(`UI запущен: http://localhost:${PORT}`);
});
