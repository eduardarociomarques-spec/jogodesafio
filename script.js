const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const LARGURA = canvas.width;
const ALTURA = canvas.height;

// Cores Retrô
const CORES = {
    PRETO: "#0f0f1e",
    BRANCO: "#ffffff",
    AMARELO: "#ffdc32",
    AZUL_NAVE: "#32b4ff",
    VERMELHO: "#ff3c50",
    VERDE_ALIEN: "#3ce664",
    ROXO_BOSS: "#b432e6"
};

// --- GERADOR DE SONS RETRÔ (8-BIT) ---
const AudioContextClass = window.AudioContext || window.webkitAudioContext;
const audioCtx = AudioContextClass ? new AudioContextClass() : null;

function tocarSom(freq, duracao, tipo = "square") {
    if (!audioCtx) return;
    try {
        if (audioCtx.state === "suspended") audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = tipo;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duracao);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duracao);
    } catch (e) {
        // Ignora erro caso o áudio seja bloqueado pelo navegador
    }
}

// --- MATRIZES DE PIXEL ART ---
const MATRIZ_NAVE = [
    "     1     ",
    "    111    ",
    "    121    ",
    "  1 111 1  ",
    "  1111111  ",
    " 113111311 ",
    "11111111111",
    "1 11   11 1"
];

const MATRIZ_ALIEN = [
    "  1     1  ",
    "   1   1   ",
    "  1111111  ",
    " 112111211 ",
    "11111111111",
    "1 1111111 1",
    "1 1     1 1",
    "   11 11   "
];

const MATRIZ_BOSS = [
    "    11111111    ",
    "  111111111111  ",
    " 11221111112211 ",
    "1112211111122111",
    "1111111331111111",
    " 11111111111111 ",
    "  11 11  11 11  ",
    " 11  11  11  11 "
];

function desenharSprite(matriz, mapaCores, x, y, escala) {
    for (let linha = 0; linha < matriz.length; linha++) {
        for (let col = 0; col < matriz[linha].length; col++) {
            const pixel = matriz[linha][col];
            if (mapaCores[pixel]) {
                ctx.fillStyle = mapaCores[pixel];
                ctx.fillRect(x + col * escala, y + linha * escala, escala, escala);
            }
        }
    }
}

// --- ESTADO DO JOGO ---
let jogador, inimigos, tirosJogador, tirosInimigos, boss, pontos, fase, estado;
const teclas = {};
const estrelas = Array.from({ length: 50 }, () => ({
    x: Math.random() * LARGURA,
    y: Math.random() * ALTURA
}));

function iniciarJogo() {
    jogador = {
        x: LARGURA / 2 - 22,
        y: ALTURA - 60,
        largura: 44,
        altura: 32,
        velocidade: 5,
        vidas: 3,
        cooldown: 0,
        invencivel: 0
    };
    inimigos = [];
    tirosJogador = [];
    tirosInimigos = [];
    boss = null;
    pontos = 0;
    fase = 1;
    estado = "JOGANDO";
    criarOnda(fase);
}

function criarOnda(numFase) {
    inimigos = [];
    boss = null;
    if (numFase < 3) {
        const linhas = 2 + numFase;
        const colunas = 7;
        const vel = 1.5 + numFase * 0.5;
        for (let l = 0; l < linhas; l++) {
            for (let c = 0; c < colunas; c++) {
                inimigos.push({
                    x: 80 + c * 65,
                    y: 40 + l * 45,
                    largura: 33,
                    altura: 24,
                    velocidade: vel
                });
            }
        }
    } else {
        boss = {
            x: LARGURA / 2 - 40,
            y: 35,
            largura: 80,
            altura: 40,
            velocidade: 3,
            hp: 30,
            maxHp: 30
        };
    }
}

function colidiu(a, b) {
    return (
        a.x < b.x + b.largura &&
        a.x + a.largura > b.x &&
        a.y < b.y + b.altura &&
        a.y + a.altura > b.y
    );
}

// Controles
window.addEventListener("keydown", (e) => {
    teclas[e.code] = true;
    if (estado === "JOGANDO" && e.code === "Space") {
        e.preventDefault();
        if (jogador.cooldown === 0) {
            tocarSom(600, 0.1, "square");
            tirosJogador.push({ x: jogador.x + jogador.largura / 2 - 2, y: jogador.y, largura: 4, altura: 12, vel: -8 });
            jogador.cooldown = 18;
        }
    } else if ((estado === "GAME_OVER" || estado === "VITORIA") && e.code === "KeyR") {
        iniciarJogo();
    }
});

window.addEventListener("keyup", (e) => {
    teclas[e.code] = false;
});

function atualizar() {
    if (estado !== "JOGANDO") return;

    // Movimento do jogador
    if ((teclas["ArrowLeft"] || teclas["KeyA"]) && jogador.x > 0) {
        jogador.x -= jogador.velocidade;
    }
    if ((teclas["ArrowRight"] || teclas["KeyD"]) && jogador.x + jogador.largura < LARGURA) {
        jogador.x += jogador.velocidade;
    }

    if (jogador.cooldown > 0) jogador.cooldown--;
    if (jogador.invencivel > 0) jogador.invencivel--;

    // Tiros
    tirosJogador.forEach((t) => (t.y += t.vel));
    tirosJogador = tirosJogador.filter((t) => t.y + t.altura > 0);

    tirosInimigos.forEach((t) => (t.y += t.vel));
    tirosInimigos = tirosInimigos.filter((t) => t.y < ALTURA);

    // Movimento dos inimigos
    let inverter = false;
    inimigos.forEach((inimigo) => {
        inimigo.x += inimigo.velocidade;
        if (inimigo.x + inimigo.largura >= LARGURA - 10 || inimigo.x <= 10) {
            inverter = true;
        }
        // Verifica se os inimigos invadiram a base
        if (inimigo.y + inimigo.altura >= ALTURA - 35) {
            estado = "GAME_OVER";
        }
        if (Math.random() < 0.002 * fase) {
            tirosInimigos.push({ x: inimigo.x + inimigo.largura / 2, y: inimigo.y + inimigo.altura, largura: 4, altura: 12, vel: 5 });
        }
    });

    if (inverter) {
        inimigos.forEach((inimigo) => {
            inimigo.velocidade *= -1;
            inimigo.y += 15;
        });
    }

    // Movimento e ataque do Chefão
    if (boss) {
        boss.x += boss.velocidade;
        if (boss.x + boss.largura >= LARGURA - 20 || boss.x <= 20) {
            boss.velocidade *= -1;
        }
        if (Math.random() < 0.04) {
            tirosInimigos.push({ x: boss.x + 15, y: boss.y + boss.altura, largura: 4, altura: 12, vel: 6 });
            tirosInimigos.push({ x: boss.x + boss.largura - 15, y: boss.y + boss.altura, largura: 4, altura: 12, vel: 6 });
        }
    }

    // Colisão tiros do jogador nos inimigos
    for (let i = tirosJogador.length - 1; i >= 0; i--) {
        let acertou = false;
        for (let j = inimigos.length - 1; j >= 0; j--) {
            if (colidiu(tirosJogador[i], inimigos[j])) {
                tocarSom(120, 0.2, "sawtooth");
                inimigos.splice(j, 1);
                pontos += 100;
                acertou = true;
                break;
            }
        }
        if (!acertou && boss && colidiu(tirosJogador[i], boss)) {
            tocarSom(120, 0.2, "sawtooth");
            boss.hp--;
            pontos += 50;
            acertou = true;
            if (boss.hp <= 0) {
                boss = null;
                pontos += 1000;
                estado = "VITORIA";
            }
        }
        if (acertou) tirosJogador.splice(i, 1);
    }

    // Dano no jogador
    if (jogador.invencivel === 0) {
        let levouDano = false;
        for (let i = tirosInimigos.length - 1; i >= 0; i--) {
            if (colidiu(jogador, tirosInimigos[i])) {
                tirosInimigos.splice(i, 1);
                levouDano = true;
                break;
            }
        }
        for (let j = inimigos.length - 1; j >= 0; j--) {
            if (colidiu(jogador, inimigos[j])) {
                inimigos.splice(j, 1);
                levouDano = true;
                break;
            }
        }
        if (levouDano) {
            tocarSom(150, 0.3, "square");
            jogador.vidas--;
            jogador.invencivel = 60;
            if (jogador.vidas <= 0) {
                estado = "GAME_OVER";
            }
        }
    }

    // Avançar fase
    if (estado === "JOGANDO" && inimigos.length === 0 && !boss && fase < 3) {
        fase++;
        tirosInimigos = [];
        criarOnda(fase);
    }
}

function desenhar() {
    ctx.fillStyle = CORES.PRETO;
    ctx.fillRect(0, 0, LARGURA, ALTURA);

    // Estrelas
    ctx.fillStyle = CORES.BRANCO;
    estrelas.forEach((e) => ctx.fillRect(e.x, e.y, 2, 2));

    // Jogador
    if (jogador.invencivel === 0 || Math.floor(jogador.invencivel / 5) % 2 === 0) {
        desenharSprite(MATRIZ_NAVE, { "1": CORES.AZUL_NAVE, "2": CORES.BRANCO, "3": CORES.VERMELHO }, jogador.x, jogador.y, 4);
    }

    // Inimigos
    inimigos.forEach((inimigo) => {
        desenharSprite(MATRIZ_ALIEN, { "1": CORES.VERDE_ALIEN, "2": CORES.PRETO }, inimigo.x, inimigo.y, 3);
    });

    // Chefão
    if (boss) {
        desenharSprite(MATRIZ_BOSS, { "1": CORES.ROXO_BOSS, "2": CORES.AMARELO, "3": CORES.VERMELHO }, boss.x, boss.y, 5);
        ctx.fillStyle = CORES.VERMELHO;
        ctx.fillRect(170, 12, 300, 10);
        ctx.fillStyle = CORES.VERDE_ALIEN;
        ctx.fillRect(170, 12, 300 * (boss.hp / boss.maxHp), 10);
    }

    // Tiros
    ctx.fillStyle = CORES.AMARELO;
    tirosJogador.forEach((t) => ctx.fillRect(t.x, t.y, t.largura, t.altura));

    ctx.fillStyle = CORES.VERMELHO;
    tirosInimigos.forEach((t) => ctx.fillRect(t.x, t.y, t.largura, t.altura));

    // HUD
    ctx.fillStyle = CORES.AMARELO;
    ctx.font = "bold 18px Courier New";
    ctx.textAlign = "left";
    ctx.fillText(`PONTOS: ${pontos}   VIDAS: ${jogador.vidas}   FASE: ${fase}`, 15, ALTURA - 15);

    // Telas finais
    if (estado === "GAME_OVER" || estado === "VITORIA") {
        ctx.fillStyle = "rgba(15, 15, 30, 0.8)";
        ctx.fillRect(0, 0, LARGURA, ALTURA);

        ctx.textAlign = "center";
        ctx.font = "bold 36px Courier New";
        ctx.fillStyle = estado === "GAME_OVER" ? CORES.VERMELHO : CORES.VERDE_ALIEN;
        ctx.fillText(estado === "GAME_OVER" ? "FIM DE JOGO!" : "MISSAO CUMPRIDA!", LARGURA / 2, ALTURA / 2 - 20);

        ctx.font = "bold 18px Courier New";
        ctx.fillStyle = CORES.BRANCO;
        ctx.fillText(`Pontuacao Final: ${pontos} - Pressione R para reiniciar`, LARGURA / 2, ALTURA / 2 + 25);
    }
}

function loop() {
    atualizar();
    desenhar();
    requestAnimationFrame(loop);
}

iniciarJogo();
loop();