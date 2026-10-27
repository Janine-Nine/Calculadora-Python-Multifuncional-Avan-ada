// Python Ultimate Calculator - Web Edition (JavaScript Core)
document.addEventListener("DOMContentLoaded", () => {
  // Estado
  let expression = "";
  let currentResult = "0";
  let memory = 0;
  let angleMode = "deg";
  let history = JSON.parse(localStorage.getItem("puc_history") || "[]");

  // Elementos
  const exprDisplay = document.getElementById("display-expr");
  const resultDisplay = document.getElementById("display-result");
  const angleFlag = document.getElementById("angle-mode-flag");
  const memFlag = document.getElementById("mem-flag");
  const historyList = document.getElementById("history-list");

  // Navegação de Abas
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      const targetId = `tab-${btn.dataset.tab}`;
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // Alternador de Tema
  document.getElementById("btn-theme-toggle").addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
  });

  // Visor update
  function updateDisplay() {
    exprDisplay.textContent = expression;
    resultDisplay.textContent = currentResult;
    angleFlag.textContent = angleMode.toUpperCase();
    memFlag.textContent = memory !== 0 ? "M" : "";
  }

  // Teclado da Calculadora
  document.querySelectorAll("[data-insert]").forEach((btn) => {
    btn.addEventListener("click", () => {
      expression += btn.dataset.insert;
      updateDisplay();
    });
  });

  document.getElementById("btn-clear").addEventListener("click", () => {
    expression = "";
    currentResult = "0";
    updateDisplay();
  });

  document.getElementById("btn-backspace").addEventListener("click", () => {
    expression = expression.slice(0, -1);
    updateDisplay();
  });

  document.getElementById("btn-toggle-angle").addEventListener("click", () => {
    angleMode = angleMode === "deg" ? "rad" : "deg";
    updateDisplay();
  });

  document.getElementById("btn-sign").addEventListener("click", () => {
    if (currentResult.startsWith("-")) {
      currentResult = currentResult.substring(1);
    } else if (currentResult !== "0") {
      currentResult = "-" + currentResult;
    }
    updateDisplay();
  });

  document.getElementById("btn-inv").addEventListener("click", () => {
    const v = parseFloat(currentResult.replace(",", "."));
    if (v === 0) {
      alert("Divisão por zero.");
      return;
    }
    currentResult = String(1 / v).replace(".", ",");
    updateDisplay();
  });

  document.getElementById("btn-copy").addEventListener("click", () => {
    navigator.clipboard.writeText(currentResult);
    alert(`Resultado '${currentResult}' copiado!`);
  });

  // Avaliação Segura de Expressão (Parser Seguro em JS)
  function safeEval(expr) {
    let sanitized = expr.replace(/,/g, ".");
    sanitized = sanitized.replace(/\^/g, "**");
    sanitized = sanitized.replace(/pi/g, String(Math.PI));
    sanitized = sanitized.replace(/e(?![a-zA-Z0-9])/g, String(Math.E));

    // Funções
    sanitized = sanitized.replace(/sin\(([^)]+)\)/g, (_, val) => {
      const v = safeEval(val);
      const rad = angleMode === "deg" ? (v * Math.PI) / 180 : v;
      return Math.sin(rad);
    });
    sanitized = sanitized.replace(/cos\(([^)]+)\)/g, (_, val) => {
      const v = safeEval(val);
      const rad = angleMode === "deg" ? (v * Math.PI) / 180 : v;
      return Math.cos(rad);
    });
    sanitized = sanitized.replace(/tan\(([^)]+)\)/g, (_, val) => {
      const v = safeEval(val);
      const rad = angleMode === "deg" ? (v * Math.PI) / 180 : v;
      return Math.tan(rad);
    });
    sanitized = sanitized.replace(/sqrt\(([^)]+)\)/g, (_, val) => Math.sqrt(safeEval(val)));
    sanitized = sanitized.replace(/log10\(([^)]+)\)/g, (_, val) => Math.log10(safeEval(val)));
    sanitized = sanitized.replace(/ln\(([^)]+)\)/g, (_, val) => Math.log(safeEval(val)));
    sanitized = sanitized.replace(/abs\(([^)]+)\)/g, (_, val) => Math.abs(safeEval(val)));

    // Fatorial simples (ex: 5!)
    sanitized = sanitized.replace(/(\d+)!/g, (_, num) => {
      let n = parseInt(num, 10);
      let f = 1;
      for (let i = 2; i <= n; i++) f *= i;
      return f;
    });

    // Validação estrita de caracteres permitidos
    if (/[^0-9+\-*/().\s*]/.test(sanitized)) {
      throw new Error("Expressão com caracteres ou sintaxe inválida.");
    }

    const res = Function(`"use strict"; return (${sanitized});`)();
    if (!isFinite(res)) throw new Error("Resultado infinito ou indefinido.");
    return res;
  }

  document.getElementById("btn-equals").addEventListener("click", () => {
    if (!expression.trim()) return;
    try {
      const res = safeEval(expression);
      const formatted = String(Number(res.toFixed(8))).replace(".", ",");
      currentResult = formatted;
      addHistory(expression, formatted, "Básica");
    } catch (err) {
      currentResult = "Erro";
      alert("Erro ao calcular: " + err.message);
    }
    updateDisplay();
  });

  // Memória
  document.querySelectorAll("[data-mem]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.mem;
      const num = parseFloat(currentResult.replace(",", ".")) || 0;
      if (action === "MC") memory = 0;
      else if (action === "MR") expression += String(memory);
      else if (action === "M+") memory += num;
      else if (action === "M-") memory -= num;
      else if (action === "MS") memory = num;
      updateDisplay();
    });
  });

  // Frações
  document.getElementById("btn-calc-frac")?.addEventListener("click", () => {
    const n1 = parseInt(document.getElementById("f-n1").value, 10);
    const d1 = parseInt(document.getElementById("f-d1").value, 10);
    const n2 = parseInt(document.getElementById("f-n2").value, 10);
    const d2 = parseInt(document.getElementById("f-d2").value, 10);
    const op = document.getElementById("f-op").value;

    if (d1 === 0 || d2 === 0) {
      alert("Denominador zero inválido.");
      return;
    }

    let num = 0, den = 1;
    if (op === "+") {
      num = n1 * d2 + n2 * d1;
      den = d1 * d2;
    } else if (op === "-") {
      num = n1 * d2 - n2 * d1;
      den = d1 * d2;
    } else if (op === "*") {
      num = n1 * n2;
      den = d1 * d2;
    } else {
      num = n1 * d2;
      den = d1 * n2;
    }

    function gcd(a, b) {
      return b === 0 ? a : gcd(b, a % b);
    }
    const g = Math.abs(gcd(num, den));
    num /= g;
    den /= g;

    const out = `Resultado Simplificado: ${num}/${den}\nValor Decimal: ${(num / den).toFixed(6)}`;
    document.getElementById("frac-output").textContent = out;
    addHistory(`${n1}/${d1} ${op} ${n2}/${d2}`, `${num}/${den}`, "Frações");
  });

  // Álgebra (2º Grau)
  document.getElementById("btn-calc-quad")?.addEventListener("click", () => {
    const a = parseFloat(document.getElementById("q-a").value);
    const b = parseFloat(document.getElementById("q-b").value);
    const c = parseFloat(document.getElementById("q-c").value);

    if (a === 0) {
      alert("Coeficiente 'a' não pode ser 0 em equação do 2º grau.");
      return;
    }

    const delta = b * b - 4 * a * c;
    let out = `Equação: (${a})x² + (${b})x + (${c}) = 0\nΔ = b² - 4ac = (${b})² - 4·(${a})·(${c}) = ${delta}\n`;

    if (delta > 0) {
      const x1 = (-b + Math.sqrt(delta)) / (2 * a);
      const x2 = (-b - Math.sqrt(delta)) / (2 * a);
      out += `Duas raízes reais distintas:\nx₁ = ${x1.toFixed(4)}\nx₂ = ${x2.toFixed(4)}`;
    } else if (delta === 0) {
      const x = -b / (2 * a);
      out += `Raiz real dupla:\nx = ${x.toFixed(4)}`;
    } else {
      const real = (-b / (2 * a)).toFixed(4);
      const imag = (Math.sqrt(-delta) / (2 * Math.abs(a))).toFixed(4);
      out += `Duas raízes complexas conjugadas (Δ < 0):\nx₁ = ${real} + ${imag}i\nx₂ = ${real} - ${imag}i`;
    }

    document.getElementById("quad-output").textContent = out;
  });

  // Financiamento Price
  document.getElementById("btn-calc-fin")?.addEventListener("click", () => {
    const pv = parseFloat(document.getElementById("fin-pv").value);
    const i = parseFloat(document.getElementById("fin-rate").value) / 100;
    const n = parseInt(document.getElementById("fin-n").value, 10);

    const factor = Math.pow(1 + i, n);
    const pmt = (pv * (i * factor)) / (factor - 1);
    const total = pmt * n;
    const interest = total - pv;

    const fmt = (v) => "R$ " + v.toFixed(2).replace(".", ",");
    const out = `Parcela Mensal Fixa: ${fmt(pmt)}\nTotal a Pagar: ${fmt(total)}\nTotal em Juros: ${fmt(interest)}`;
    document.getElementById("fin-output").textContent = out;
  });

  // Histórico
  function addHistory(expr, res, cat) {
    const item = {
      expr,
      res,
      cat,
      time: new Date().toLocaleTimeString("pt-BR"),
    };
    history.unshift(item);
    if (history.length > 50) history.pop();
    localStorage.setItem("puc_history", JSON.stringify(history));
    renderHistory();
  }

  function renderHistory() {
    if (!historyList) return;
    historyList.innerHTML = history.length === 0 ? "<li style='color:var(--text-muted);'>Nenhum cálculo registrado.</li>" : "";
    history.forEach((h) => {
      const li = document.createElement("li");
      li.className = "history-item";
      li.innerHTML = `<span><strong>[${h.cat}]</strong> ${h.expr}</span><span style="color:var(--accent-light);">${h.res}</span>`;
      historyList.appendChild(li);
    });
  }

  document.getElementById("btn-clear-history")?.addEventListener("click", () => {
    if (confirm("Limpar todo o histórico?")) {
      history = [];
      localStorage.removeItem("puc_history");
      renderHistory();
    }
  });

  renderHistory();
  updateDisplay();
});
