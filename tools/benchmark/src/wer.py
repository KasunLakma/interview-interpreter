def normalize(text):
    """අකුරු සරල කරලා වචන ලැයිස්තුවක් බවට හරවයි."""
    text = text.lower().strip()
    # සිංහල අකුරු වල ඇති නොපෙනෙන සම්බන්ධක අකුරු ඉවත් කරයි
    text = text.replace("\u200d", "").replace("\u200c", "")
    for ch in '.,!?;:"()[]':
        text = text.replace(ch, " ")
    return text.split()


def word_error_rate(reference, hypothesis):
    """
    reference  = නිවැරදි වාක්‍යය
    hypothesis = STT සේවාවෙන් ලැබුණු වාක්‍යය
    ප්‍රතිඵලය: 0.0 (සම්පූර්ණ නිවැරදි) සිට ඉහළට
    """
    ref = normalize(reference)
    hyp = normalize(hypothesis)

    if not ref:
        return 0.0 if not hyp else 1.0

    # වචන මට්ටමේ edit distance (Levenshtein)
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i]
        for j, h in enumerate(hyp, 1):
            cost = 0 if r == h else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur

    return prev[-1] / len(ref)


if __name__ == "__main__":
    ref = "I have worked for five years as a welder"
    hyp = "I have worked for five year as welder"
    print(f"WER: {word_error_rate(ref, hyp):.2%}")