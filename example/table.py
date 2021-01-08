from ssg import get_dataframe

def md_link(text, url):
    return f"[{text}]({url})

def make_presentation(df):
    zf = df[["stars", "lang", "url"]]
    zf["stars"] = zf.stars.divide(1000).round(1)
    zf.index = df.apply(lambda x: md_link(x.name, x.url), result_type="expand", axis=1)
    del zf["url"]
    zf.columns = ["'000 stars", "Language"]
    return zf


df = get_dataframe("data/ssg.yaml")
tf = make_presentation(df)
print(tf.to_markdown(tablefmt="github", floatfmt=".1f"))