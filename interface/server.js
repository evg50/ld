// const express = require('express');
// const { exec } = require('child_process');
// const path = require('path');

// const app = express();
// const PORT = 3000;
// const adb = `"H:\\LDPlayer\\LDPlayer9\\adb.exe"`;
// app.use(express.static(path.join(__dirname, 'public')));

// // Получение списка устройств
// app.get("/devices", (req, res) => {
//     exec(`${adb} devices`, (err, stdout) => {
//         if (err) return res.json([]);

//         const lines = stdout.split("\n").slice(1);
//         const devices = lines
//             .map(l => l.trim().split("\t"))
//             .filter(parts => parts.length === 2 && parts[1] === "device")
//             .map(parts => parts[0]);

//         res.json(devices);
//     });
// });

// app.get("/start-ld", (req, res) => {
//     const index = req.query.index;
//     if (index === undefined) return res.send("Ошибка: не указан index");

//     const ldconsole = `"H:\\LDPlayer\\LDPlayer9\\ldconsole.exe"`;

//     exec(`${ldconsole} launch --index ${index}`, (err) => {
//         if (err) return res.send("Ошибка запуска LDPlayer");
//         res.send("LDPlayer с индексом " + index + " запущен");
//     });
// });



// // Запуск игры
// app.get("/start-game", (req, res) => {
//     const device = req.query.device;
//     if (!device) return res.send("Ошибка: не указан device");

//     exec(
//         `python -m Ldplayer_bot.services.start_game ${device}`,
//         { cwd: path.join(__dirname, "..") },
//         (err, stdout) => {
//             if (err) return res.send("Ошибка: " + err);
//             res.send(stdout);
//         }
//     );
// });

// let botProcess = null;

// app.get("/bot/start", (req, res) => {
//     const device = req.query.device;

//     if (!device) {
//         return res.json({ status: "device undefined" });
//     }

//     if (botProcess) {
//         return res.json({ status: "already running" });
//     }

//     botProcess = exec(
//         `python -m Ldplayer_bot.main ${device}`,
//         { cwd: path.join(__dirname, "..") }
//     );

//     botProcess.stdout.on("data", data => {
//         console.log("[BOT]", data.toString());
//     });

//     botProcess.stderr.on("data", data => {
//         console.log("[BOT ERROR]", data.toString());
//     });

//     botProcess.on("exit", () => {
//         botProcess = null;
//     });

//     res.json({ status: "started" });
// });

// app.get("/bot/stop", (req, res) => {
//     if (!botProcess) {
//         return res.json({ status: "not running" });
//     }

//     botProcess.kill("SIGTERM");
//     botProcess = null;

//     res.json({ status: "stopped" });
// });

// app.get("/bot/stop", (req, res) => {
//     if (!botProcess) {
//         return res.json({ status: "not running" });
//     }

//     botProcess.kill("SIGTERM");
//     botProcess = null;

//     res.json({ status: "stopped" });
// });

// app.get("/status", (req, res) => {
//     const device = req.query.device;

//     if (!device) {
//         return res.json({ status: "device undefined" });
//     }

//     exec(`adb -s ${device} shell getprop sys.boot_completed`, (err, stdout) => {
//         if (err) {
//             return res.json({ status: "ADB error" });
//         }

//         const value = stdout.trim();

//         if (value === "1") {
//             res.json({ status: "Устройство загружено" });
//         } else {
//             res.json({ status: "Загрузка..." });
//         }
//     });
// });


// // Скриншот
// app.get("/screenshot", (req, res) => {
//     const device = req.query.device;

//     exec(
//         `python -m Ldplayer_bot.services.screenshot ${device}`,
//         { cwd: path.join(__dirname, "..") },
//         (err, stdout) => {
//             if (err) return res.json({ error: err.toString() });

//             const filePath = stdout.trim();

//             res.sendFile(filePath);
//         }
//     );
// });


// // Охота
// app.get('/hunt', (req, res) => {
//     const device = req.query.device;
//     const count = req.query.count || 5;
//     const pausa = req.query.pausa || 120;

//     if (!device) return res.send("Ошибка: не указан device");

//     const cmd = `python -m Ldplayer_bot.services.hunt_smart ${device} ${count} ${pausa}`;

//     exec(cmd, { cwd: path.join(__dirname, "..") }, (err, stdout) => {
//         if (err) return res.send("Ошибка: " + err);
//         res.send(stdout);
//     });
// });

// app.listen(PORT, () => {
//   console.log(`UI запущен: http://localhost:${PORT}`);
// });
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
        `"C:\\Users\\Пользователь\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m Ldplayer_bot.services.ldplayer_manager ${index}`,
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

// ---------------------------------------------------------
// ⭐ АВТОЗАПУСК LDPLAYER + АВТОЗАПУСК ИГРЫ
// ---------------------------------------------------------


// ---------------------------------------------------------
// Ручной запуск игры (если нужно)
// ---------------------------------------------------------
// app.get("/start-game", (req, res) => {
//     const device = req.query.device;
//     if (!device) return res.send("Ошибка: device не указан");

//     exec(
//         `python -m Ldplayer_bot.services.start_game ${device}`,
//         { cwd: path.join(__dirname, "..") },
//         (err, stdout) => {
//             if (err) return res.send("Ошибка: " + err);
//             res.send(stdout);
//         }
//     );
// });

// // ---------------------------------------------------------
// // БОТ
// // ---------------------------------------------------------
// let botProcess = null;

// app.get("/bot/start", (req, res) => {
//     const device = req.query.device;
//     if (!device) return res.json({ status: "device undefined" });

//     if (botProcess) return res.json({ status: "already running" });

//     botProcess = exec(
//         `python -m Ldplayer_bot.main ${device}`,
//         { cwd: path.join(__dirname, "..") }
//     );

//     botProcess.stdout.on("data", d => console.log("[BOT]", d.toString()));
//     botProcess.stderr.on("data", d => console.log("[BOT ERROR]", d.toString()));
//     botProcess.on("exit", () => botProcess = null);

//     res.json({ status: "started" });
// });

// app.get("/bot/stop", (req, res) => {
//     if (!botProcess) return res.json({ status: "not running" });

//     botProcess.kill("SIGTERM");
//     botProcess = null;

//     res.json({ status: "stopped" });
// });

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
