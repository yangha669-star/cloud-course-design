from flask import Flask, jsonify
import os
import redis
import requests

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

@app.route("/")
def index():
    return jsonify({
        "message": "Flask backend is running"
    })

@app.route("/api/ping")
def ping():
    try:
        if REDIS_PASSWORD:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
        else:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True
            )

        r.incr("ping_count")
        count = r.get("ping_count")

        print("收到 /api/ping 请求，当前访问次数：", count, flush=True)

        return jsonify({
            "status": "ok",
            "message": "backend connected redis",
            "ping_count": count
        })

    except Exception as e:
        print("Redis connection error:", str(e), flush=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)