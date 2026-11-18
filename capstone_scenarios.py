"""
The fixed inputs for the capstone criteria (criteria.md, "Capstone criteria").

Kept in one file so every trial — and anyone re-running it — sends exactly the
same thing. `run_capstone_eval.py` reads these.

The non-English texts were written for this test (by Claude, see the README's
Capstone "How I Used AI"). They are ordinary, everyday paragraphs on purpose:
the question is never whether they look AI-written, only whether a system that
can't read them labels them AI anyway.
"""

from scenarios import SCENARIOS

# Criterion 2 — ten texts the style signal wasn't built to read. Order and
# names match the criterion sentence.
UNREADABLE_TEXTS = {
    "korean": (
        "나는 어제 친구와 함께 공원에 갔다. 날씨가 정말 좋아서 우리는 오랫동안 걸었다. "
        "그리고 근처 카페에서 커피를 마시면서 이야기를 나눴다."
    ),
    "chinese": (
        "昨天下午我和妹妹去超市买菜。我们买了很多水果和蔬菜，还买了一个蛋糕。"
        "回家以后，妈妈做了一顿很好吃的晚饭。"
    ),
    "russian": (
        "Вчера я ходил в парк с другом. Погода была отличная, и мы долго гуляли. "
        "Потом мы пили кофе в маленьком кафе."
    ),
    "arabic": (
        "ذهبت أمس إلى السوق مع أخي. اشترينا بعض الخبز والفواكه، "
        "ثم جلسنا في مقهى صغير وتحدثنا عن المدرسة."
    ),
    "vietnamese": (
        "Hôm qua tôi đi chợ với mẹ. Chúng tôi mua rau, cá và một ít trái cây. "
        "Buổi tối cả nhà cùng ăn cơm và nói chuyện rất vui."
    ),
    "spanish": (
        "Ayer fui al mercado con mi hermana. Compramos frutas, pan y un poco de queso. "
        "Después caminamos por el parque y hablamos de nuestras clases."
    ),
    "french": (
        "Hier, je suis allée au marché avec ma soeur. Nous avons acheté des fruits, du pain "
        "et un peu de fromage. Ensuite, nous avons marché dans le parc."
    ),
    "emoji_only": "🔥🔥🔥 😂😂 🙌🙌🙌🙌 ❤️❤️ 🎉🎉🎉 👍👍",
    "korean_english_mix": (
        "오늘은 정말 바쁜 하루였다. 회의가 세 번이나 있었고 점심도 못 먹었다. "
        "Honestly I just want to sleep now."
    ),
    "short_english": "I really liked the movie last night.",
}

# Criteria 1 and 3 — one ordinary paragraph both signals can read, so any
# "unsure" comes from the injected fault, not from the text.
NORMAL_TEXT = (
    "The implementation of the proposed framework requires careful consideration "
    "of several key factors. First, it is important to note that the system must "
    "be able to handle a wide variety of different inputs. Additionally, the "
    "overall performance of the solution depends on a number of important variables."
)

# Criterion 5 — the ten normal submissions are my own writing from scenarios.py.
OWN_WRITING = next(s["texts"] for s in SCENARIOS if s["name"] == "my own writing")

# Criterion 5 — the five bad inputs, as (name, how it is sent). "raw" bodies
# are sent as-is with a JSON content type, so the not-JSON one stays broken.
BAD_INPUTS = [
    ("empty text", {"json": {"text": "", "creator_id": "{cid}"}}),
    ("no text field", {"json": {"creator_id": "{cid}"}}),
    ("too short", {"json": {"text": "hi", "creator_id": "{cid}"}}),
    ("over 1000 words", {"json": {"text": "word " * 1001, "creator_id": "{cid}"}}),
    ("not JSON", {"raw": "text=this is not json&creator_id={cid}"}),
]
