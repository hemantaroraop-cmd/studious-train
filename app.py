from flask import Flask, request, jsonify
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import aiohttp
import requests
import json
import os
import threading
from datetime import datetime
import like_pb2
import uid_generator_pb2
import visit_count_pb2
from google.protobuf.message import DecodeError
from collections import OrderedDict

app = Flask(__name__)

# ✅ API keys
VALID_API_KEYS = {
    "BATMANXD"
}

# 🔢 Daily limit
daily_limit = 500
used_count = 0
last_reset_date = datetime.now().date()
counter_lock = threading.Lock()

# 🌐 Proxy list (optional — agar block ho raha ho toh)
PROXIES = [
    # "http://user:pass@ip:port",
]


# ================= COUNTER MANAGEMENT =================

def check_reset():
    """Har request pe check karo — agar naya din hai toh reset"""
    global used_count, last_reset_date
    today = datetime.now().date()
    if today != last_reset_date:
        with counter_lock:
            used_count = 0
            last_reset_date = today
        app.logger.info(f"🔄 Counter reset for new day: {today}")


def increment_used():
    global used_count
    with counter_lock:
        used_count += 1


# ================= TOKEN LOADING =================

def load_tokens(region):
    try:
        if region == "IND":
            path = "token_ind.json"
        elif region in {"BR", "US", "SAC", "NA"}:
            path = "token_br.json"
        else:
            path = "token_bd.json"

        if not os.path.exists(path):
            app.logger.error(f"❌ Token file not found: {path}")
            return None

        with open(path, "r") as f:
            tokens = json.load(f)

        # ✅ Sirf valid tokens filter karo
        valid = [t for t in tokens if t.get("token") and len(t["token"]) > 20]
        app.logger.info(f"✅ Loaded {len(valid)}/{len(tokens)} valid tokens for {region}")
        return valid if valid else None

    except Exception as e:
        app.logger.error(f"Error loading tokens for {region}: {e}")
        return None


# ================= ENCRYPTION =================

def encrypt_message(plaintext):
    try:
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = pad(plaintext, AES.block_size)
        return binascii.hexlify(cipher.encrypt(padded)).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Encryption error: {e}")
        return None


# ================= PROTOBUF =================

def create_protobuf_message(user_id, region):
    try:
        msg = like_pb2.like()
        msg.uid = int(user_id)
        msg.region = region
        return msg.SerializeToString()
    except Exception as e:
        app.logger.error(f"Protobuf (like) error: {e}")
        return None


def create_protobuf(uid):
    try:
        msg = uid_generator_pb2.uid_generator()
        msg.saturn_ = int(uid)
        msg.garena = 1
        return msg.SerializeToString()
    except Exception as e:
        app.logger.error(f"Protobuf (uid) error: {e}")
        return None


def enc(uid):
    data = create_protobuf(uid)
    if data is None:
        return None
    return encrypt_message(data)


# ================= HTTP REQUEST =================

async def send_request(encrypted_uid, token, url, session):
    """Single like request — session reuse hota hai"""
    try:
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB55"
        }

        proxy = PROXIES[hash(token) % len(PROXIES)] if PROXIES else None

        async with session.post(
            url, data=edata, headers=headers,
            timeout=aiohttp.ClientTimeout(total=15),
            proxy=proxy
        ) as response:
            text = await response.text()
            if response.status == 200:
                app.logger.info(f"✅ Like OK: {token[:15]}...")
            else:
                app.logger.warning(f"⚠️ Token fail: {token[:15]}... status={response.status}")
            return text

    except asyncio.TimeoutError:
        app.logger.warning(f"⏱ Timeout: {token[:15]}...")
        return None
    except Exception as e:
        app.logger.error(f"send_request error: {e}")
        return None


async def send_multiple_requests(uid, region, url):
    """Batch me 270 tokens ko bhejo — load control ke saath"""
    try:
        protobuf_message = create_protobuf_message(uid, region)
        if protobuf_message is None:
            return []

        encrypted_uid = encrypt_message(protobuf_message)
        if encrypted_uid is None:
            return []

        tokens = load_tokens(region)
        if not tokens:
            return []

        all_results = []
        batch_size = 20
        delay = 0.5

        # ✅ Ek hi session reuse karo — load kam
        connector = aiohttp.TCPConnector(limit=50, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            for i in range(0, len(tokens), batch_size):
                batch = tokens[i:i + batch_size]
                tasks = [
                    send_request(encrypted_uid, t["token"], url, session)
                    for t in batch
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                all_results.extend(results)

                # ✅ Chhota gap — server block nahi karega
                if i + batch_size < len(tokens):
                    await asyncio.sleep(delay)

        success = sum(1 for r in all_results if r)
        app.logger.info(f"📊 Batch complete: {success}/{len(tokens)} success")
        return all_results

    except Exception as e:
        app.logger.error(f"send_multiple_requests error: {e}")
        return []


# ================= PLAYER INFO =================

def make_request(encrypt, region, token):
    try:
        if region == "IND":
            url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
        elif region in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
        else:
            url = "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow"

        edata = bytes.fromhex(encrypt)
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB55"
        }
        response = requests.post(url, data=edata, headers=headers, verify=False, timeout=15)
        decoded = visit_count_pb2.Info()
        decoded.ParseFromString(response.content)
        return decoded
    except DecodeError as e:
        app.logger.error(f"DecodeError: {e}")
        return None
    except Exception as e:
        app.logger.error(f"make_request error: {e}")
        return None


# ================= ROUTES =================

@app.route('/like', methods=['GET'])
def handle_requests():
    check_reset()

    # ✅ API key check
    api_key = request.args.get("key")
    if api_key not in VALID_API_KEYS:
        return app.response_class(
            response=json.dumps(OrderedDict([
                ("error", "Invalid or missing API key"),
                ("status", 3)
            ]), separators=(',', ':')),
            status=401,
            mimetype='application/json'
        )

    uid = request.args.get("uid")
    region = request.args.get("region", "").upper()

    if not uid or not region:
        return jsonify({"error": "UID and region are required", "status": 3}), 400

    try:
        # ✅ Pehle player info lo
        tokens = load_tokens(region)
        if not tokens:
            raise Exception("Failed to load tokens")

        token = tokens[0]['token']
        encrypted_uid = enc(uid)
        if not encrypted_uid:
            raise Exception("Encryption failed")

        before = make_request(encrypted_uid, region, token)
        if before is None:
            raise Exception("Failed to get initial info")

        before_like = before.AccountInfo.Likes

        # ✅ Like URL
        if region == "IND":
            url = "https://client.ind.freefiremobile.com/LikeProfile"
        elif region in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/LikeProfile"
        else:
            url = "https://clientbp.ggpolarbear.com/LikeProfile"

        # ✅ Likes bhejo
        asyncio.run(send_multiple_requests(uid, region, url))

        # ✅ After info
        after = make_request(encrypted_uid, region, token)
        if after is None:
            raise Exception("Failed to get final info")

        after_like = after.AccountInfo.Likes
        like_given = max(after_like - before_like, 0)
        status = 1 if like_given > 0 else 2

        if status == 1:
            increment_used()

        remaining = max(daily_limit - used_count, 0)

        result = OrderedDict([
            ("LikesGivenByAPI", like_given),
            ("LikesafterCommand", after_like),
            ("LikesbeforeCommand", before_like),
            ("PlayerNickname", after.AccountInfo.PlayerNickname),
            ("Level", after.AccountInfo.Levels),
            ("Region", after.AccountInfo.PlayerRegion),
            ("UID", after.AccountInfo.UID),
            ("status", status),
            ("daily_limit", daily_limit),
            ("used", used_count),
            ("remaining", remaining)
        ])

        return app.response_class(
            response=json.dumps(result, separators=(',', ':')),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        app.logger.error(f"handle_requests error: {e}")
        return jsonify({"error": str(e), "status": 3}), 500


@app.route('/remain', methods=['GET'])
def remain_info():
    check_reset()
    remaining = max(daily_limit - used_count, 0)
    return jsonify({
        "daily_limit": daily_limit,
        "remaining": remaining,
        "used": used_count,
        "reset_info": "4:00 AM IST"
    })


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "endpoints": ["/like?key=ZEXXY&uid=XXX&region=IND", "/remain"],
        "daily_limit": daily_limit,
        "used": used_count
    })


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)
