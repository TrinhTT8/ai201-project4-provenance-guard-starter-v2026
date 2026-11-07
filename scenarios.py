"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "When I was 6, my mom took me to Thailand during her worktrip. Because I was a kid back then, I couldn't remember much of the city elements. However, it was a special trip and it brought me so many nostalgic moments whenever I do visit Thailand again. It's a great city with bustling streets, savory dishes, kind people and beautiful architectures. Definitely, one of my favorite country to travel to.",
            "My favorite TV show is Arcane. It is an animated show, adapted from a famous video game, League of Legends. Although I am not a League player, I really enjoy the show and its plot. The dynamic characters, the music, the scenery and the animations were top-notched, with each details being embedded with intentions. I have rewatched the show several time, but I don't ever get tired or bored of it. If I need to kill time on the plane, I will turn on Arcane for sure.",
            "Hello, my name is Jane Doe and I like to try out new coffee shops. There's has been a trend with coffee shops in the city I live, and they usually have a diverse lineup for each seasonal holidays. Lots of unique and aesthetic places are opening up, so me and my sister has come up with a plan to try a new one weekly. This week, we tried out a new matcha place, but it didn't live up to our expectations...",
            "Everyone is out due to the holiday at the office. It feels so empty and spacious. You would usually hear people talk in their meeting, people typing on their keyboards or chit chatters along the hallway. Today, there is none of that but the sound of the air condition.",
            "What is the best time to beat traffic in the morning? It always take me more than 40 minutes to get to the office no matter how early I start. It is incredibly annoying sitting in the traffic. Therefore, I am trying to plan out the best time to leave the house in the morning, so I don't have to hit the traffic and all the craziness on the road. My plan is to get out of the house by 7 am because that's when all the school buses are not active yet, so less traffic on the road.",
            "The weather in Texas is so unpredictable. One day it is hot and the next day, we are living in the ice age. However, I do prefer the cold more because Texas' heat is no joke. In the summer, the outside feels like a melting pot. To the point where I could feel my skin burning just walking under the sun. Even though I don't appreciate the spontaneous weather conditions in Texas, I still enjoy the Fall weather we are entering. Not too hot but not too cold.",
            "Time has flown by quickly. It is almost the end of 2026, and I still remember when we just celebrated the new year in January. I feel like you don't notice the clock ticking by when you are packed with schedules, work, chores, hang outs and other responsibilities. That's why I have been trying to be more mindful spending my time. My goals are to travel and hang out with my family and friends more. Hopefully, I could make it a tradition to have a family vacation once a year!",
            "Fruits are an amazing source of vitamin and fiber. They have natural sugar, rich minerals and can support your health and digestive system. My favorites are kiwi, mango, plum, pineapple and strawberry. I try to incorporate fruits into my diet by having them as desserts or snacks. Yet, I know that some fruits need to be eaten in moderation since they spike your sugar.",
            "The dog jumped over the neighbor's fence. We didn't know why she did such thing, but we are hypothesizing that she saw a squirrel. Our dog is known to be the squirrel catcher because she would go crazy if she sees a squirrel on the street. One time, while we were walking around the neighborhood, she saw a squirrel and just took off. Luckily, we held on to her leash, so she wouldn't run across the street to chase the squirrel. We seriously need to take her to training or teach her not to do that...",
            "This is a sentence, just a sentence. You know how sentences are made up of words, punctuation, tone, and many other things. Just like that, this is also a sentence that was made up of all those elements. Sentences are easy to write, and they should make sense to the reader (or at least I hope so). Stories, news, and blogs are all made up of sentences, all pieced together to make something meaningful.",
        ],
    },
    # Criterion 2 (appeals) is tested by hand with curl, not here: run_eval.py
    # only calls /submit, and an appeal needs a real content_id from a
    # submission first. 5 appeals on a real content_id, 5 on a made-up one,
    # then GET /log to check what was recorded.
    {
        "name": "score spread",
        "criterion": 3,
        # 5 clearly-AI texts (written by Claude) and 5 clearly-human texts
        # (my own writing, reused from criterion 1).
        "texts": [
            # AI
            "Regular exercise is one of the most important habits for maintaining good health. It helps to strengthen the heart, improve circulation, and support a healthy body weight. In addition, physical activity can reduce stress and improve overall mood. Many experts recommend at least thirty minutes of moderate exercise on most days of the week. Furthermore, staying active can lower the risk of many chronic diseases. Overall, making exercise a part of your daily routine is a simple and effective way to improve your quality of life.",
            "Effective time management is an essential skill for students in today's fast-paced academic environment. By prioritizing tasks and setting clear goals, students can significantly improve their productivity. Additionally, creating a structured schedule helps to reduce stress and prevent procrastination. It is also important to take regular breaks, as this allows the mind to recharge and maintain focus. Furthermore, utilizing digital tools such as calendars and task managers can streamline the planning process. Ultimately, developing strong time management habits can lead to greater academic success and a healthier work-life balance.",
            "Reading regularly offers many benefits for people of all ages. It helps to improve vocabulary, strengthen memory, and develop critical thinking skills. In addition, reading can reduce stress by providing a healthy escape from daily pressures. Many people find that reading before bed improves the quality of their sleep. Furthermore, exposure to different stories and perspectives can increase empathy and understanding. Overall, making time to read each day is a simple way to support both mental health and personal growth.",
            "Social media has become an important part of modern communication. It allows people to stay connected with friends and family, regardless of distance. In addition, social media platforms provide access to news, entertainment, and educational content. However, it is important to use these platforms responsibly, as excessive use can affect mental health and productivity. Setting time limits and taking regular breaks can help maintain a healthy balance. Ultimately, social media can be a valuable tool when it is used in a mindful and intentional way.",
            "Remote work has transformed the way many organizations operate. It offers employees greater flexibility and eliminates the need for a daily commute. In addition, remote work can improve productivity by reducing workplace distractions. However, it also presents challenges, such as maintaining clear communication and building strong team relationships. To address these challenges, many companies use video conferencing and collaboration tools. Overall, remote work can be highly effective when supported by the right technology and clear expectations.",
            # Human (mine)
            "When I was 6, my mom took me to Thailand during her worktrip. Because I was a kid back then, I couldn't remember much of the city elements. However, it was a special trip and it brought me so many nostalgic moments whenever I do visit Thailand again. It's a great city with bustling streets, savory dishes, kind people and beautiful architectures. Definitely, one of my favorite country to travel to.",
            "My favorite TV show is Arcane. It is an animated show, adapted from a famous video game, League of Legends. Although I am not a League player, I really enjoy the show and its plot. The dynamic characters, the music, the scenery and the animations were top-notched, with each details being embedded with intentions. I have rewatched the show several time, but I don't ever get tired or bored of it. If I need to kill time on the plane, I will turn on Arcane for sure.",
            "What is the best time to beat traffic in the morning? It always take me more than 40 minutes to get to the office no matter how early I start. It is incredibly annoying sitting in the traffic. Therefore, I am trying to plan out the best time to leave the house in the morning, so I don't have to hit the traffic and all the craziness on the road. My plan is to get out of the house by 7 am because that's when all the school buses are not active yet, so less traffic on the road.",
            "The weather in Texas is so unpredictable. One day it is hot and the next day, we are living in the ice age. However, I do prefer the cold more because Texas' heat is no joke. In the summer, the outside feels like a melting pot. To the point where I could feel my skin burning just walking under the sun. Even though I don't appreciate the spontaneous weather conditions in Texas, I still enjoy the Fall weather we are entering. Not too hot but not too cold.",
            "The dog jumped over the neighbor's fence. We didn't know why she did such thing, but we are hypothesizing that she saw a squirrel. Our dog is known to be the squirrel catcher because she would go crazy if she sees a squirrel on the street. One time, while we were walking around the neighborhood, she saw a squirrel and just took off. Luckily, we held on to her leash, so she wouldn't run across the street to chase the squirrel. We seriously need to take her to training or teach her not to do that...",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 4,
        # 2 clearly human (mine), 2 clearly AI (Claude), 1 borderline (AI text
        # lightly edited). Only the borderline one should land in unsure.
        "texts": [
            # Human (mine)
            "Everyone is out due to the holiday at the office. It feels so empty and spacious. You would usually hear people talk in their meeting, people typing on their keyboards or chit chatters along the hallway. Today, there is none of that but the sound of the air condition.",
            "Time has flown by quickly. It is almost the end of 2026, and I still remember when we just celebrated the new year in January. I feel like you don't notice the clock ticking by when you are packed with schedules, work, chores, hang outs and other responsibilities. That's why I have been trying to be more mindful spending my time. My goals are to travel and hang out with my family and friends more. Hopefully, I could make it a tradition to have a family vacation once a year!",
            # AI
            "Regular exercise is one of the most important habits for maintaining good health. It helps to strengthen the heart, improve circulation, and support a healthy body weight. In addition, physical activity can reduce stress and improve overall mood. Many experts recommend at least thirty minutes of moderate exercise on most days of the week. Furthermore, staying active can lower the risk of many chronic diseases. Overall, making exercise a part of your daily routine is a simple and effective way to improve your quality of life.",
            "Reading regularly offers many benefits for people of all ages. It helps to improve vocabulary, strengthen memory, and develop critical thinking skills. In addition, reading can reduce stress by providing a healthy escape from daily pressures. Many people find that reading before bed improves the quality of their sleep. Furthermore, exposure to different stories and perspectives can increase empathy and understanding. Overall, making time to read each day is a simple way to support both mental health and personal growth.",
            # Borderline
            "Time management is a big deal for students, especially with how busy school gets. If you prioritize tasks and set clear goals, you can get a lot more done. Making a schedule helps too. Honestly, it cuts down on stress and stops you from putting things off until the last minute. Take breaks! Your brain needs time to recharge or you just lose focus. I also use my phone calendar and a to-do app to plan things out, which saves a lot of time. In the end, good habits now mean better grades and less burnout later.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "     ", "creator_id": "eval_bad_spaces"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 1001, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
