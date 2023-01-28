from ssg import from_yaml, to_dataframe

ssg_list = from_yaml("data/ssg2.yaml")
print(ssg_list)
df = to_dataframe(ssg_list)
df.to_csv("data/ssg.csv")
