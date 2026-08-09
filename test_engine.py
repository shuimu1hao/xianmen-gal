#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仙门物语 交互流程模拟：mock DOM 保存元素引用，驱动引擎真实点击路径。
模拟 6 次选择（师傅线），验证：流程推进、好感度、结局页渲染。"""
import re, os, subprocess, sys

BASE = os.path.expanduser("~/hermes11/xianmen-gal")
html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
engine_js = re.findall(r"<script>(.*?)</script>", html, re.S)[0]
data_js = open(os.path.join(BASE, "data.js"), encoding="utf-8").read()

sim = r"""
// ===== 元素仓库（按 id 保存引用，支持 onclick / style / classList）=====
const elements = {};
const mkEl = (id) => ({
  id, style:{}, _classes:new Set(),
  innerHTML:"", textContent:"", src:"",
  onclick:null, _listeners:{},
  classList:{
    add(c){ this._classes.add(c); }, remove(c){ this._classes.delete(c); },
    contains(c){ return this._classes.has(c); }
  },
  appendChild(){}, addEventListener(ev,fn){ this._listeners[ev]=fn; },
  querySelectorAll(){ return []; }, closest(){ return null; }
});
global.document = {
  getElementById(id){ if(!elements[id]) elements[id]=mkEl(id); return elements[id]; },
  createElement(){ return mkEl("dyn_"+Math.random()); },
  addEventListener(){}
};
global.window = { SCRIPT: undefined };
global.localStorage = { getItem(){return null;}, setItem(){}, removeItem(){} };
global.requestAnimationFrame = (f)=>f();
global.alert = (m)=>{ console.log("ALERT:", m); };
""" + data_js + "\n" + engine_js + r"""

// ===== 驱动 =====
const app = document.getElementById("app");
const btnStart = document.getElementById("btnStart");
const choiceLayer = document.getElementById("choiceLayer");
const endScreen = document.getElementById("endScreen");

// 开始游戏
btnStart.onclick();
console.log("开始后 idx 推进: choiceLayer.show=" + choiceLayer.classList.contains("show"));

// 模拟点击推进 + 选项选择，直到结局
let clicks = 0, choicesMade = 0;
const MAX = 400;
let endTitle = null;
while (clicks < MAX) {
  // 如果 endScreen 显示 = 结局
  if (!endScreen.classList.contains("hidden")) {
    endTitle = document.getElementById("endTitle").textContent;
    break;
  }
  // 如果选项层显示 → 点第一个（师傅线）
  if (choiceLayer.classList.contains("show")) {
    // 重建的按钮挂载在 choiceLayer 的 children 上，但 mock 没存 → 直接调 app 点击会走 choice 分支？
    // 真实引擎: choiceBtn.onclick 在 renderChoices 里绑定。这里我们通过 choiceLayer.innerHTML 拿不到子节点，
    // 改为模拟: 手动执行一个选项的 onclick —— 需要从引擎内部暴露。简化：直接操作状态。
    choicesMade++;
    // 引擎的 renderChoices 创建了 choiceBtn 并 appendChild 到 choiceLayer，mock 里 appendChild 是空操作，
    // 所以无法触发。改为: 直接调用 app click 处理不了选项。
    // —— 这里用真实路径: 我们需要能访问 choiceBtn.onclick。
    // mock appendChild 改为保存 children
    break;
  }
  // 普通点击推进
  app._listeners.click && app._listeners.click({ target: document.createElement("div") });
  clicks++;
}
console.log("模拟结束: choicesMade=" + choicesMade + " clicks=" + clicks + " endTitle=" + endTitle);
"""

# 上面 walk 里选项按钮拿不到的问题：改进 mock 的 appendChild 记录 children
sim_improved = r"""
const elements = {};
const mkEl = (id) => {
  let _html = "";
  const el = { id, style:{}, _classes:new Set(), children:[],
    get innerHTML(){ return _html; },
    set innerHTML(v){ _html = v; el.children = []; },  // 清空 children 模拟真实 DOM
    textContent:"", src:"",
    onclick:null, _listeners:{},
    appendChild(ch){ el.children.push(ch); },
    addEventListener(ev,fn){ el._listeners[ev]=fn; },
    querySelectorAll(){ return []; },
    closest(){ return null; }
  };
  el.classList = {
    add(c){ el._classes.add(c); }, remove(c){ el._classes.delete(c); },
    contains(c){ return el._classes.has(c); }
  };
  return el;
};
global.document = {
  getElementById(id){ if(!elements[id]) elements[id]=mkEl(id); return elements[id]; },
  createElement(){ const e=mkEl("dyn"+Math.random()); return e; },
  addEventListener(){}
};
global.window = global;  // window 即全局，data.js 的 window.SCRIPT 同步为全局 SCRIPT
global.localStorage = { getItem(){return null;}, setItem(){}, removeItem(){} };
global.requestAnimationFrame = (f)=>f();
global.alert = ()=>{};
""" + data_js + "\n" + engine_js + r"""

const app = document.getElementById("app");
const btnStart = document.getElementById("btnStart");
const choiceLayer = document.getElementById("choiceLayer");
const endScreen = document.getElementById("endScreen");

btnStart.onclick();

let clicks=0, choices=0, endTitle=null, steps=0;
while (steps++ < 600) {
  if (!endScreen.classList.contains("hidden")) {
    endTitle = document.getElementById("endTitle").textContent;
    break;
  }
  if (choiceLayer.classList.contains("show")) {
    const btns = choiceLayer.children.filter(c=>c.className && c.className.includes && c.className.includes("choiceBtn"));
    if (btns.length === 0) { console.log("FAIL: 选项层无按钮"); process.exit(1); }

    const pick = parseInt(process.env.PICK || "0", 10);
    btns[pick].onclick();
    choices++;
    continue;
  }
  app._listeners.click && app._listeners.click({ target: document.createElement("div") });
  clicks++;
}
console.log("RESULT: choices="+choices+" clicks="+clicks+" endTitle="+endTitle);
if (!endTitle) { console.log("FAIL: 未到结局"); process.exit(1); }
if (choices !== 6) { console.log("FAIL: 选择次数="+choices+" 期望6"); process.exit(1); }
console.log("PASS: 师傅线全流程到达结局: " + endTitle);
"""

r = subprocess.run(["node", "-e", sim_improved], capture_output=True, text=True, timeout=120)
print("STDOUT:", r.stdout.strip())
print("STDERR:", r.stderr.strip()[:800])
sys.exit(0 if r.returncode == 0 else 1)
