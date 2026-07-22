const form = document.getElementById("question-form");
const input = document.getElementById("question");
const answerBox = document.getElementById("answer");
const qBtns = document.querySelectorAll("[data-question]");

// 点击推荐问题自动填充
qBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        input.value = btn.dataset.question;
    });
});

// 提交表单调用问答接口
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q) return;

    answerBox.classList.remove("empty-state");
    answerBox.innerText = "正在查询数据，请稍候...";

    try {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: q })
        });
        const data = await res.json();
        answerBox.innerText = data.reply;
    } catch (err) {
        answerBox.innerText = "请求失败，请刷新页面后重试。";
    }
});
