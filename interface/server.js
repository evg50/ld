
const express = require("express");
const { exec } = require("child_process");
const path = require("path");

const app = express();
const PORT = 3000;

// Пути к LDPlayer
const LD_CONSOLE = `"H:\\LDPlayer\\LDPlayer9\\ldconsole.exe"`;
const ADB = `"H:\\LDPlayer\\LDPlayer9\\adb.exe"`;

// Папка public
app.use(express.static(path.join(__dirname, "public")));

// ---------------------------------------------------------
// Получение списка устройств
// ---------------------------------------------------------
app.get("/devices", (req, res) => {
    exec(`${ADB} devices`, (err, stdout) => {
        if (err) return res.json([]);

        const devices = stdout
            .split("\n")
            .slice(1)
            .map(l => l.trim().split("\t"))
            .filter(p => p.length === 2 && p[1] === "device")
            .map(p => p[0]);

        res.json(devices);
    });
});

app.get("/start-ld", (req, res) => {
    const index = req.query.index;
    if (!index) return res.send("Ошибка: index не указан");

    // Мгновенный ответ UI
    res.send(`Запускаю LDPlayer и игру для индекса ${index}...`);

    // Запуск Python
    exec(
        `"C:\\Users\\Пользователь\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m Ldplayer_bot.services.ldplayer_manager ${parseInt(index)}`,
        { cwd: "C:\\Ldplayer_bot" },
        (err, stdout, stderr) => {
            if (err) {
                console.log("Ошибка Python:", stderr);
            } else {
                console.log(stdout);
            }
        }
    );
});
app.get("/run-hunt", (req, res) => {
    const device = req.query.device;
    const index = parseInt(req.query.index);

    if (!device || isNaN(index)) {
        return res.send("Ошибка: device или index не указан");
    }

    // Логика выбора количества атак
    let attacks = 11;
    let pause = 60;

    if (index === 54 || index === 56) {
        attacks = 14;
    }

    res.send(`Охота запускается на ${device} (атаки=${attacks}, пауза=${pause})...`);

    const { exec } = require("child_process");

    const cmd = `"C:\\Users\\Пользователь\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m Ldplayer_bot.services.hunt_sm ${device} ${attacks} ${pause}`;

    exec(cmd, { cwd: "C:\\Ldplayer_bot" }, (err, stdout, stderr) => {
        if (err) {
            console.log("Ошибка охоты:", stderr);
        } else {
            console.log("Охота результат:", stdout);
        }
    });
});


app.get("/stop-ld", (req, res) => {
    const index = req.query.index;
    if (!index) return res.send("Ошибка: index не указан");

    res.send(`Закрываю LDPlayer index=${index}...`);

    const cmd = `"H:\\LDPlayer\\LDPlayer9\\ldconsole.exe" quit --index ${index}`;

    const { exec } = require("child_process");
    exec(cmd, (err, stdout, stderr) => {
        if (err) {
            console.log("Ошибка закрытия LDPlayer:", stderr);
        } else {
            console.log("LDPlayer закрыт:", stdout);
        }
    });
});
app.get("/run-vip", (req, res) => {
    const device = req.query.device;
    if (!device) return res.send("Ошибка: device не указан");

    res.send(`Запускаю VIP алгоритм для ${device}...`);

    const { exec } = require("child_process");

    const cmd = `"C:\\Users\\Пользователь\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m Ldplayer_bot.services.take_vip ${device}`;

    exec(cmd, { cwd: "C:\\Ldplayer_bot" }, (err, stdout, stderr) => {
        if (err) {
            console.log("Ошибка VIP:", stderr);
        } else {
            console.log("VIP результат:", stdout);
        }
    });
});

// ---------------------------------------------------------
// Статус загрузки эмулятора
// ---------------------------------------------------------
app.get("/status", (req, res) => {
    const device = req.query.device;
    if (!device) return res.json({ status: "device undefined" });

    exec(`${ADB} -s ${device} shell getprop sys.boot_completed`, (err, stdout) => {
        if (err) return res.json({ status: "ADB error" });

        res.json({
            status: stdout.trim() === "1" ? "Устройство загружено" : "Загрузка..."
        });
    });
});

// ---------------------------------------------------------
// Скриншот
// ---------------------------------------------------------
app.get("/screenshot", (req, res) => {
    const device = req.query.device;

    exec(
        `python -m Ldplayer_bot.services.screenshot ${device}`,
        { cwd: path.join(__dirname, "..") },
        (err, stdout) => {
            if (err) return res.json({ error: err.toString() });

            res.sendFile(stdout.trim());
        }
    );
});

// ---------------------------------------------------------
// Охота
// ---------------------------------------------------------
app.get("/hunt", (req, res) => {
    const device = req.query.device;
    const count = req.query.count || 5;
    const pausa = req.query.pausa || 120;

    if (!device) return res.send("Ошибка: device не указан");

    exec(
        `python -m Ldplayer_bot.services.hunt_smart ${device} ${count} ${pausa}`,
        { cwd: path.join(__dirname, "..") },
        (err, stdout) => {
            if (err) return res.send("Ошибка: " + err);
            res.send(stdout);
        }
    );
});

// ---------------------------------------------------------
app.listen(PORT, () => {
    console.log(`UI запущен: http://localhost:${PORT}`);
});
