import os
import sys
import time
import random
import google.generativeai as genai
import tweepy

# -------------------------------------------------------------
# 金庫から鍵を読み込み（前後の空白を自動除去してエラーを完全防止）
# -------------------------------------------------------------
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"].strip()
TWITTER_API_KEY = os.environ["TWITTER_API_KEY"].strip()
TWITTER_API_SECRET = os.environ["TWITTER_API_SECRET"].strip()
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"].strip()
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"].strip()

NOTE_URL = "https://note.com/ren_highvalue"

# -------------------------------------------------------------
# AI原稿作成
# -------------------------------------------------------------
FALLBACK_TWEETS = [
    f"「手持ちのスキルを磨けば単価が上がる」は受託の罠。必要なのはスキルの習得ではなく「パッケージ化と商談の型」です。徹夜で月収20万から抜け出した全手順をnoteにまとめました👇\n{NOTE_URL}",
    f"なぜ努力家ほど月収20万で力尽き、要領のいい人が月商100万を稼ぐのか？差は「売り方」だけです。労働時間を半分にして30万〜50万の案件を安定受注する事業戦略はこちら👇\n{NOTE_URL}"
]

def generate_tweet():
    print("[1/3] AIが投稿文を作成中...", flush=True)
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # 最新のモデル名で接続
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        prompt = f"""
        あなたは「レン | 高単価化の事業戦略」本人です。
        X（Twitter）で、下請けや低単価・徹夜作業で疲弊している個人事業主やフリーランスに向けて、
        思わず手が止まる有益で本質を突いた投稿を1件作成してください。

        【条件】
        - 1行目は強烈な問いかけや共感
        - スキル習得ではなく「売り方」を変えるべきという気づき
        - 最後にこのnote記事への誘導を入れる: {NOTE_URL}
        - 日本語120文字以内（文字数厳守）
        - 本文のみを出力
        """
        res = model.generate_content(prompt)
        text = res.text.strip()
        if len(text) > 140:
            text = text[:135] + "…"
        print("AI生成成功！", flush=True)
        return text
    except Exception as e:
        print(f"AI一時エラー（予備テキストを採用）: {e}", flush=True)
        return random.choice(FALLBACK_TWEETS)

# -------------------------------------------------------------
# Xへの投稿
# -------------------------------------------------------------
def post_tweet(tweet_text):
    print("[2/3] Xへ接続中...", flush=True)
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    
    print("[3/3] ツイートを投稿中...", flush=True)
    time.sleep(2)
    res = client.create_tweet(text=tweet_text)
    tweet_id = res.data['id']
    tweet_url = f"https://x.com/i/web/status/{tweet_id}"
    print(f"\n==========================================", flush=True)
    print(f"【大成功！】Xへ完全自動投稿されました！", flush=True)
    print(f"投稿URL: {tweet_url}", flush=True)
    print(f"==========================================\n", flush=True)

if __name__ == "__main__":
    print("=== 自動化タスク起動（あなた爆睡中） ===", flush=True)
    text = generate_tweet()
    print(f"\n【投稿内容】:\n{text}\n", flush=True)
    post_tweet(text)
    print("=== 全タスク完了！ ===", flush=True)
