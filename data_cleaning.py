import pandas as pd
import matplotlib.pyplot as plt
def remove_outliers(col):
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    return col.where((col >= lower) & (col <= upper))

df=pd.read_csv("hard_dataset.csv")

df["name"]=df["name"].str.strip().str.lower()
df["name"]=df["name"].fillna("unknown")
df["name"]=df["name"].str.title()

df["age"]=pd.to_numeric(df["age"], errors="coerce")
df.loc[df["age"]<0,"age"]=pd.NA
df.loc[df["age"]>100,"age"]=pd.NA
df["age"]=df["age"].fillna(df["age"].mean())


df["department"]=df["department"].str.strip().str.lower()
df["department"]=df["department"].fillna("not assigned")
df["department"]=df["department"].str.title()

df["salary"]=pd.to_numeric(df["salary"],errors="coerce")
df.loc[df["salary"]<0,"salary"]=pd.NA
df["salary"]=remove_outliers(df["salary"])
df["salary"]=df["salary"].fillna(df["salary"].median())

df["joining_date"]=pd.to_datetime(df["joining_date"],errors="coerce")
df["joining_date"]=df["joining_date"].fillna(df["joining_date"].median())

today=pd.to_datetime("today")
df["experience years"]=(today-df["joining_date"]).dt.days/365.25


df["performance_score"]=pd.to_numeric(df["performance_score"],errors="coerce")
df.loc[df["performance_score"]<0,"performance_score"]=pd.NA
df.loc[df["performance_score"]>10,"performance_score"]=pd.NA
df["performance_score"]=remove_outliers(df["performance_score"])
df["performance_score"]=df["performance_score"].fillna(df["performance_score"].median())

df["city"]=df["city"].str.strip().str.lower()
df["city"]=df["city"].fillna(df["city"].mode()[0])
df["city"]=df["city"].str.title()

df.to_csv("clear dataset")
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.groupby("department")["salary"].mean())
print(df.groupby("department")["salary"].max())
print(df.head())

plt.figure(figsize=(14,10))
plt.subplot(2,2,1)
df.groupby("department")["salary"].mean().plot(kind="bar",color="orange")
plt.title("average salary by department",fontsize=12)

plt.subplot(2,2,2)
plt.scatter(df["performance_score"],df["salary"],color="green")
plt.xlabel("Performance of the employees")
plt.ylabel("salaries of the employees")
plt.title("performance vs salary",fontsize=12)

plt.subplot(2,2,3)
df["city"].value_counts().plot(kind="pie",autopct="%1.1f%%",)
plt.title("employees by the city",fontsize=12)

plt.subplot(2,2,4)
df["department"].value_counts().plot(kind="bar",color="green")
plt.title("employees per department")
plt.suptitle("DASHBOARD OF THE INDUSTRY REPORT ",fontsize=16)
plt.tight_layout()
plt.savefig("DASHBOARD.png")
plt.show()
