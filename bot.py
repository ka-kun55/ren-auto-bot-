import os
import time
import random
import google.generativeai as genai
import tweepy

# -------------------------------------------------------------
# 金庫（Secrets）から安全に鍵を読み込み
# -------------------------------------------------------------
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
NOTE_URL = "https://note.com/ren_highvalue"

twitter_client = tweepy.Client(
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
)

# 万が一AIが落ちていた場合の非常用テキスト（絶対に止まらせない）
FALLBACK_TWEETS = [
    f"「手持ちのスキルを磨けば単価が上がる」は受託の罠。必要なのはスキルの習得ではなく「パッケージ化と商談の型」です。徹夜で月収20万から抜け出した全手順をnoteにまとめました👇\n{NOTE_URL}",
    f"なぜ努力家ほど月収20万で力尽き、要領のいい人が月商100万を稼ぐのか？差は「売り方」だけです。労働時間を半分にして30万〜50万の案件を安定受注する事業戦略はこちら👇\n{NOTE_URL}"
]

def generate_tweet():
    """レンさん本人になりきってバズるツイートを生成"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        あなたは「レン | 高単価化の事業戦略」本人です。
        X（Twitter）で、下請けや低単価・徹夜作業で疲弊している個人事業主やフリーランスに向けて、
        思わず手が止まる有益で本質を突いた投稿を1件作成してください。

        【あなたの背景】
        ・元・月収20万で徹夜ばかりしていた受託ワーカー
        ・スキル習得をやめ「伴走パッケージ化」と「商談の型」で手持ちスキルのまま30万〜50万の案件を安定受注
        ・労働時間を半分にし月商100万を達成

        【条件】
        - 1行目は強烈な共感や問いかけ（例: 「徹夜で作業して手取り20万未満のあなたへ」「単価が上がらない本当の理由」）
        - スキルを増やすのではなく「売り方」を変えるべきという気づきを与える
        - 最後にこのnote記事への誘導を入れる: {NOTE_URL}
        - 日本語130文字以内（文字数厳守！）
        - 本文のみを出力すること
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if len(text) > 140:
            text = text[:135] + "…"
        return text
    except Exception as e:
        print(f"AI生成エラー（予備テキストを使用）: {e}")
        return random.choice(FALLBACK_TWEETS)

def post_tweet(text):
    """Xへ投稿"""
    try:
        time.sleep(random.randint(2, 5))
        res = twitter_client.create_tweet(text=text)
        print(f"【大成功！】Xへ完全自動投稿されました！ ツイートID: {res.data['id']}")
    except Exception as e:
        print(f"投稿エラー: {e}")
        raise e

if __name__ == "__main__":
    print("=== 自動化タスク起動（あなた爆睡中） ===")
    tweet = generate_tweet()
