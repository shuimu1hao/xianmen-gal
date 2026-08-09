#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  仙门物语 · 启动/停止脚本
#  用法:
#    bash ~/hermes11/xianmen-gal/start.sh         启动并打开游戏
#    bash ~/hermes11/xianmen-gal/start.sh stop    停止游戏服务器
#    bash ~/hermes11/xianmen-gal/start.sh status  查看运行状态
# ============================================================
PROJ=~/hermes11/xianmen-gal
PORT=8391
URL="http://localhost:$PORT/"

cd "$PROJ" || { echo "❌ 项目目录不存在: $PROJ"; exit 1; }

# ---------- 工具函数 ----------
http_code() {
  curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$URL" 2>/dev/null
}

# 杀掉占用端口的旧 http.server（精确匹配，避免误杀 Hermes）
kill_old_server() {
  local pids
  pids=$(ps -eo pid,args | grep -E "http\.server ${PORT}" | grep -v grep | grep -v "hermes-snap" | awk '{print $1}')
  if [ -n "$pids" ]; then
    echo "🧹 清理旧服务器进程: $pids"
    kill $pids 2>/dev/null
    sleep 1
  fi
}

# ---------- 命令分发 ----------
case "$1" in
  stop)
    kill_old_server
    if [ "$(http_code)" = "000" ]; then
      echo "✅ 游戏服务器已停止"
    else
      echo "⚠️ 仍有响应，尝试强杀..."
      pids=$(ps -eo pid,args | grep -E "http\.server ${PORT}" | grep -v grep | grep -v "hermes-snap" | awk '{print $1}')
      [ -n "$pids" ] && kill -9 $pids 2>/dev/null
      sleep 1
      [ "$(http_code)" = "000" ] && echo "✅ 已停止" || echo "❌ 停止失败"
    fi
    exit 0
    ;;
  status)
    code=$(http_code)
    if [ "$code" = "200" ]; then
      echo "✅ 服务运行中: $URL (HTTP $code)"
      echo "   端口: $PORT"
    else
      echo "❌ 服务未运行 (HTTP $code)"
    fi
    exit 0
    ;;
esac

# ---------- 启动流程 ----------
# 1. 已在运行 → 直接打开
if [ "$(http_code)" = "200" ]; then
  echo "✅ 服务已在运行: $URL"
  termux-open-url "$URL"
  exit 0
fi

# 2. 端口被占用但不是我们的服务 → 提示
if curl -s -o /dev/null --max-time 2 "http://localhost:$PORT/" 2>/dev/null; then
  echo "⚠️ 端口 $PORT 被其他服务占用，尝试清理..."
fi

# 3. 清理残留
kill_old_server

# 4. 启动服务器
echo "🚀 启动游戏服务器: $URL"
nohup python3 -m http.server "$PORT" --bind 127.0.0.1 > "$PREFIX/tmp/xianmen_http.log" 2>&1 &

# 5. 等待就绪（最多 5 秒）
for i in 1 2 3 4 5; do
  sleep 1
  if [ "$(http_code)" = "200" ]; then
    echo "✅ 服务器已就绪 (${i}s)"
    termux-open-url "$URL"
    echo "📱 已在浏览器打开，也可以手动访问: $URL"
    exit 0
  fi
done

# 6. 启动失败诊断
echo "❌ 服务器启动失败，日志如下:"
tail -5 "$PREFIX/tmp/xianmen_http.log" 2>/dev/null
echo "   试试: bash $0 stop 后再启动"
exit 1
